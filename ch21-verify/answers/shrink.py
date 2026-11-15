#!/usr/bin/env python3
"""
Exercise 21.4: shrink failing fuzz programs, by removing instructions one
at a time while the failure remains.

    python3 shrink.py [how-many]

Run from this folder. For three of the verifier's refusals, a broken copy
is made as measure/mutants.py makes it, with the refusal taken out, and
built for testing as fuzz.sh wants it, with sanitizers and a step limit.
The fuzzer's programs from seed 1 are run on it, as fuzz.sh runs them, and
the first few that fail (3 unless told) are shrunk:

  again and again, from the last instruction to the first, take one out;
  if the program still fails in the same way (the same sanitizer's
  complaint, or verified and checked runs that still differ), leave it
  out; stop when a whole pass takes nothing out.

A program is kept as a list of instructions, not of words, so that taking
one out cannot cut another in half; a jump to an instruction that is taken
out goes to the one after it. The smallest found is printed for each.
"""

import os
import struct
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
sys.path.insert(0, CHAPTER)
import isa  # noqa: E402

FUZZ = ["-O1", "-g", "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
        "-DSTEP_LIMIT=20000"]
REFUSALS = ["a pop from a frame with too few values",
            "LOAD of a local the frame does not have",
            "STORE to a local the frame does not have"]
TARGETS = {"JMP", "JZ", "CALL"}


def mutant(folder, message):
    os.makedirs(folder)
    for f in ["loop.h", "ops.h"]:
        os.symlink(os.path.join(CHAPTER, f), os.path.join(folder, f))
    s = open(os.path.join(CHAPTER, "vm.c")).read()
    old = 'ok = refuse(pc, "%s");' % message
    assert s.count(old) == 1, message
    open(os.path.join(folder, "vm.c"), "w").write(s.replace(old, "(void) 0;"))
    vm = os.path.join(folder, "vm-fuzz")
    subprocess.run(["cc", "-std=gnu99", *FUZZ, "-o", vm, os.path.join(folder, "vm.c")],
                   check=True, stderr=subprocess.DEVNULL)
    return vm


def decode(words):
    """Words to [name, operands...]; a jump's target becomes the index of
    the instruction at or after it, or None beyond the end."""
    out, starts, a = [], [], 0
    while a < len(words):
        entry = isa.BY_CODE.get(words[a])
        n = len(entry[1]) if entry else 0
        if entry is None or a + n >= len(words):
            out.append([".word", words[a]])
            starts.append(a)
            a += 1
            continue
        out.append([entry[0]] + words[a + 1:a + 1 + n])
        starts.append(a)
        a += 1 + n
    for ins in out:
        if ins[0] in TARGETS:
            t = ins[1]
            later = [k for k, s in enumerate(starts) if s >= t]
            ins[1] = ("to", later[0] if later else None, t - starts[later[0]] if later else 0)
    return out


def encode(ins):
    starts, a = [], 0
    for i in ins:
        starts.append(a)
        a += len(i) if i[0] != ".word" else 1
    words = []
    for i in ins:
        if i[0] == ".word":
            words.append(i[1])
            continue
        ops = []
        for x in i[1:]:
            if isinstance(x, tuple):
                k, off = x[1], x[2]
                ops.append(starts[k] + off if k is not None else a + 5)
            else:
                ops.append(x)
        words += [isa.BY_NAME[i[0]][0]] + ops
    return words


def without(ins, k):
    out = []
    for j, i in enumerate(ins):
        if j == k:
            continue
        i = list(i)
        for p, x in enumerate(i):
            if isinstance(x, tuple) and x[1] is not None:
                t = x[1] if x[1] < k else (x[1] - 1 if x[1] > k else x[1])
                if x[1] == k:
                    t = k if k < len(ins) - 1 else None
                    x = ("to", t, 0)
                else:
                    x = ("to", t, x[2])
                i[p] = x
        out.append(i)
    return out


def write(path, words):
    with open(path, "wb") as f:
        f.write(b"SVM\x01" + struct.pack("<i", len(words)) + struct.pack("<%di" % len(words),
                                                                         *words))


def failure(vm, path):
    """None if the verified and checked runs agree; else what went wrong."""
    a = subprocess.run([vm, path], capture_output=True)
    c = subprocess.run([vm, "-C", path], capture_output=True)
    both = a.stdout + a.stderr + c.stdout + c.stderr
    if b"runtime error" in both or b"Sanitizer" in both:
        for line in both.decode(errors="replace").splitlines():
            if "runtime error" in line:
                return "sanitizer: " + line.split("runtime error: ", 1)[1]
            if "ERROR: AddressSanitizer" in line:
                return "sanitizer: " + line.split("AddressSanitizer: ", 1)[1].split(" on ")[0]
        return "sanitizer"
    if (a.stdout, a.stderr, a.returncode) != (c.stdout, c.stderr, c.returncode):
        return "verified and checked runs differ"
    return None


def listing(ins):
    starts, a = [], 0
    for i in ins:
        starts.append(a)
        a += len(i) if i[0] != ".word" else 1
    lines = []
    for k, i in enumerate(ins):
        parts = []
        for x in i[1:]:
            if isinstance(x, tuple):
                parts.append(str(starts[x[1]] + x[2]) if x[1] is not None else "beyond the end")
            else:
                parts.append(str(x))
        lines.append("      %3d  %s" % (starts[k], " ".join([i[0]] + parts)))
    return "\n".join(lines)


def main():
    how_many = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    with tempfile.TemporaryDirectory() as w:
        programs = os.path.join(w, "fuzz")
        subprocess.run([sys.executable, os.path.join(CHAPTER, "fuzz.py"), "1", "600", programs],
                       check=True, cwd=CHAPTER)
        trial = os.path.join(w, "t.vm")
        for n, message in enumerate(REFUSALS):
            vm = mutant(os.path.join(w, "m%d" % n), message)
            print("taken out: %s" % message)
            found = 0
            for name in sorted(os.listdir(programs)):
                if found == how_many:
                    break
                path = os.path.join(programs, name)
                kind = failure(vm, path)
                if kind is None:
                    continue
                found += 1
                data = open(path, "rb").read()
                (count,) = struct.unpack("<i", data[4:8])
                ins = decode(list(struct.unpack("<%di" % count, data[8:8 + 4 * count])))
                before, tries = len(ins), 0
                changed = True
                while changed:
                    changed = False
                    for k in range(len(ins) - 1, -1, -1):
                        if k >= len(ins):
                            continue
                        smaller = without(ins, k)
                        write(trial, encode(smaller))
                        tries += 1
                        if failure(vm, trial) == kind:
                            ins = smaller
                            changed = True
                print("  %s: %s" % (name, kind))
                print("    %d instructions, %d after %d tries:" % (before, len(ins), tries))
                print(listing(ins))


if __name__ == "__main__":
    main()
