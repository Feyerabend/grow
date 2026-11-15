#!/usr/bin/env python3
"""
Which pairs and triples of instructions run most, for exercises 20.2 and 20.3.

    import counts; counts.counts(folder)

or, to print them:

    python3 counts.py

The programs are measure/cost.py's 22: the six benchmarks and the sixteen
samples. A copy of vm.c, the switch build, counts at its fetch every pair
and every triple run in a row, within one program. Counted as cost.py does
it, every sequence run, so that loop, the longest, weighs most.
"""

import collections
import glob
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
sys.path.insert(0, CHAPTER)
import isa  # noqa: E402

NAMES = {code: name for code, name, _ in isa.INSTRUCTIONS}
BENCHMARKS = ["fib", "loop", "sieve", "closures", "enkel-sieve", "basal-loop"]
CONTROL = {"HALT", "JMP", "JZ", "CALL", "CALLI", "RET"}

COUNTING = r"""
static int p1 = -1, p2 = -1;
static long long pairs[NOPS][NOPS], triples[NOPS][NOPS][NOPS];

__attribute__((destructor)) static void report_runs(void) {
    int a, b, c;
    for (a = 0; a < NOPS; a++)
        for (b = 0; b < NOPS; b++) {
            if (pairs[a][b])
                fprintf(stderr, "pair %d %d %lld\n", a, b, pairs[a][b]);
            for (c = 0; c < NOPS; c++)
                if (triples[a][b][c])
                    fprintf(stderr, "triple %d %d %d %lld\n", a, b, c, triples[a][b][c]);
        }
}

static void run(void) {"""


def counting_build(folder):
    s = open(os.path.join(CHAPTER, "vm.c")).read()
    marker = "#define UNKNOWN     default:\n\nstatic void run(void) {"
    assert s.count(marker) == 1
    s = s.replace(marker, "#define UNKNOWN     default:\n" + COUNTING)
    fetch = "        op = code[pc++];\n        switch (op) {"
    assert s.count(fetch) == 1
    s = s.replace(fetch, "        op = code[pc++];\n"
                         "        if (op >= 0 && op < NOPS) {\n"
                         "            if (p1 >= 0) pairs[p1][op]++;\n"
                         "            if (p2 >= 0) triples[p2][p1][op]++;\n"
                         "            p2 = p1; p1 = op;\n"
                         "        }\n"
                         "        switch (op) {")
    path = os.path.join(folder, "vm.c")
    open(path, "w").write(s)
    for h in ["ops.h", "super.h"]:
        os.symlink(os.path.join(CHAPTER, h), os.path.join(folder, h))
    binary = os.path.join(folder, "vm-count")
    subprocess.run(["cc", "-std=gnu99", "-O2", "-DDISPATCH=SWITCH", "-o", binary, path],
                   check=True)
    return binary


def programs(folder):
    out = [os.path.join(CHAPTER, "bench", b + ".vm") for b in BENCHMARKS]
    for b in BENCHMARKS:
        subprocess.run(["make", "-s", "-C", CHAPTER, "bench/%s.vm" % b], check=True)
    for path in sorted(glob.glob(os.path.join(CHAPTER, "samples", "*.asm"))):
        vm = os.path.join(folder, os.path.basename(path)[:-4] + ".vm")
        subprocess.run([sys.executable, os.path.join(CHAPTER, "asm.py"), path, vm],
                       check=True)
        out.append(vm)
    return out


def counts(folder):
    """Every pair and every triple run, over the 22 programs."""
    counter = counting_build(folder)
    pairs, triples = collections.Counter(), collections.Counter()
    for p in programs(folder):
        r = subprocess.run([counter, p], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                           text=True)
        for m in re.finditer(r"^pair (\d+) (\d+) (\d+)$", r.stderr, re.M):
            a, b, n = map(int, m.groups())
            pairs[(NAMES[a], NAMES[b])] += n
        for m in re.finditer(r"^triple (\d+) (\d+) (\d+) (\d+)$", r.stderr, re.M):
            a, b, c, n = map(int, m.groups())
            triples[(NAMES[a], NAMES[b], NAMES[c])] += n
    return pairs, triples


def possible(seq):
    """A sequence run in a row is one in the code, and can be fused,
    only if no instruction but the last can change pc."""
    return all(op not in CONTROL for op in seq[:-1])


def main():
    with tempfile.TemporaryDirectory() as folder:
        pairs, triples = counts(folder)
    for title, runs in [("pairs", pairs), ("triples", triples)]:
        total = sum(runs.values())
        print("%s, of every %s run over 22 programs (* cannot be fused)" % (title, title[:-1]))
        for seq, n in runs.most_common(12):
            print("  %s%-22s %5.1f%%" % (" " if possible(seq) else "*", " ".join(seq),
                                         100 * n / total))


if __name__ == "__main__":
    main()
