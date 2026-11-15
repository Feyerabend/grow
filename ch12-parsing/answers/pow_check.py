#!/usr/bin/env python3
"""
Exercise 12.1: ^ in all three parsers. Each copy must build the same tree for
the same expressions, and how many lines of each parser had to change is
counted, the shared scanner apart.

    usage: python3 pow_check.py
"""

import difflib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import common_pow                               # noqa: E402
import combinators_pow                          # noqa: E402
import descent_pow                              # noqa: E402
import pratt_pow                                # noqa: E402

TESTS = ["2 ^ 3 ^ 2;", "-2 ^ 2;", "2 * 3 ^ 2;", "2 ^ -1;", "(2 ^ 3) ^ 2;", "1 + 2 ^ 3 * 4 < 5;"]

for text in TESTS:
    tokens = common_pow.scan(text)
    trees = {name: common_pow.sexp(m.parse(tokens)[0])
             for name, m in (("descent", descent_pow), ("pratt", pratt_pow), ("combinators", combinators_pow))}
    assert len(set(trees.values())) == 1, (text, trees)
    print(f"{text:22} {trees['descent']}")

print("\nlines changed, not counting the import of common_pow:")
for name in ("descent", "pratt", "combinators", "common"):
    old = open(os.path.join(HERE, "..", name + ".py")).read().splitlines()
    new = open(os.path.join(HERE, name + "_pow.py")).read().splitlines()
    removed = added = 0
    for line in difflib.unified_diff(old, new, lineterm="", n=0):
        if line.startswith(("---", "+++", "@@")) or "import" in line:
            continue                            # the import only points at common_pow
        removed += line.startswith("-")
        added += line.startswith("+")
    print(f"  {name:12} {removed} removed, {added} added" + ("  (the scanner, shared)" if name == "common" else ""))
