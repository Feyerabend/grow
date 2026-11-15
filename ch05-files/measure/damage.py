#!/usr/bin/env python3
"""
What a damaged program file does. A good .vm file has one byte changed, to a
random value, at a random place, and the machine is run on it. Done many times
for each sample, and the outcomes counted: refused by the loader, a trap, the
same output as the good file, other output, or still running after a second.

    usage: python3 measure/damage.py [count] [seed]     (from ch05-files)
"""

import collections
import os
import random
import subprocess
import sys
import tempfile

SAMPLES = ["gcd", "fib", "primes"]


def run(exe, path):
    try:
        r = subprocess.run([exe, path], capture_output=True, text=True, timeout=1)
    except subprocess.TimeoutExpired:
        return None, "still running after a second"
    return r, None


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    with tempfile.TemporaryDirectory() as folder:
        exe = os.path.join(folder, "vm")
        subprocess.run(["cc", "-std=c99", "-O1", "-w", "-o", exe, "vm.c"], check=True)
        totals = collections.Counter()
        where = collections.Counter()
        for name in SAMPLES:
            good = os.path.join(folder, name + ".vm")
            subprocess.run([sys.executable, "tobin.py", f"samples/{name}.txt", good], check=True)
            data = open(good, "rb").read()
            expected = subprocess.run([exe, good], capture_output=True, text=True).stdout
            bad = os.path.join(folder, "bad.vm")
            for _ in range(count):
                i = rng.randrange(len(data))
                v = rng.randrange(256)
                while v == data[i]:
                    v = rng.randrange(256)
                with open(bad, "wb") as f:
                    f.write(data[:i] + bytes([v]) + data[i + 1:])
                r, other = run(exe, bad)
                if other:
                    kind = other
                elif r.returncode == 2:
                    kind = "refused by the loader"
                elif r.returncode == 1:
                    kind = "trapped"
                elif r.stdout == expected:
                    kind = "ran, same output"
                else:
                    kind = "ran, other output"
                totals[kind] += 1
                where[(kind, "header" if i < 8 else "code")] += 1
            print(f"{name}: {len(data)} bytes, {count} damaged copies")
    n = count * len(SAMPLES)
    print(f"\nall {n}:")
    for kind, k in totals.most_common():
        print(f"  {k:>5}  {100 * k / n:4.1f}%  {kind}   "
              f"(header {where[(kind, 'header')]}, code {where[(kind, 'code')]})")


if __name__ == "__main__":
    main()
