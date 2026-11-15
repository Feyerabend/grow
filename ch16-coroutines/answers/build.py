#!/usr/bin/env python3
"""
Exercise 16.1: the coroutine machine keeping each coroutine's saved block,
and using it again at the next YIELD when it is exactly the size needed.
Not "big enough": RESUME works out how many frames a saved block holds from
its length, so a block with room to spare would need that count kept
somewhere else, a change to the specification's layout of a coroutine.

The block stays in the coroutine while it runs, where the machine as it is
clears it. So whatever was in it stays reachable until the next YIELD
overwrites it: the collector keeps it, garbage or not.

    usage: python3 build.py > vm_keep.c
"""

import os

s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vm.c")).read()


def change(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)


change("    heap[b + HEADER + CO_SAVED] = integer(0);\n", "")
change("""        saved = allocate(n + 2 * nf);   /* may collect: nothing is off the stack yet */""",
       """        saved = heap[l->co.n + HEADER + CO_SAVED];
        if (!saved.is_ref || heap[saved.n].n != n + 2 * nf)
            saved = allocate(n + 2 * nf);   /* may collect: nothing is off the stack yet */""")
print(s, end="")
