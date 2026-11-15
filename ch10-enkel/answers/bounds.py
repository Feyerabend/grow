#!/usr/bin/env python3
"""
Exercise 10.5: the six-instruction check refuses what the ten-instruction one
refuses. For an array of 5, every index from -3 to 7, and the two extremes of
32 bits, is read through a computed index, with both checks; each must print
the element when 0 <= i < 5, and trap otherwise.

    usage: python3 bounds.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import measure_more as mm                       # noqa: E402

import enkel                                    # noqa: E402
import asm                                      # noqa: E402
import vm                                       # noqa: E402
import cost                                     # noqa: E402

PROGRAM = """array A:5;
var i;
begin
    A.0 is 10; A.1 is 11; A.2 is 12; A.3 is 13; A.4 is 14;
    i is {i};
    print A.(i)
end.
"""


def outcome(generator, i):
    text = PROGRAM.format(i=i)
    program = enkel.Parser(enkel.scan(text)).program()
    enkel.Resolver(program).resolve()
    g = generator(text.splitlines(), True)
    a = asm.Assembler("bounds")
    _, code = a.assemble(g.program(program))
    m = mm.Machine(code)
    try:
        status = vm.run(m, False)
    except SystemExit as e:
        status = e.code
    printed = m.out.getvalue().decode().strip()
    return printed if status == 0 else "trap"


for i in [-2147483647, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 2147483647]:
    ten, six = outcome(cost.Tagging, i), outcome(mm.Short, i)
    print(f"{i:>11}: ten {ten:>4}, six {six:>4}" + ("" if ten == six else "   DIFFERENT"))
