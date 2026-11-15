#!/usr/bin/env python3
"""
The copies the translator's second stage leaves, for exercise 19.1.

    python3 copies.py

Run from this folder, after make test in the chapter's folder. For fib,
the code before and after stage two. Then, for the three benchmarks and
the twelve samples, every MOV left, sorted by the first instruction after
it that is not a MOV or MOVI: a CALL (arguments put into the window), a
SWAPR or ROTR (which stage two does not look through), a JMP (a value
carried to where two paths meet), or something else.
"""

import collections
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)


def listing(path, *flags):
    run = subprocess.run([sys.executable, "translate.py", "-l", *flags, path, "/dev/null"],
                         cwd=CHAPTER, stdout=subprocess.PIPE, text=True, check=True)
    return [line for line in run.stdout.splitlines() if line.startswith(" ")]


def name(line):
    return line.split()[0]


def main():
    naive, full = listing("bench/fib.vm", "-naive"), listing("bench/fib.vm")
    for title, lines in [("fib, stage one", naive), ("fib, stage two", full)]:
        kinds = collections.Counter(name(x) for x in lines)
        print("%s: %d instructions, %d MOV, %d MOVI" % (
            title, len(lines), kinds["MOV"], kinds["MOVI"]))
    print()
    paths = ["bench/%s.vm" % b for b in ["fib", "loop", "sieve"]]
    paths += sorted(os.path.relpath(p, CHAPTER)
                    for p in glob.glob(os.path.join(CHAPTER, "samples", "*.vm")))
    total = collections.Counter()
    for path in paths:
        lines = listing(path)
        kinds = collections.Counter()
        for k, line in enumerate(lines):
            if name(line) != "MOV":
                continue
            j = k + 1
            while j < len(lines) and name(lines[j]) in ("MOV", "MOVI"):
                j += 1
            after = name(lines[j]) if j < len(lines) else "end"
            kind = {"CALL": "call", "SWAPR": "swap", "ROTR": "swap",
                    "JMP": "join"}.get(after, "other")
            kinds[kind] += 1
        total += kinds
        print("%-32s %s" % (os.path.basename(path),
                            ", ".join("%s %d" % (k, kinds[k]) for k in sorted(kinds)) or "none"))
    print("%-32s %s" % ("all", ", ".join("%s %d" % (k, total[k]) for k in sorted(total))))


main()
