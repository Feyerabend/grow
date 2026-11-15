#!/usr/bin/env python3
"""
Exercise 12.3: the combinator parser's messages, before and after one label,
"an expression", given to comparison. Then measure/errors.py's 2000 programs
with one token wrong: does the label move any message to another place?

    usage: python3 label_check.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import combinators                              # noqa: E402
import combinators_label                        # noqa: E402
import common                                   # noqa: E402

for text in [";", "1 + ;", "(;", "1 < ;", "1 2;", "(1 + 2;", "- ;", "1 * (2 + );"]:
    print(text)
    for name, m in (("before", combinators), ("after", combinators_label)):
        try:
            m.parse(common.scan(text))
        except common.CompileError as e:
            print(f"  {name:6} {e.line}:{e.col}: {e}")
