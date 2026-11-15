#!/usr/bin/env python3
"""
Exercise 17.1, measured: measure/race.py's race with INC in place of the
seven instructions that read, add and write, for the same turns, no lock.

    usage: python3 inc.py
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(HERE, "..")
sys.path.insert(0, CH)
sys.path.insert(0, os.path.join(CH, "measure"))
os.chdir(CH)
import isa                                      # noqa: E402

isa.INSTRUCTIONS.append((38, "INC", ()))
isa.BY_NAME["INC"] = (38, ())
isa.BY_CODE[38] = ("INC", ())
import asm                                      # noqa: E402
import race                                     # noqa: E402
import vmfile                                   # noqa: E402

READ_ADD_WRITE = """        PUSH 0
        LOADM
        PUSH 1
        ADD
        PUSH 0
        SWAP
        STOREM
"""

with tempfile.TemporaryDirectory() as work:
    c, exe = os.path.join(work, "vm_inc.c"), os.path.join(work, "vm")
    with open(c, "w") as f:
        subprocess.run([sys.executable, os.path.join(HERE, "build.py")], stdout=f, check=True)
    subprocess.run(["cc", "-std=c99", "-O2", "-w", "-o", exe, c], check=True)
    print("turn   seven instructions      INC")
    for turn in (0, 2, 3, 5, 7, 10, 14, 15, 20, 50, 200):
        row = []
        for text in (race.program(turn, race.NONE),
                     race.program(turn, race.NONE).replace(READ_ADD_WRITE, "        PUSH 0\n        INC\n")):
            a = asm.Assembler("race")
            _, code = a.assemble(text)
            path = os.path.join(work, "p.vm")
            vmfile.write(path, code)
            r = subprocess.run([exe, "-t", path], capture_output=True, text=True, check=True)
            steps = sum(1 for line in r.stderr.splitlines() if re.match(r"\s*\d+\s+\d+\s+[A-Z]", line))
            row.append(f"{r.stdout.strip():>6} {steps:>7}")
        print(f"{turn:>4}   {row[0]}   {row[1]}")
