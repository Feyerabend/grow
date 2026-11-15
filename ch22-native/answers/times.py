#!/usr/bin/env python3
"""
Exercises 22.1 and 22.2: the benchmarks compiled each way, timed, best of
seven, beside the interpreter and vm2c.py's own code.

    python3 times.py

Run from this folder, on mains power. Built with cc -O2, as the Makefile
builds the benchmarks.
"""

import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
BENCHMARKS = ["fib", "loop", "sieve", "closures", "enkel-sieve", "basal-loop"]
MODES = [("native", []), ("-cache", ["-cache"]), ("-calls", ["-calls"]),
         ("both", ["-cache", "-calls"])]


def best(command):
    times = []
    for _ in range(7):
        start = time.perf_counter()
        subprocess.run(command, stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


def main():
    subprocess.run(["make", "-s", "-C", CHAPTER, "vm", "benchmarks"], check=True)
    with tempfile.TemporaryDirectory() as w:
        print("ms, best of 7  interpreted" + "".join("%9s" % m for m, _ in MODES))
        for b in BENCHMARKS:
            program = os.path.join(CHAPTER, "bench", b + ".vm")
            cells = ["%12.0f" % best([os.path.join(CHAPTER, "vm"), program])]
            for name, mode in MODES:
                c, exe = os.path.join(w, b + ".c"), os.path.join(w, b)
                with open(c, "w") as f:
                    subprocess.run([sys.executable, os.path.join(HERE, "vm2c_more.py"), *mode,
                                    program], stdout=f, check=True)
                subprocess.run(["cc", "-O2", "-w", "-I", CHAPTER, c, "-o", exe], check=True)
                cells.append("%9.0f" % best([exe]))
            print("%-13s" % b + "".join(cells))


main()
