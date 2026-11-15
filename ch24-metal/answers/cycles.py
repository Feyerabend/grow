#!/usr/bin/env python3
"""
Exercises 24.2, 24.3 and 24.5: clock cycles on the variants of build.py.

    python3 cycles.py

Run from this folder. For every sample, its output is checked on each
variant, and the cycles counted: the chapter's CPU, which takes one for
every instruction; pipe, fetch and execute overlapped; div, with the
divider of 32 cycles; pair, with LOAD and ADD joined, and how often. Then
one DIV alone, on the CPU and on div.
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
VARIANTS = ["pipe", "div", "pair"]


def run(folder, program):
    if folder is None:
        command = [sys.executable, os.path.join(CHAPTER, "vrun.py"), "-c", program]
    else:
        command = [sys.executable, os.path.join(HERE, "vrun_more.py"), folder, "-c", program]
    r = subprocess.run(command, capture_output=True, text=True)
    cycles = int(re.search(r"^cycles (\d+)", r.stderr, re.M).group(1))
    fused = re.search(r"^fused (\d+)", r.stderr, re.M)
    return r.stdout, cycles, int(fused.group(1)) if fused else None


def main():
    subprocess.run(["make", "-s", "-C", CHAPTER, "sim"], check=True)
    with tempfile.TemporaryDirectory() as w:
        for v in VARIANTS:
            subprocess.run([sys.executable, os.path.join(HERE, "build.py"), v,
                            os.path.join(w, v)], check=True)
        print("%-26s %8s %8s %8s %8s %6s" % ("cycles", "cpu", "pipe", "div", "pair", "fused"))
        for asm in sorted(f for f in os.listdir(os.path.join(CHAPTER, "samples"))
                          if f.endswith(".asm")):
            vm = os.path.join(w, asm[:-4] + ".vm")
            subprocess.run([sys.executable, os.path.join(CHAPTER, "asm.py"),
                            os.path.join(CHAPTER, "samples", asm), vm], check=True)
            want = open(os.path.join(CHAPTER, "samples", asm[:-4] + ".out")).read()
            out, base, _ = run(None, vm)
            assert out == want, asm
            cells, fused = [], 0
            for v in VARIANTS:
                out, cycles, f = run(os.path.join(w, v), vm)
                assert out == want, (v, asm)
                cells.append(cycles)
                fused = f if f is not None else fused
            print("%-26s %8d %8d %8d %8d %6d" % (asm[:-4], base, *cells, fused))
        one = os.path.join(w, "div.asm")
        open(one, "w").write("        PUSH -7\n        PUSH 2\n        DIV\n        PRINT\n"
                             "        PUSH -7\n        PUSH 2\n        MOD\n        PRINT\n"
                             "        HALT\n")
        vm = os.path.join(w, "div.vm")
        subprocess.run([sys.executable, os.path.join(CHAPTER, "asm.py"), one, vm], check=True)
        for name, folder in [("cpu", None), ("div", os.path.join(w, "div"))]:
            out, cycles, _ = run(folder, vm)
            print("PUSH -7, PUSH 2, DIV, PRINT, and the same with MOD, HALT, on %s: %d cycles,"
                  " printing %s" % (name, cycles, " ".join(out.split())))


main()
