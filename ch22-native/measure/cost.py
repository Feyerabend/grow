"""Interpreted against native: the time each benchmark takes.

    python3 measure/cost.py

Run from the chapter's folder, after make benchmarks, on a quiet
computer on mains power. Each benchmark runs seven times on chapter
19's interpreter, seven times compiled by vm2c.py as make builds it
(verified, so without the checks the analysis made), and seven times
compiled by vm2c.py -C, with every check. The best of each is kept.
Native code is built with cc -O2, as the Makefile does, or with the
compiler CC names: CC=gcc-16 python3 measure/cost.py, after
make CC=gcc-16 benchmarks, so that every column is GCC's.
"""

import os
import subprocess
import tempfile
import time

RUNS = 7
CC = os.environ.get("CC", "cc")
BENCHMARKS = ["fib", "loop", "sieve", "closures", "enkel-sieve", "basal-loop"]


def best(args):
    times = []
    for _ in range(RUNS):
        start = time.perf_counter()
        subprocess.run(args, stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


def checked(b, work):
    c = os.path.join(work, b + ".c")
    exe = os.path.join(work, b)
    with open(c, "w") as f:
        subprocess.run(["python3", "vm2c.py", "-C", "bench/%s.vm" % b],
                       stdout=f, check=True)
    subprocess.run([CC, "-O2", "-w", "-I.", c, "-o", exe], check=True)
    return exe


with tempfile.TemporaryDirectory() as work:
    print("best of %d runs, milliseconds, %s -O2" % (RUNS, CC))
    print("%-12s %11s %8s %8s %8s" %
          ("", "interpreted", "checked", "native", "faster"))
    for b in BENCHMARKS:
        i = best(["./vm", "bench/%s.vm" % b])
        c = best([checked(b, work)])
        n = best(["./bench/%s" % b])
        print("%-12s %11.0f %8.0f %8.0f %7.1fx" % (b, i, c, n, i / n))
