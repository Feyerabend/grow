#!/usr/bin/env python3
"""
Exercises 20.2 and 20.3: superinstructions chosen by counting, made by
supers.py, and what they save.

    python3 choose.py [times] [check]

Builds, in a temporary folder:
  chapter    the chapter's eight pairs, made from ops.h by supers.py
  pairs      the eight most common pairs that can be fused, from counts.py
  triples    the chapter's eight, and the eight most common triples that can
  pairs-tri  the eight chosen pairs, and the same eight triples
and prints the dispatches each runs on the six benchmarks, beside
vm-threaded (none) and vm-super (the chapter's eight, written by hand).
With times, also best of seven times; with check, runs the suite and
tests/super on every build made here.
"""

import os
import re
import subprocess
import sys
import tempfile
import time

import counts as runs
import supers

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
BENCHMARKS = runs.BENCHMARKS


def steps(machine, program):
    r = subprocess.run([machine, "-c", program], stdout=subprocess.DEVNULL,
                       stderr=subprocess.PIPE, text=True)
    return int(re.search(r"steps: (\d+)", r.stderr).group(1))


def best(machine, program):
    times = []
    for _ in range(7):
        start = time.perf_counter()
        subprocess.run([machine, program], stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


def top(counter, n):
    return [seq for seq, _ in counter.most_common() if runs.possible(seq)][:n]


def check(binary):
    for extra in [[], ["-g", "copy", "-S"]]:
        r = subprocess.run([sys.executable, "conform.py", binary, *extra], cwd=CHAPTER,
                           stdout=subprocess.PIPE, text=True)
        line = r.stdout.strip().splitlines()[-1]
        print("  " + re.sub(r".*/", "", line))
    for t in sorted(os.listdir(os.path.join(CHAPTER, "tests", "super"))):
        if not t.endswith(".asm"):
            continue
        vm = os.path.join(os.path.dirname(binary), "t.vm")
        subprocess.run([sys.executable, "asm.py", "tests/super/" + t, vm], cwd=CHAPTER,
                       check=True)
        a = subprocess.run(["./vm-threaded", vm], cwd=CHAPTER, capture_output=True, text=True)
        b = subprocess.run([binary, vm], capture_output=True, text=True)
        if (a.stdout, a.stderr, a.returncode) != (b.stdout, b.stderr, b.returncode):
            print("  tests/super/%s differs" % t)
    print("  tests/super: checked")


def main():
    timing, checking = "times" in sys.argv[1:], "check" in sys.argv[1:]
    subprocess.run(["make", "-s", "-C", CHAPTER, "all"], check=True)
    with tempfile.TemporaryDirectory() as folder:
        pairs, triples = runs.counts(folder)
        chosen_pairs = top(pairs, 8)
        chosen_triples = top(triples, 8)
        print("the eight pairs chosen:  ", ", ".join(" ".join(s) for s in chosen_pairs))
        print("the eight triples chosen:", ", ".join(" ".join(s) for s in chosen_triples))
        sets = [("chapter", supers.CHAPTER_EIGHT), ("pairs", chosen_pairs),
                ("triples", supers.CHAPTER_EIGHT + chosen_triples),
                ("pairs-tri", chosen_pairs + chosen_triples)]
        machines = [("none", os.path.join(CHAPTER, "vm-threaded")),
                    ("by hand", os.path.join(CHAPTER, "vm-super"))]
        for name, seqs in sets:
            machines.append((name, supers.build(os.path.join(folder, name), seqs)))
        if checking:
            for name, binary in machines[2:]:
                print(name)
                check(binary)
        print()
        print("dispatched   " + "".join("%13s" % n for n, _ in machines))
        for b in BENCHMARKS:
            program = os.path.join(CHAPTER, "bench", b + ".vm")
            print("%-12s " % b + "".join("%13s" % "{:,}".format(steps(m, program))
                                         for _, m in machines))
        if timing:
            print()
            print("ms, best of 7" + "".join("%13s" % n for n, _ in machines))
            for b in BENCHMARKS:
                program = os.path.join(CHAPTER, "bench", b + ".vm")
                print("%-12s " % b + "".join("%13.0f" % best(m, program)
                                             for _, m in machines))


main()
