#!/usr/bin/env python3
"""
Exercise 12.4: the shunting-yard parser beside the other three, as same.py
and measure/speed.py compare them: the same trees on the samples and on
fuzz.py's 5000 expressions; speed and Python calls on those; and how deep
((((1)))) can nest.

    usage: python3 four.py
"""

import cProfile
import glob
import os
import pstats
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CH12 = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
sys.path.insert(0, CH12)
import combinators                              # noqa: E402
import common                                   # noqa: E402
import descent                                  # noqa: E402
import pratt                                    # noqa: E402
import shunting                                 # noqa: E402

PARSERS = [("descent", descent), ("pratt", pratt), ("combinators", combinators), ("shunting", shunting)]


def same(tokens):
    ref = [common.sexp(t) for t in descent.parse(tokens)]
    return all([common.sexp(t) for t in m.parse(tokens)] == ref for _, m in PARSERS)


def deepest(parser, limit):
    lo, hi = 1, limit
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        try:
            parser.parse(common.scan("(" * mid + "1" + ")" * mid + ";"))
            lo = mid
        except RecursionError:
            hi = mid
    return lo


def main():
    for path in sorted(glob.glob(os.path.join(CH12, "samples", "*.expr"))):
        print(f"{os.path.basename(path)}: the same trees from all four: "
              f"{same(common.scan(open(path).read()))}")
    with tempfile.TemporaryDirectory() as work:
        p, e = os.path.join(work, "f.expr"), os.path.join(work, "f.out")
        subprocess.run([sys.executable, os.path.join(CH12, "fuzz.py"), "3", "5000", p, e], check=True)
        tokens = common.scan(open(p).read())
    print(f"fuzz.py's 5000 expressions: the same trees from all four: {same(tokens)}")
    timing = "times" in sys.argv[1:]
    print(f"\n{len(tokens)} tokens")
    for name, parser in PARSERS:
        profile = cProfile.Profile()
        profile.enable()
        parser.parse(tokens)
        profile.disable()
        calls = pstats.Stats(profile).total_calls
        line = f"  {name:12} {calls:9} calls, {calls / len(tokens):5.1f} a token"
        if timing:
            best = min(timed(parser, tokens) for _ in range(5))
            line += f", best of 5 {best * 1000:5.0f} ms"
        depth = deepest(parser, 2000)
        line += f", nests to {depth}" if depth < 1999 else ", nests to 2000 and more"
        print(line)
    deep = 100000
    shunting.parse(common.scan("(" * deep + "1" + ")" * deep + ";"))
    print(f"  shunting parses {deep} parentheses deep")


def timed(parser, tokens):
    t = time.perf_counter()
    parser.parse(tokens)
    return time.perf_counter() - t


if __name__ == "__main__":
    main()
