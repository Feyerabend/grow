#!/usr/bin/env python3
"""
What does the run-time library cost? PRINT X; calls print_number, written in
assembly, where PRINT X is one instruction. For a few numbers, count the
instructions the machine executes for each, with ./vm -t, which traces one line
per instruction: the program LET X = n, PRINT X (or PRINT X;), less the same
program without the PRINT.

    usage: python3 measure/library.py     (run in code/ch11-basal, after make vm)
"""

import os
import subprocess
import sys

NUMBERS = [0, 7, 42, 12345, 2147483647, -1, -2147483648]


def executed(source):
    with open("_lib.bas", "w") as f:
        f.write(source)
    asm = subprocess.run([sys.executable, "basal.py", "_lib.bas"], capture_output=True,
                         text=True, check=True).stdout
    with open("_lib.asm", "w") as f:
        f.write(asm)
    subprocess.run([sys.executable, "asm.py", "_lib.asm", "_lib.vm"], check=True)
    r = subprocess.run(["./vm", "-t", "_lib.vm"], capture_output=True, text=True)
    for name in ("_lib.bas", "_lib.asm", "_lib.vm"):
        os.remove(name)
    return len(r.stderr.splitlines()), r.stdout


def main():
    print(f"{'number':>12}  PRINT X  PRINT X;   output")
    for n in NUMBERS:
        let = f"LET X = {n}\n" if n >= 0 else f"LET X = 0 - {-n - 1} - 1\n"
        base, _ = executed(let)
        plain, out1 = executed(let + "PRINT X\n")
        semi, out2 = executed(let + "PRINT X;\n")
        assert out1 == out2 + "\n", (out1, out2)
        print(f"{n:12}  {plain - base:7}  {semi - base:8}   {out2}")


if __name__ == "__main__":
    main()
