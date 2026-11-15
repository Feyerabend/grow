#!/usr/bin/env python3
"""
Exercise 4.4: the random programs of measure/random_programs.py, the same 2000
with the same seed, on chapter 4's machine as it is and with a limit of a
million steps.

    usage: python3 steps.py [count] [seed]
"""

import collections
import os
import random
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "measure"))
import harness                                  # noqa: E402
import random_programs as rp                    # noqa: E402
from run import checked, patch                  # noqa: E402


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rng = random.Random(seed)
    source = open(os.path.join(HERE, "..", "vm.c")).read()
    with tempfile.TemporaryDirectory() as folder:
        plain = harness.build(checked(source), os.path.join(folder, "plain"), ["-O1"])
        limited = harness.build(checked(patch(source, ["steps"])), os.path.join(folder, "limited"), ["-O1"])
        a, b, both = collections.Counter(), collections.Counter(), collections.Counter()
        path = os.path.join(folder, "p.txt")
        for _ in range(count):
            with open(path, "w") as f:
                f.write(" ".join(map(str, rp.program(rng))))
            x, y = rp.outcome(plain, path, True), rp.outcome(limited, path, True)
            a[x] += 1
            b[y] += 1
            if x != y:
                both[(x, y)] += 1
    print(f"{count} random programs, seed {seed}")
    for title, c in (("chapter 4 as it is:", a), ("with a limit of a million steps:", b)):
        print(title)
        for k, n in c.most_common():
            print(f"  {n:>5}  {k}")
    print("the programs whose outcome changed:")
    for (x, y), n in both.most_common():
        print(f"  {n:>5}  {x}  ->  {y}")


if __name__ == "__main__":
    main()
