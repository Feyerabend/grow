"""Time the three builds on the four benchmarks, and count what they run.

    python3 measure/bench.py

Run from the chapter's folder, after make all and make benchmarks. Each
build runs each benchmark seven times and the best time is kept. A
fourth build, made here from a copy of vm.c, counts the instructions
each benchmark executes and which instruction follows which, so that
the time can be given per instruction. Last, each build is compiled
to assembly, to count the indirect jumps the compiler left in it: an
instruction's own jump in the source may not be its own in the program.
"""

import collections
import os
import re
import subprocess
import sys
import tempfile
import time

BUILDS = ["switch", "goto", "threaded"]
BENCHMARKS = ["fib", "loop", "sieve", "closures"]
RUNS = 7
CC = os.environ.get("CC", "cc")

# The names of the instructions, by number, from isa.py.
sys.path.insert(0, ".")
import isa  # noqa: E402

NAMES = {code: name for code, name, _ in isa.INSTRUCTIONS}


def best(command):
    times = []
    for _ in range(RUNS):
        start = time.perf_counter()
        subprocess.run(command, stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times)


COUNTING = r"""
static long long counted;
static long long pairs[NOPS + 1][NOPS + 1];
static int previous = NOPS;

__attribute__((destructor)) static void report_counts(void) {
    int a, b;
    fprintf(stderr, "count %lld\n", counted);
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
    source = source.replace(
        fetch,
        "        op = code[pc++];\n"
        "        counted++;\n"
        "        if (op >= 0 && op < NOPS) { pairs[previous][op]++; previous = op; }\n"
        "        switch (op) {")
    path = os.path.join(folder, "vm.c")
    open(path, "w").write(source)
    os.symlink(os.path.abspath("ops.h"), os.path.join(folder, "ops.h"))
    binary = os.path.join(folder, "vm-count")
    subprocess.run([CC, "-std=c99", "-O2", "-DDISPATCH=SWITCH", "-o", binary, path],
                   check=True)
    return binary


def indirect_jumps(build, folder):
    """Count the indirect jumps in the assembly of one build."""
    path = os.path.join(folder, build + ".s")
    subprocess.run([CC, "-std=gnu99", "-O2", "-DDISPATCH=" + build.upper(), "-S",
                    "-o", path, "vm.c"], check=True)
    text = open(path).read()
    # arm64: br xN; x86-64: jmp *...
    return len(re.findall(r"\tbr\tx\d+|\tjmpq?\s+\*", text))


def main():
    names = NAMES
    with tempfile.TemporaryDirectory() as folder:
        counter = counting_build(folder)
        counts, top = {}, {}
        for b in BENCHMARKS:
            run = subprocess.run([counter, "bench/%s.vm" % b], stdout=subprocess.DEVNULL,
                                 stderr=subprocess.PIPE, text=True, check=True)
            pairs = collections.Counter()
            for line in run.stderr.splitlines():
                m = re.match(r"count (\d+)", line)
                if m:
                    counts[b] = int(m.group(1))
                m = re.match(r"pair (\d+) (\d+) (\d+)", line)
                if m and int(m.group(1)) < len(NAMES):
                    pairs[(int(m.group(1)), int(m.group(2)))] = int(m.group(3))
            top[b] = pairs
        jumps = {v: indirect_jumps(v, folder) for v in BUILDS}

    print("best of %d runs, %s -O2" % (RUNS, CC))
    print("%-9s %12s  %18s %18s %18s" % ("", "executed", *BUILDS))
    for b in BENCHMARKS:
        cells = []
        for v in BUILDS:
            t = best(["./vm-" + v, "bench/%s.vm" % b])
            cells.append("%5.0f ms %4.2f ns" % (t * 1000, t * 1e9 / counts[b]))
        print("%-9s %12s  %18s %18s %18s" % (b, "{:,}".format(counts[b]), *cells))

    print("%-9s %12s  %18s %18s %18s" % ("jumps", "", *(str(jumps[v]) for v in BUILDS)))
    print("(jumps: the indirect jumps in each build's assembly)")
    print()
    print("the most common pairs, and how often the first is followed by the second")
    for b in BENCHMARKS:
        pairs = top[b]
        firsts = collections.Counter()
        for (a, _), n in pairs.items():
            firsts[a] += n
        total = sum(pairs.values())
        line = []
        for (a, c), n in pairs.most_common(3):
            line.append("%s %s %.0f%% of all, %.0f%% after %s" % (
                names.get(a, a), names.get(c, c), 100 * n / total,
                100 * n / firsts[a], names.get(a, a)))
        print("%-9s %s" % (b, "; ".join(line)))
    lt = collections.Counter()
    for b in BENCHMARKS:
        for (a, c), n in top[b].items():
            if names.get(a) == "LT":
                lt[names.get(c, c)] += n
    print("after LT, in all four:", dict(lt))


main()
