#!/usr/bin/env python3
"""
Make opt_more.py, the optimiser with two more rules, for
exercises 20.1 and 20.4, in a folder of their own:

    python3 build.py folder

  -dup           STORE k, LOAD k  ->  DUP, STORE k            (exercise 1)
  -dup-anywhere  the same, also inside functions: wrong, see below
  -assoc         PUSH a, MUL, PUSH b, MUL  ->  PUSH a*b, MUL  (exercise 4)

Both rules are used only where the stack's depth is known and nothing in
the window can trap, as the chapter's rules are. DUP, STORE k takes the
stack one place higher than STORE k, LOAD k ever does, so it must not make
a stack overflow that was not there. The analysis knows the depth within a
function's frame, but the limit is on the whole stack, all frames together,
and that is known only in the main program, below every call: so -dup is
used only there, as the chapter's folding and PUSH a, DROP are.
-dup-anywhere drops that condition, to measure it and to show that it is
wrong.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)


def patch(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def main():
    folder = sys.argv[1]
    o = open(os.path.join(CHAPTER, "opt.py")).read()
    o = patch(o, """        out.append(item)
        i += 1
    items[:] = out
    return changed""", """        if (RULES & {"dup", "dup-anywhere"} and known and item.op == "STORE"
                and plain(i + 1) and items[i + 1].op == "LOAD"
                and items[i + 1].operands == item.operands
                and depth[i] + 1 <= flow.REGISTERS
                and ("dup-anywhere" in RULES or item.main)):
            out.append(Item(item.labels, "DUP", []))
            out.append(Item([], "STORE", item.operands))
            removed["store, load made dup, store"] += 1
            i += 2
            changed = True
            continue
        if ("assoc" in RULES and known and item.op == "PUSH" and all(plain(i + k) for k in (1, 2, 3))
                and items[i + 1].op == "MUL" and items[i + 2].op == "PUSH"
                and items[i + 3].op == "MUL"
                and number(item.operands[0]) is not None
                and number(items[i + 2].operands[0]) is not None):
            a, b = number(item.operands[0]), number(items[i + 2].operands[0])
            out.append(Item(item.labels, "PUSH", [str(fold("MUL", a, b))]))
            out.append(items[i + 1])
            removed["multiplications joined"] += 2
            i += 4
            changed = True
            continue
        out.append(item)
        i += 1
    items[:] = out
    return changed


RULES = set()""")
    o = patch(o, """    stats = args[:1] == ["-s"]
    if stats:
        args = args[1:]""", """    while args and args[0] in ("-dup", "-dup-anywhere", "-assoc"):
        RULES.add(args.pop(0)[1:])
    stats = args[:1] == ["-s"]
    if stats:
        args = args[1:]""")
    o = patch(o, 'sys.exit("usage: opt.py [-s] program.asm > optimised.asm")',
              'sys.exit("usage: opt_more.py [-dup | -dup-anywhere] [-assoc] [-s] program.asm")')
    open(os.path.join(folder, "opt_more.py"), "w").write(o)
    for name in ["asm.py", "flow.py", "isa.py", "vmfile.py"]:
        shutil.copy(os.path.join(CHAPTER, name), folder)


main()
