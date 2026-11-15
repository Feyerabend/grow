#!/usr/bin/env python3
"""
Exercise 12.2: a ? b : c in the Pratt parser, at the loosest precedence.

    usage: python3 cond_check.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import common_cond                              # noqa: E402
import pratt_cond                               # noqa: E402

for text in ["1 < 2 ? 10 : 20;", "1 ? 2 : 3 ? 4 : 5;", "1 ? 2 ? 3 : 4 : 5;",
             "1 + 2 ? 3 * 4 : -5;", "(1 ? 2 : 3) + 4;", "1 ? 2;", "1 ? 2 : ;", "1 : 2;"]:
    try:
        trees = pratt_cond.parse(common_cond.scan(text))
        print(f"{text:22} {common_cond.sexp(trees[0])}")
    except common_cond.CompileError as e:
        print(f"{text:22} {e.line}:{e.col}: {e}")
