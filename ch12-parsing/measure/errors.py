#!/usr/bin/env python3
"""
Do the three parsers find a mistake in the same place?

Take fuzz.py's random expressions (seed 3), and make 2000 wrong programs, each
one expression with one token changed: deleted, doubled, or replaced by another
token. Every parser must reject it (a change can leave a right expression; those
are counted and left out). For each wrong program, compare where each parser
says the mistake is, and the first words of what it says.

    usage: python3 measure/errors.py       (run in code/ch12-parsing)
"""

import collections
import os
import random
import subprocess
import sys
import tempfile

sys.path.insert(0, os.getcwd())
import combinators                               # noqa: E402
import common                                    # noqa: E402
import descent                                   # noqa: E402
import pratt                                     # noqa: E402

PARSERS = [("descent", descent), ("pratt", pratt), ("combinators", combinators)]
KINDS = list("+-*/%()<=;") + ["7"]


def where(parser, text):
    try:
        parser.parse(common.scan(text))
        return None
    except common.CompileError as e:
        return (e.line, e.col), str(e)


def main():
    with tempfile.TemporaryDirectory() as work:
        p, e = os.path.join(work, "f.expr"), os.path.join(work, "f.out")
        subprocess.run([sys.executable, "fuzz.py", "3", "500", p, e], check=True)
        lines = open(p).read().splitlines()
    rng = random.Random(1)
    tally = collections.Counter()
    for _ in range(2000):
        line = rng.choice(lines)
        words = line.replace("(", "( ").replace(")", " )").replace(";", " ;").split()
        k = rng.randrange(len(words))
        how = rng.choice(["delete", "double", "replace"])
        if how == "delete":
            words = words[:k] + words[k + 1:]
        elif how == "double":
            words = words[:k + 1] + words[k:]
            k += 1                                   # the copy is the change
        else:
            words = words[:k] + [rng.choice(KINDS)] + words[k + 1:]
        text = " ".join(words) + "\n"
        changed = len(" ".join(words[:k])) + (1 if k else 0) + 1     # column of word k
        results = [where(parser, text) for _, parser in PARSERS]
        if all(r is None for r in results):
            tally["still right"] += 1
            continue
        assert all(r is not None for r in results), text
        places = {r[0] for r in results}
        tally["wrong"] += 1
        tally["same place, all three" if len(places) == 1 else "places differ"] += 1
        place = results[0][0]                       # (line, column); the program is line 1
        tally["at the change" if place == (1, changed) else
              "after the change" if place > (1, changed) else "before the change"] += 1
        if results[0][1] == results[1][1]:
            tally["descent and pratt, same words"] += 1
    total = tally["wrong"]
    print(f"2000 changed programs: {tally['still right']} still right, {total} wrong\n")
    for key in ("same place, all three", "places differ", "descent and pratt, same words",
                "at the change", "after the change", "before the change"):
        print(f"  {key:32} {tally[key]:5}  {100 * tally[key] / total:5.1f}%")


if __name__ == "__main__":
    main()
