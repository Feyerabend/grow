#!/usr/bin/env python3
"""
Exercise 19.2: the register machine with JGE and JGEI, made by build.py.

    python3 jge.py [times]

Run from this folder, after make test in the chapter's folder. Checks that
the fused code prints the same as the stack machine for the benchmarks, the
samples and ltref.asm (a trap at the LT), and counts the instructions run
before and after; with times, also times the three benchmarks, best of seven.
"""

import glob
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)


def run(command):
    r = subprocess.run(command, cwd=CHAPTER, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, text=True)
    steps = re.search(r"steps: (\d+)", r.stderr)
    rest = re.sub(r"steps: \d+\n", "", r.stderr)
    return r.stdout + rest + "status %d\n" % r.returncode, int(steps.group(1)) if steps else 0


def best(command):
    times = []
    for _ in range(7):
        start = time.perf_counter()
        subprocess.run(command, cwd=CHAPTER, stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


def main():
    timing = sys.argv[1:] == ["times"]
    with tempfile.TemporaryDirectory() as w:
        subprocess.run([sys.executable, os.path.join(HERE, "build.py"), w], check=True)
        rvm = os.path.join(w, "rvm")
        subprocess.run(["cc", "-std=c99", "-O2", "-o", rvm, os.path.join(w, "rvm.c")],
                       check=True)
        ltref = os.path.join(w, "ltref.vm")
        subprocess.run([sys.executable, "asm.py", os.path.join(HERE, "ltref.asm"), ltref],
                       cwd=CHAPTER, check=True)
        programs = ["bench/%s.vm" % b for b in ["fib", "loop", "sieve"]]
        programs += sorted(os.path.relpath(p, CHAPTER)
                           for p in glob.glob(os.path.join(CHAPTER, "samples", "*.vm")))
        programs.append(ltref)
        print("%-30s %13s %13s %13s %6s" % ("instructions run", "stack", "register",
                                            "with JGE", "fewer"))
        for p in programs:
            fused = os.path.join(w, "fused.rvm")
            subprocess.run([sys.executable, os.path.join(w, "translate.py"), "-jge", p,
                            fused], cwd=CHAPTER, check=True)
            want, s = run(["./vm", "-c", p])
            plain = os.path.join(CHAPTER, p[:-3] + ".rvm")
            if not os.path.exists(plain):
                plain = os.path.join(w, "plain.rvm")
                subprocess.run([sys.executable, "translate.py", p, plain], cwd=CHAPTER,
                               check=True)
            got_r, r = run(["./rvm", "-c", plain])
            got_j, j = run([rvm, "-c", fused])
            same = "" if want == got_r == got_j else "  DIFFERENT"
            name = os.path.basename(p)[:-3]
            print("%-30s %13s %13s %13s %5.1f%%%s" % (
                name, "{:,}".format(s), "{:,}".format(r), "{:,}".format(j),
                100 * (1 - j / r), same))
            if p == ltref:
                print("  " + got_j.replace("\n", "; ").rstrip("; "))
        if timing:
            print()
            print("best of 7, ms        register      with JGE")
            for b in ["fib", "loop", "sieve"]:
                fused = os.path.join(w, b + ".rvm")
                subprocess.run([sys.executable, os.path.join(w, "translate.py"), "-jge",
                                "bench/%s.vm" % b, fused], cwd=CHAPTER, check=True)
                print("%-16s %12.0f %13.0f" % (b, best(["./rvm", "bench/%s.rvm" % b]),
                                               best([rvm, fused])))


main()
