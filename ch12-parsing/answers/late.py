#!/usr/bin/env python3
"""
Exercise 12.5: one-token mistakes that every parser reports later than where
they were made. Each program is right but for one token; the place the token
belongs is given, and where each of the four parsers says the mistake is.

    usage: python3 late.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import combinators                              # noqa: E402
import common                                   # noqa: E402
import descent                                  # noqa: E402
import pratt                                    # noqa: E402
import shunting                                 # noqa: E402

CASES = [
    ("(1 + 2) * 3;", "(1 + 2 * 3;", "the ) deleted, after the 2: column 7"),
    ("(1 + 2) * 3;", "((1 + 2) * 3;", "a ( doubled, at the start: column 1"),
    ("1 + 2;", "1 + 2 3;", "the + deleted: column 7, before the 3"),
]

for right, wrong, where in CASES:
    print(f"{wrong:16} {where}")
    for name, m in (("descent", descent), ("pratt", pratt), ("combinators", combinators),
                    ("shunting", shunting)):
        try:
            m.parse(common.scan(wrong))
            print(f"  {name:12} accepted it")
        except common.CompileError as e:
            print(f"  {name:12} {e.line}:{e.col}: {e}")
