#!/usr/bin/env python3
"""
What happens to random programs, on a machine without checks and on one with.

Each program is 24 numbers: instructions of chapter 3 (codes 0 to 18) with an
operand where one is due, drawn from 0 to 30, so that jumps and locals often
land somewhere. The same program runs on chapter 3's machine, built with
AddressSanitizer so that a read or write outside its arrays is caught, and on
chapter 4's machine. Each run gets a second at most.

    usage: python3 measure/random_programs.py [count] [seed]   (from ch04-traps)
"""

import collections
import os
import random
import subprocess
import sys
import tempfile

import harness

OPERANDS = {1: 1, 6: 1, 7: 1, 15: 1, 16: 1, 17: 2}     # PUSH, JMP, JZ, LOAD, STORE, CALL
CH03 = os.path.join(os.path.dirname(__file__), "..", "..", "ch03-calls", "vm.c")


def program(rng):
    words = []
    while len(words) < 24:
        op = rng.randrange(19)
        words.append(op)
        words += [rng.randrange(31) for _ in range(OPERANDS.get(op, 0))]
    return words[:24]


def outcome(exe, path, checked):
    try:
        r = subprocess.run([exe, path], capture_output=True, text=True, timeout=1)
    except subprocess.TimeoutExpired:
        return "still running after a second"
    if checked:
        if r.returncode == 0:
            return "halted"
        line = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "?"
        return line.split(" at ")[0]           # "trap: stack underflow"
    if "AddressSanitizer" in r.stderr:
        return "read or wrote outside its memory"
    if r.returncode == 0:
        return "halted"
    return f"died, status {r.returncode}"


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rng = random.Random(seed)
    with tempfile.TemporaryDirectory() as folder:
        plain = harness.build(harness.unchecked(CH03), os.path.join(folder, "ch03"),
                              ["-O1", "-g", "-fsanitize=address"])
        safe = harness.build(harness.checked("vm.c"), os.path.join(folder, "ch04"), ["-O1"])
        a, b = collections.Counter(), collections.Counter()
        both = collections.Counter()
        path = os.path.join(folder, "p.txt")
        for _ in range(count):
            with open(path, "w") as f:
                f.write(" ".join(map(str, program(rng))))
            x, y = outcome(plain, path, False), outcome(safe, path, True)
            a[x] += 1
            b[y] += 1
            both[(x, y)] += 1
    print(f"{count} random programs, seed {seed}")
    print("\nchapter 3, unchecked:")
    for k, n in a.most_common():
        print(f"  {n:>5}  {k}")
    print("\nchapter 4, checked:")
    for k, n in b.most_common():
        print(f"  {n:>5}  {k}")
    print("\nunchecked 'halted', and what the checked machine said of the same program:")
    for (x, y), n in both.most_common():
        if x == "halted" and y != "halted":
            print(f"  {n:>5}  {y}")


if __name__ == "__main__":
    main()
