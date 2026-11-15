#!/usr/bin/env python3
"""
How fast is each parser, how many Python calls does it make, and how deep can
an expression nest before it gives up?

Speed: fuzz.py's random expressions (seed 3, as make test, but 5000 of them),
scanned once; each parser builds the trees, the best of five runs. Calls: the
same, under cProfile, which counts every Python function call. Depth: ((((1))))
nested deeper one step at a time, until Python's limit of 1000 calls stops the
parser with a RecursionError.

    usage: python3 measure/speed.py       (run in code/ch12-parsing)
"""

import cProfile
import os
import pstats
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.getcwd())
import combinators                               # noqa: E402
import common                                    # noqa: E402
import descent                                   # noqa: E402
import pratt                                     # noqa: E402

PARSERS = [("descent", descent), ("pratt", pratt), ("combinators", combinators)]


def calls(parser, tokens):
    profile = cProfile.Profile()
    profile.enable()
    parser.parse(tokens)
    profile.disable()
    return pstats.Stats(profile).total_calls


def deepest(parser):
    lo, hi = 1, 2000
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        try:
            parser.parse(common.scan("(" * mid + "1" + ")" * mid + ";"))
            lo = mid
        except RecursionError:
            hi = mid
    return lo


def main():
    with tempfile.TemporaryDirectory() as work:
        p, e = os.path.join(work, "f.expr"), os.path.join(work, "f.out")
        subprocess.run([sys.executable, "fuzz.py", "3", "5000", p, e], check=True)
        tokens = common.scan(open(p).read())
    print(f"{len(tokens)} tokens\n")
    print(f"  {'parser':12} {'best of 5':>9} {'calls':>10} {'calls a token':>14} {'deepest':>8}")
    for name, parser in PARSERS:
        best = float("inf")
        for _ in range(5):
            t = time.perf_counter()
            parser.parse(tokens)
            best = min(best, time.perf_counter() - t)
        n = calls(parser, tokens)
        print(f"  {name:12} {best * 1000:7.0f} ms {n:10} {n / len(tokens):14.1f} {deepest(parser):8}")


if __name__ == "__main__":
    main()
