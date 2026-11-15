#!/usr/bin/env python3
"""
Exercise 22.3: the JIT of jit.h, built by build.py, checked and timed.

    python3 jit.py [times]

Builds two machines: vm-jit, which translates PUSH, ADD, LOAD, STORE, JZ and
JMP, as the exercise asks; and vm-jit8, with SUB and AND too. Runs the suite
on both, with both collectors and stress; prints, with -J, what each
translates in each benchmark; and runs 1200 random programs, chapter 21's
fuzz.py and answers/fuzz_more.py, seed 1, on both, verified, against the
chapter's interpreter with every check (-C). A program that runs over a
half a second either way is left out: the machine code does not count steps, so a
program that never ends cannot be stopped in the same place. With times,
the benchmarks are timed, best of seven.
"""

import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
VERIFY = os.path.join(CHAPTER, "..", "ch21-verify")
BENCHMARKS = ["fib", "loop", "sieve", "closures", "enkel-sieve", "basal-loop"]


def run(command):
    try:
        r = subprocess.run(command, capture_output=True, timeout=0.5)
    except subprocess.TimeoutExpired:
        return None
    return r.stdout, r.stderr, r.returncode


def best(command):
    times = []
    for _ in range(7):
        start = time.perf_counter()
        subprocess.run(command, stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


def main():
    subprocess.run(["make", "-s", "-C", CHAPTER, "vm", "benchmarks"], check=True)
    vm = os.path.join(CHAPTER, "vm")
    with tempfile.TemporaryDirectory() as w:
        subprocess.run([sys.executable, os.path.join(HERE, "build.py"), w], check=True)
        machines = []
        for name, flags in [("vm-jit", ["-DJIT"]), ("vm-jit8", ["-DJIT", "-DJIT_MORE"])]:
            exe = os.path.join(w, name)
            subprocess.run(["cc", "-std=gnu99", "-O2", "-Wall", "-Wextra", *flags, "-o", exe,
                            os.path.join(w, "vm.c")], check=True)
            machines.append((name, exe))
        for name, exe in machines:
            for extra in [[], ["-g", "copy", "-S"]]:
                r = subprocess.run([sys.executable, "conform.py", exe, *extra], cwd=CHAPTER,
                                   capture_output=True, text=True)
                print(re.sub(r".*/", "", r.stdout.strip().splitlines()[-1]))
        for b in BENCHMARKS:
            program = os.path.join(CHAPTER, "bench", b + ".vm")
            want = open(os.path.join(CHAPTER, "bench", b + ".out")).read()
            for name, exe in machines:
                r = subprocess.run([exe, "-J", program], capture_output=True, text=True)
                assert r.stdout == want, (name, b)
                print("%-12s %-8s %s" % (b, name, r.stderr.strip()))
        compared = skipped = differ = 0
        for gen in [os.path.join(VERIFY, "fuzz.py"),
                    os.path.join(VERIFY, "answers", "fuzz_more.py")]:
            d = os.path.join(w, os.path.basename(gen)[:-3])
            subprocess.run([sys.executable, gen, "1", "600", d], cwd=VERIFY, check=True)
            for p in sorted(os.listdir(d)):
                program = os.path.join(d, p)
                want = run([vm, "-C", program])
                for name, exe in machines:
                    got = run([exe, program])
                    if want is None or got is None:
                        skipped += 1
                        continue
                    compared += 1
                    if got != want:
                        differ += 1
                        print("%s %s: differs" % (name, p))
        print("random programs: %d runs compared, %d differ, %d left out as too long" % (
            compared, differ, skipped))
        if "times" in sys.argv[1:]:
            print()
            print("ms, best of 7   interpreted   vm-jit  vm-jit8")
            for b in BENCHMARKS:
                program = os.path.join(CHAPTER, "bench", b + ".vm")
                print("%-14s %11.0f %8.0f %8.0f" % (b, best([vm, program]),
                                                    *(best([exe, program]) for _, exe in machines)))


main()
