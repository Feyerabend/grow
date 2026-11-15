#!/usr/bin/env python3
"""
Exercise 22.5: vm2c.py's code with "start =" only before instructions that
can trap, and what that changes in the machine code.

    python3 lean.py [benchmark]

In a verified program, DROP, SWAP, ROT, STORE, JMP, JZ, EQ and HALT cannot
trap: their pops are checked by the verifier, and they push no more than
they pop. Their "start =" is taken out of vm2c.py's code. Both versions are
compiled to arm64 assembly with cc -O2, and the stores to start counted, in
all of run() and in the loop of the benchmark (loop unless told): the
stretch of run() from the label of the loop's first instruction to the jump
back to it.
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
sys.path.insert(0, CHAPTER)
import isa  # noqa: E402
import vm2c  # noqa: E402
import vmfile  # noqa: E402

CANNOT_TRAP = {"DROP", "SWAP", "ROT", "STORE", "JMP", "JZ", "EQ", "HALT"}


def lean(code, text):
    out = []
    for line in text.splitlines():
        m = re.match(r"A(\d+): start = \d+;$", line)
        if m:
            a = int(m.group(1))
            if a < len(code) and isa.BY_CODE.get(code[a], ("",))[0] in CANNOT_TRAP:
                line = "A%d:;" % a
        out.append(line)
    return "\n".join(out) + "\n"


def assembly(folder, name, text):
    """arm64 assembly from cc -O2. -mno-global-merge keeps start a symbol of
    its own, so that its stores can be found by name."""
    c = os.path.join(folder, name + ".c")
    out = os.path.join(folder, name + ".s")
    open(c, "w").write(text)
    subprocess.run(["cc", "-O2", "-w", "-mno-global-merge", "-I", CHAPTER, "-S", "-o", out, c],
                   check=True)
    return open(out).read()


def instructions(lines):
    return [l for l in lines if re.match(r"\t[a-z]", l)]


def parts(asm):
    """main(), into which run() is put inline; and in it the innermost loop:
    from the line Clang marks as a loop's header to the branch back to it."""
    body = asm[asm.index("_main:"):]
    body = body[:body.index(".cfi_endproc")].splitlines()
    headers = [k for k, l in enumerate(body) if "Inner Loop Header" in l]
    loop = []
    if headers:
        k = headers[-1]
        label = body[k].split(":")[0]
        for j in range(k, len(body)):
            loop.append(body[j])
            if re.match(r"\tb(\.\w+)?\s+%s$" % re.escape(label), body[j]):
                break
    return instructions(body), instructions(loop)


def stores(lines):
    return [l for l in lines if l.startswith("\tstr") and "_start@PAGEOFF" in l]


def main():
    b = sys.argv[1] if len(sys.argv) > 1 else "loop"
    subprocess.run(["make", "-s", "-C", CHAPTER, "bench/%s.vm" % b], check=True)
    code = vmfile.read(os.path.join(CHAPTER, "bench", b + ".vm"))
    plain = vm2c.compile_program(code, False)
    with tempfile.TemporaryDirectory() as w:
        loops = []
        for name, text in [("as vm2c.py writes it", plain), ("start only where it can trap",
                                                              lean(code, plain))]:
            whole, loop = parts(assembly(w, name[:2], text))
            loops.append(loop)
            print("%s: %d \"start =\" in the C" % (name, text.count("start = ")))
            print("  run(): %d instructions, %d of them stores to start" % (
                len(whole), len(stores(whole))))
            print("  its innermost loop: %d instructions, %d of them stores to start" % (
                len(loop), len(stores(loop))))
        def unnamed(loop):
            return [re.sub(r"\b[xw]\d+\b", "r", l) for l in loop]
        print("the two loops are %s" % (
            "the same, instruction for instruction" if loops[0] == loops[1] else
            "the same but for which registers they use" if unnamed(loops[0]) == unnamed(loops[1])
            else "different"))


main()
