#!/usr/bin/env python3
"""
Count the indirect jumps and indirect calls in each build's assembly, at
-O2 and at -O0, for exercises 18.2, 18.4 and 18.5: as measure/bench.py
counts them, but for all six builds. arm64 only.

    python3 jumps.py
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
CC = os.environ.get("CC", "cc")
BUILDS = [("switch", "vm.c"), ("goto", "vm.c"), ("spread", "vm_more.c"),
          ("threaded", "vm.c"), ("indirect", "vm_more.c"),
          ("subroutine", "vm_more.c")]


def main():
    print("%-6s" % "" + "".join("%12s" % n for n, _ in BUILDS))
    with tempfile.TemporaryDirectory() as folder:
        more = os.path.join(folder, "vm_more.c")
        with open(more, "w") as out:
            subprocess.run([sys.executable, os.path.join(HERE, "build.py")], stdout=out,
                           check=True)
        for level in ["-O2", "-O0"]:
            cells = []
            for name, source in BUILDS:
                path = os.path.join(CHAPTER, source) if source == "vm.c" else more
                out = os.path.join(folder, name + ".s")
                subprocess.run([CC, "-std=gnu99", level, "-I", CHAPTER,
                                "-DDISPATCH=" + name.upper(), "-S", "-o", out, path],
                               check=True)
                text = open(out).read()
                br = len(re.findall(r"\tbr\tx\d+", text))
                blr = len(re.findall(r"\tblr\tx\d+", text))
                cells.append("%d" % br + (" + %d call" % blr if blr else ""))
            print("%-6s" % level + "".join("%12s" % c for c in cells))
    print("(indirect jumps, br; and indirect calls, blr)")


main()
