#!/usr/bin/env python3
"""
Time chapter 18's three builds and this folder's three more, on the four
benchmarks, best of seven, for exercises 18.2 and 18.4 to 18.6.

    python3 times.py [-O0 | -O2]

Run from this folder. Every build is compiled here, in a temporary folder,
at the level asked for, -O2 if none: vm-switch, vm-goto and vm-threaded
from ../vm.c, and vm-spread, vm-indirect and vm-subroutine from what
build.py makes. Times are not kept in .out files: they belong to one
computer on one day.
"""

import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
CC = os.environ.get("CC", "cc")
RUNS = 7
BENCHMARKS = ["fib", "loop", "sieve", "closures"]
BUILDS = [("switch", "vm.c"), ("goto", "vm.c"), ("spread", "vm_more.c"),
          ("threaded", "vm.c"), ("indirect", "vm_more.c"),
          ("subroutine", "vm_more.c")]


def best(command):
    times = []
    for _ in range(RUNS):
        start = time.perf_counter()
        subprocess.run(command, stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times)


def main():
    level = sys.argv[1] if len(sys.argv) > 1 else "-O2"
    for b in BENCHMARKS:
        subprocess.run(["make", "-s", "-C", CHAPTER, "bench/%s.vm" % b], check=True)
    with tempfile.TemporaryDirectory() as folder:
        more = os.path.join(folder, "vm_more.c")
        with open(more, "w") as out:
            subprocess.run([sys.executable, os.path.join(HERE, "build.py")], stdout=out,
                           check=True)
        binaries = []
        for name, source in BUILDS:
            path = os.path.join(CHAPTER, source) if source == "vm.c" else more
            binary = os.path.join(folder, "vm-" + name)
            subprocess.run([CC, "-std=gnu99", level, "-I", CHAPTER,
                            "-DDISPATCH=" + name.upper(), "-o", binary, path], check=True)
            binaries.append(binary)
        print("best of %d runs, %s %s, in ms" % (RUNS, CC, level))
        print("%-9s" % "" + "".join("%11s" % n for n, _ in BUILDS))
        for b in BENCHMARKS:
            program = os.path.join(CHAPTER, "bench", b + ".vm")
            print("%-9s" % b + "".join("%11.0f" % (best([x, program]) * 1000)
                                       for x in binaries))


main()
