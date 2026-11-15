"""Stack machine against register machine: instructions run, time, and size.

    python3 measure/cost.py

Run from the chapter's folder, after make all benchmarks and the
samples' .rvm files (make test makes them all). For the three
benchmarks it counts the instructions run on the stack machine, on the
naive register translation and on the full one (-c), and times each,
best of seven runs. For the twelve samples it counts only. It also
gives the size of each program: instructions, and words without the
address of origin that every register instruction carries for its traps.
"""

import glob
import os
import re
import struct
import subprocess
import sys
import time

sys.path.insert(0, ".")
import isa  # noqa: E402

RUNS = 7
OPERANDS = {code: len(kinds) for code, _, kinds in isa.INSTRUCTIONS}


def steps(machine, program):
    run = subprocess.run([machine, "-c", program], stdout=subprocess.DEVNULL,
                         stderr=subprocess.PIPE, text=True)
    return int(re.search(r"steps: (\d+)", run.stderr).group(1))


def best(machine, program):
    times = []
    for _ in range(RUNS):
        start = time.perf_counter()
        subprocess.run([machine, program], stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


def words(path):
    data = open(path, "rb").read()
    (n,) = struct.unpack("<i", data[4:8])
    return list(struct.unpack("<%di" % n, data[8:8 + 4 * n]))


def stack_size(path):
    code = words(path)
    count, a = 0, 0
    while a < len(code):
        count += 1
        a += 1 + OPERANDS.get(code[a], 0)
    return count, len(code)


def register_size(path):
    n = len(words(path)) // 5
    return n, 4 * n


def main():
    print("best of %d runs; instructions run, and milliseconds" % RUNS)
    print("%-8s %13s %13s %13s %8s %8s %8s" % (
        "", "stack", "naive", "register", "stack", "naive", "register"))
    for b in ["fib", "loop", "sieve"]:
        s, n, r = "bench/%s.vm" % b, "bench/%s-naive.rvm" % b, "bench/%s.rvm" % b
        counts = [steps("./vm", s), steps("./rvm", n), steps("./rvm", r)]
        times = [best("./vm", s), best("./rvm", n), best("./rvm", r)]
        print("%-8s %13s %13s %13s %8.0f %8.0f %8.0f" % (
            b, *("{:,}".format(c) for c in counts), *times))

    print()
    print("%-28s %12s %12s %7s   %s" % ("instructions run", "stack", "register", "fewer",
                                          "size: instructions, words"))
    for path in sorted(glob.glob("samples/*.vm")) + ["bench/%s.vm" % b for b in
                                                     ["fib", "loop", "sieve"]]:
        rvm = path[:-3] + ".rvm"
        if not os.path.exists(rvm):
            continue
        s, r = steps("./vm", path), steps("./rvm", rvm)
        si, sw = stack_size(path)
        ri, rw = register_size(rvm)
        name = os.path.basename(path)[:-3]
        print("%-28s %12s %12s %6.0f%%   %d, %d  ->  %d, %d" % (
            name, "{:,}".format(s), "{:,}".format(r), 100 * (1 - r / s), si, sw, ri, rw))


main()
