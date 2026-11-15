#!/usr/bin/env python3
"""
What the checks cost in time. One loop, counting a local down from 50 million
in a frame, runs on chapter 3's machine, which checks nothing, and on chapter
4's, which checks everything. Both are built with cc -O2 and timed, best of
five. The numbers are from one computer and differ from run to run.

    usage: python3 measure/cost.py      (from ch04-traps)
"""

import os
import subprocess
import tempfile
import time

import harness

CH03 = os.path.join(os.path.dirname(__file__), "..", "..", "ch03-calls", "vm.c")
N = 50_000_000
# PUSH N, CALL f 1, PRINT, HALT; f: LOAD 0, JZ end, LOAD 0, PUSH 1, SUB, STORE 0, JMP loop;
# end: PUSH 7, RET.  Addresses: main 0 to 6, f at 7, its loop at 7, end at 20.
LOOP = [1, N, 17, 7, 1, 5, 0,
        15, 0, 7, 20, 15, 0, 1, 1, 3, 16, 0, 6, 7,
        1, 7, 18]
INSTRUCTIONS = 7 * N + 11


def best(exe, path):
    times = []
    for _ in range(5):
        start = time.perf_counter()
        out = subprocess.run([exe, path], capture_output=True, text=True, check=True).stdout
        times.append(time.perf_counter() - start)
    assert out.strip() == "7", out
    return min(times)


def main():
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "loop.txt")
        with open(path, "w") as f:
            f.write(" ".join(map(str, LOOP)))
        plain = harness.build(harness.unchecked(CH03), os.path.join(folder, "ch03"), ["-O2"])
        safe = harness.build(harness.checked("vm.c"), os.path.join(folder, "ch04"), ["-O2"])
        a, b = best(plain, path), best(safe, path)
    print(f"{INSTRUCTIONS} instructions")
    print(f"chapter 3, unchecked: {a:.2f} s, {a / INSTRUCTIONS * 1e9:.2f} ns an instruction")
    print(f"chapter 4, checked:   {b:.2f} s, {b / INSTRUCTIONS * 1e9:.2f} ns an instruction")
    print(f"the checks cost {100 * (b - a) / a:.0f} per cent")


if __name__ == "__main__":
    main()
