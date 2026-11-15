#!/usr/bin/env python3
"""
Exercise 9.6: how many of fuzz.py's expressions a wrong parser gets wrong, each
one counted, though a trap stops the machine. The program is run as usual; when
it traps, the trap's address says which expression trapped, since a label is
put before each one; that one is counted wrong, and a program of the
expressions after it is run next. So there are as many runs as traps, plus
one, not one run for each expression. The count is checked against
measure/mistakes.py's, which works out each expression in Python.

    usage: python3 onebyone.py         (after make vm)
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH09 = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(CH09, "measure"))
sys.path.insert(0, CH09)
import asm                                      # noqa: E402
import expr                                     # noqa: E402
import fuzz                                     # noqa: E402
import mistakes                                 # noqa: E402
import vmfile                                   # noqa: E402


def program(trees):
    out = []
    for k, node in enumerate(trees):
        out.append(f"s{k}:")                     # where expression k begins
        expr.generate(node, out)
        out.append("        PRINT")
    out.append("        HALT")
    return "\n".join(out) + "\n"


def wrong_one_by_one(trees, want, work):
    wrong, runs, k = 0, 0, 0
    while k < len(trees):
        a = asm.Assembler("p.asm")
        _, code = a.assemble(program(trees[k:]))
        path = os.path.join(work, "p.vm")
        vmfile.write(path, code)
        r = subprocess.run([os.path.join(CH09, "vm"), path], capture_output=True, text=True)
        runs += 1
        got = r.stdout.splitlines()
        wrong += sum(g != w for g, w in zip(got, want[k:]))
        if r.returncode == 0:
            break
        at = int(re.search(r" at (\d+)", r.stderr).group(1))
        starts = sorted((address, int(name[1:])) for name, address in a.labels.items())
        trapped = max(j for address, j in starts if address <= at)
        wrong += 1                               # the expression that trapped
        k += trapped + 1
    return wrong, runs


def main():
    with tempfile.TemporaryDirectory() as work:
        p, e = os.path.join(work, "f.expr"), os.path.join(work, "f.out")
        fuzz.main.__globals__["sys"].argv = ["fuzz.py", "1", "500", p, e]
        fuzz.main()
        source, want = open(p).read(), open(e).read().splitlines()
        expr.Parser.signed = mistakes.signed
        print("500 expressions, seed 1: wrong one by one on the machine, runs, "
              "and as measure/mistakes.py works it out")
        for name, change in mistakes.MISTAKES:
            for method, f in change.items():
                setattr(expr.Parser, method, f)
            trees = expr.parse(expr.scan(source))
            wrong, runs = wrong_one_by_one(trees, want, work)
            python = mistakes.one_by_one(source, want)
            for method, f in mistakes.RIGHT.items():
                setattr(expr.Parser, method, f)
            print(f"  {name:36} {wrong:4} {runs:4} {python:6}")


if __name__ == "__main__":
    main()
