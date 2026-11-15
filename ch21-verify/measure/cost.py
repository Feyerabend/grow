"""Checked against verified: the time each benchmark takes.

    python3 measure/cost.py

Run from the chapter's folder, after make vm benchmarks, on a quiet
computer. Each benchmark runs seven times with every check (-C) and
seven times verified, and the best of each is kept. Both runs execute
the same instructions; only the checks differ.
"""

import subprocess
import time

RUNS = 7
BENCHMARKS = ["fib", "loop", "sieve", "enkel-sieve", "basal-loop"]


def best(args):
    times = []
    for _ in range(RUNS):
        start = time.perf_counter()
        subprocess.run(args, stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


print("best of %d runs, milliseconds" % RUNS)
print("%-12s %8s %8s %7s" % ("", "checked", "verified", "saved"))
for b in BENCHMARKS:
    c = best(["./vm", "-C", "bench/%s.vm" % b])
    v = best(["./vm", "bench/%s.vm" % b])
    print("%-12s %8.0f %8.0f %6.0f%%" % (b, c, v, 100 * (1 - v / c)))
