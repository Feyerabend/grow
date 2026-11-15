#!/usr/bin/env python3
"""
Exercise 17.1: the thread machine with INC, code 38: pop a number, the address
of a place in memory; add 1 to what is there, wrapped, in one instruction.

    usage: python3 build.py > vm_inc.c
"""

import os

s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vm.c")).read()


def change(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)


change("    CORO, RESUME, YIELD, COSTATE, SLICE, TAS,\n    NOPS",
       "    CORO, RESUME, YIELD, COSTATE, SLICE, TAS, INC,\n    NOPS")
change('    "CORO", "RESUME", "YIELD", "COSTATE", "SLICE", "TAS"\n',
       '    "CORO", "RESUME", "YIELD", "COSTATE", "SLICE", "TAS", "INC"\n')
change("    case TAS:\n", """    case INC:
        a = number(pop());
        if (a < 0 || a >= MEMORY_SIZE)
            trap("no such memory address");
        memory[a] = integer(wrap_add(number(memory[a]), 1));
        break;
    case TAS:
""")
print(s, end="")
