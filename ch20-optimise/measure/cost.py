"""What the optimiser and the superinstructions save, and which pairs are common.

    python3 measure/cost.py

Run from the chapter's folder, after make all benchmarks. For each
benchmark it counts the instructions dispatched (-c) and times the run,
best of seven, on threaded code without and with superinstructions, each
on the program as written and as optimised. Then a build made from a
copy of vm.c, the switch build with a counter at the fetch, counts which
instruction follows which across the benchmarks and the samples: once
with every pair run counted, and once with each program given the same
weight, since loop alone runs more instructions than all the others.
"""

import collections
import glob
import os
import re
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, ".")
import isa  # noqa: E402

RUNS = 7
CC = os.environ.get("CC", "cc")
BENCHMARKS = ["fib", "loop", "sieve", "closures", "enkel-sieve", "basal-loop"]
NAMES = {code: name for code, name, _ in isa.INSTRUCTIONS}
NOPS = len(NAMES)


def steps(machine, program):
    run = subprocess.run([machine, "-c", program], stdout=subprocess.DEVNULL,
                         stderr=subprocess.PIPE, text=True)
    return int(re.search(r"steps: (\d+)", run.stderr).group(1))


def best(machine, program):
    times = []
    for _ in range(RUNS):
        start = time.perf_counter()
        subprocess.run([machine, program], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


COUNTING = r"""
static long long pairs[NOPS + 1][NOPS + 1];
static int previous = NOPS;

__attribute__((destructor)) static void report_pairs(void) {
    int a, b;
    for (a = 0; a <= NOPS; a++)
        for (b = 0; b <= NOPS; b++)
            if (pairs[a][b])
                fprintf(stderr, "pair %d %d %lld\n", a, b, pairs[a][b]);
}

static void run(void) {"""


def counting_build(folder):
    source = open("vm.c").read()
    marker = "#define UNKNOWN     default:\n\nstatic void run(void) {"
    assert source.count(marker) == 1
    source = source.replace(marker, "#define UNKNOWN     default:\n" + COUNTING)
    fetch = "        op = code[pc++];\n        switch (op) {"
    assert source.count(fetch) == 1
    source = source.replace(fetch, "        op = code[pc++];\n"
                            "        if (op >= 0 && op < NOPS) { pairs[previous][op]++; previous = op; }\n"
                            "        switch (op) {")
    path = os.path.join(folder, "vm.c")
    open(path, "w").write(source)
    for h in ["ops.h", "super.h"]:
        os.symlink(os.path.abspath(h), os.path.join(folder, h))
    binary = os.path.join(folder, "vm-count")
    subprocess.run([CC, "-std=gnu99", "-O2", "-DDISPATCH=SWITCH", "-o", binary, path],
                   check=True)
    return binary


def pair_counts(counter, program):
    run = subprocess.run([counter, program], stdout=subprocess.DEVNULL,
                         stderr=subprocess.PIPE, text=True)
    pairs = collections.Counter()
    for m in re.finditer(r"pair (\d+) (\d+) (\d+)", run.stderr):
        a, b, n = map(int, m.groups())
        if a < NOPS:
            pairs[(NAMES[a], NAMES[b])] += n
    return pairs


def main():
    print("best of %d runs, %s -O2" % (RUNS, CC))
    print("%-12s %13s %13s %13s %13s" % ("dispatched", "plain", "optimised", "super", "both"))
    rows = []
    for b in BENCHMARKS:
        plain, opt = "bench/%s.vm" % b, "bench/%s.opt.vm" % b
        runs = [("./vm-threaded", plain), ("./vm-threaded", opt),
                ("./vm-super", plain), ("./vm-super", opt)]
        counts = [steps(m, p) for m, p in runs]
        times = [best(m, p) for m, p in runs]
        rows.append((b, times))
        print("%-12s %13s %13s %13s %13s   super saves %.0f%%" % (
            b, *("{:,}".format(c) for c in counts), 100 * (1 - counts[2] / counts[0])))
    print()
    print("%-12s %13s %13s %13s %13s" % ("ms", "plain", "optimised", "super", "both"))
    for b, times in rows:
        print("%-12s %13.0f %13.0f %13.0f %13.0f" % (b, *times))

    with tempfile.TemporaryDirectory() as folder:
        counter = counting_build(folder)
        programs = ["bench/%s.vm" % b for b in BENCHMARKS]
        for asm in sorted(glob.glob("samples/*.asm")):
            vm = os.path.join(folder, os.path.basename(asm)[:-4] + ".vm")
            subprocess.run([sys.executable, "asm.py", asm, vm], check=True)
            programs.append(vm)
        every, even = collections.Counter(), collections.Counter()
        for p in programs:
            pairs = pair_counts(counter, p)
            total = sum(pairs.values())
            every.update(pairs)
            for k, n in pairs.items():
                even[k] += n / total / len(programs)
    total = sum(every.values())
    print()
    print("pairs, over %d programs: share of every pair run; and the mean share, each program"
          " weighed alike" % len(programs))
    for k, _ in every.most_common(10):
        print("  %-6s %-6s %6.1f%% %6.1f%%" % (k[0], k[1], 100 * every[k] / total, 100 * even[k]))
    print("the eight pairs of super.h")
    chosen = [("LOAD", "PUSH"), ("LOAD", "LOAD"), ("LT", "JZ"), ("PUSH", "SUB"),
              ("PUSH", "LOADM"), ("ADD", "STORE"), ("PUSH", "ADD"), ("LOAD", "ADD")]
    for k in chosen:
        print("  %-6s %-6s %6.1f%% %6.1f%%" % (k[0], k[1], 100 * every[k] / total, 100 * even[k]))
    print("  together %5.1f%% %6.1f%%" % (100 * sum(every[k] for k in chosen) / total,
                                         100 * sum(even[k] for k in chosen)))


main()
