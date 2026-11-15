#!/usr/bin/env python3
"""
Exercise 24.4: run the same program on the C machine and on the CPU, and
compare the stack after every instruction, as chapter 8's compare.py
compared traces.

    python3 compare.py [count]

The C machine is chapter 11's, whose -t writes, after every step, its
number, the address, the instruction and the stack, with | where each
frame's locals begin. The CPU is build.py's trace variant, whose testbench
writes the same with +trace, but for the instruction. The first 3000 steps
are compared, address and stack, and then what the program printed and how
it ended, if it ended by then. The programs: the samples, the suite's
programs of versions 1 and 2, and random ones from chapter 21's fuzz.py,
seed 1, the first 300 unless told.
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
C = os.path.join(CHAPTER, "..", "ch11-basal")
FUZZ = os.path.join(CHAPTER, "..", "ch21-verify", "fuzz.py")
STEPS = 3000
sys.path.insert(0, CHAPTER)
import isa  # noqa: E402
import vmfile  # noqa: E402

OPERANDS = {name: len(kinds) for code, name, kinds in isa.INSTRUCTIONS}


def first_lines(command, n):
    """The first n lines of stderr; if the program ends by then, also its
    output and its status, and None for both if it is stopped."""
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding="latin-1")
    lines = []
    for line in p.stderr:
        lines.append(line.rstrip("\n"))
        if len(lines) > n:
            p.kill()
            p.wait()
            p.stdout.close()
            p.stderr.close()
            return None, lines[:n], None
    out = p.stdout.read()
    p.wait()
    p.stdout.close()
    p.stderr.close()
    return out, lines, p.returncode


def c_trace(program):
    out, lines, status = first_lines([os.path.join(C, "vm"), "-t", program], STEPS)
    steps, rest = [], []
    for line in lines:
        m = re.match(r"\s*(\d+)\s+(\d+)  (\S+)(.*)$", line)
        if not m:
            rest.append(line)
            continue
        words = m.group(4).split()
        words = words[OPERANDS.get(m.group(3), 0):]
        steps.append((int(m.group(2)), " ".join(words)))
    return steps[:STEPS], out, rest, status


def cpu_trace(folder, program):
    code = vmfile.read(program)
    hexfile = program + ".hex"
    with open(hexfile, "w") as f:
        for word in code:
            f.write("%08x\n" % (word & 0xffffffff))
    out, lines, _ = first_lines(["vvp", "-n", os.path.join(folder, "sim"), "+program=" + hexfile,
                                 "+length=%d" % len(code), "+trace", "+limit=%d" % STEPS],
                                STEPS + 10)
    steps, rest, status = [], [], None
    for line in lines:
        m = re.match(r"(\d+) (\d+)(.*)$", line)
        if m:
            steps.append((int(m.group(2)), m.group(3).strip()))
        elif line.startswith("status "):
            status = int(line.split()[1])
        elif not line.startswith(("cycles ", "stopped after")):
            rest.append(line)
    if status == 3:                     # stopped at the limit
        out, rest, status = None, [], None
    return steps[:STEPS], out, rest, status


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    subprocess.run(["make", "-s", "-C", C, "vm"], check=True)
    with tempfile.TemporaryDirectory() as w:
        folder = os.path.join(w, "trace")
        subprocess.run([sys.executable, os.path.join(HERE, "build.py"), "trace", folder],
                       check=True)
        programs = []
        for kind in ["samples", "suite"]:
            for asm in sorted(os.listdir(os.path.join(CHAPTER, kind))):
                if not asm.endswith(".asm"):
                    continue
                text = open(os.path.join(CHAPTER, kind, asm)).read()
                if re.search(r"^\s*[A-Za-z_]*:?\s*(NEW|GETF|SETF|LEN|CALLI)\b|\.word (2[7-9]|3[01])",
                             text, re.M):
                    continue                    # versions 3 and 4: not on this CPU
                vm = os.path.join(w, kind + "-" + asm[:-4] + ".vm")
                r = subprocess.run([sys.executable, os.path.join(CHAPTER, "asm.py"),
                                    os.path.join(CHAPTER, kind, asm), vm], capture_output=True)
                if r.returncode == 0:
                    programs.append(vm)
        fuzz = os.path.join(w, "fuzz")
        subprocess.run([sys.executable, FUZZ, "1", str(count), fuzz], check=True)
        programs += [os.path.join(fuzz, p) for p in sorted(os.listdir(fuzz))]
        same = steps = 0
        for program in programs:
            a = c_trace(program)
            b = cpu_trace(folder, program)
            steps += len(a[0])
            if a == b:
                same += 1
                continue
            name = os.path.basename(program)
            k = next((i for i, (x, y) in enumerate(zip(a[0], b[0])) if x != y),
                     min(len(a[0]), len(b[0])))
            print("%s: differs at step %d: C %s, CPU %s" % (
                name, k + 1, a[0][k:k + 1] or a[1:], b[0][k:k + 1] or b[1:]))
        print("%d programs, %d steps compared; %d the same in every step" % (
            len(programs), steps, same))


main()
