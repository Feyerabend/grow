#!/usr/bin/env python3
"""
Exercise 19.3: how much of the stack machine's work only moves values.

    python3 moves.py

Run from this folder, after make test in the chapter's folder. Builds a
copy of the stack machine that counts each instruction it runs, and runs
the benchmarks and the samples on it. Two groups are counted: DUP, DROP,
SWAP, OVER and ROT, which only rearrange the stack; and LOAD and STORE,
which only copy between a local and the top. Stage one makes each of
them a MOV, or nothing, and stage two removes most of those MOVs. The
column "not run" is, for comparison, the share of the stack machine's
instructions that the register code does without. A last line counts the
same in what is written in the samples' assembly, each instruction once.
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
SHUFFLE = {"DUP", "DROP", "SWAP", "OVER", "ROT"}
LOCALS = {"LOAD", "STORE"}


def counting(folder):
    s = open(os.path.join(CHAPTER, "vm.c")).read()
    fetch = "        op = code[pc++];\n        switch (op) {"
    assert s.count(fetch) == 1
    s = s.replace(fetch, "        op = code[pc++];\n"
                         "        if (op >= 0 && op < NOPS) each[op]++;\n"
                         "        switch (op) {")
    report = "static void report(void) {\n    if (counting) {"
    assert s.count(report) == 1
    s = s.replace(report, "static long each[NOPS];\n\nstatic void report(void) {\n"
                          "    for (int k = 0; k < NOPS; k++)\n"
                          "        if (each[k])\n"
                          "            fprintf(stderr, \"op %d %ld\\n\", k, each[k]);\n"
                          "    if (counting) {")
    path = os.path.join(folder, "vm.c")
    open(path, "w").write(s)
    binary = os.path.join(folder, "vm-count")
    subprocess.run(["cc", "-std=c99", "-O2", "-I", CHAPTER, "-o", binary, path], check=True)
    return binary


def steps(machine, program):
    r = subprocess.run([machine, "-c", program], cwd=CHAPTER, stdout=subprocess.DEVNULL,
                       stderr=subprocess.PIPE, text=True)
    return r.stderr


def main():
    programs = ["bench/%s.vm" % b for b in ["fib", "loop", "sieve"]]
    programs += sorted(os.path.relpath(p, CHAPTER)
                       for p in glob.glob(os.path.join(CHAPTER, "samples", "*.vm")))
    with tempfile.TemporaryDirectory() as folder:
        vm = counting(folder)
        print("%-27s %12s %8s %8s %8s %9s" % ("instructions run", "stack", "shuffle",
                                             "locals", "both", "not run"))
        total = collections.Counter()
        for p in programs:
            each = collections.Counter()
            text = steps(vm, p)
            for m in re.finditer(r"op (\d+) (\d+)", text):
                each[NAMES[int(m.group(1))]] = int(m.group(2))
            n = int(re.search(r"steps: (\d+)", text).group(1))
            r = int(re.search(r"steps: (\d+)", steps("./rvm", p[:-3] + ".rvm")).group(1))
            sh = sum(each[k] for k in SHUFFLE)
            lo = sum(each[k] for k in LOCALS)
            total.update({"n": n, "sh": sh, "lo": lo, "r": r})
            print("%-27s %12s %7.1f%% %7.1f%% %7.1f%% %8.1f%%" % (
                os.path.basename(p)[:-3], "{:,}".format(n), 100 * sh / n, 100 * lo / n,
                100 * (sh + lo) / n, 100 * (1 - r / n)))
        # The same, counted in what is written: each instruction in the
        # samples' assembly once, however often it runs.
        static = collections.Counter()
        for p in programs:
            if not p.startswith("samples"):
                continue
            for line in open(os.path.join(CHAPTER, p[:-3] + ".asm")):
                words = [w for w in line.split(";")[0].split() if not w.endswith(":")]
                if words and words[0] in isa.BY_NAME:
                    static[words[0]] += 1
        n = sum(static.values())
        sh = sum(static[k] for k in SHUFFLE)
        lo = sum(static[k] for k in LOCALS)
        print("%-27s %12s %7.1f%% %7.1f%% %7.1f%%" % (
            "samples, as written", n, 100 * sh / n, 100 * lo / n, 100 * (sh + lo) / n))

main()
