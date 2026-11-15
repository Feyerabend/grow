#!/usr/bin/env python3
"""
Exercises 14.1 and 14.5, timed: samples/trees.asm under the four collectors,
and fit.asm under first fit and next fit. Best of five, cc -O2, as the whole
run's time; the collector's own share, from -s, beside it.

    usage: python3 times.py
"""

import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CH14 = os.path.join(HERE, "..")


def best(command):
    times, out = [], ""
    for _ in range(5):
        start = time.perf_counter()
        r = subprocess.run(command, capture_output=True, text=True, check=True)
        times.append(time.perf_counter() - start)
        out = r.stderr
    gc = float(re.search(r"([\d.]+) seconds collecting", out).group(1))
    return min(times) * 1000, gc * 1000


with tempfile.TemporaryDirectory() as work:
    c, exe = os.path.join(work, "vm_more.c"), os.path.join(work, "vm")
    with open(c, "w") as f:
        subprocess.run([sys.executable, os.path.join(HERE, "build.py")], stdout=f, check=True)
    subprocess.run(["cc", "-std=c99", "-O2", "-o", exe, c], check=True)
    programs = {}
    for name, path in (("trees", os.path.join(CH14, "samples", "trees.asm")),
                       ("fit", os.path.join(HERE, "fit.asm"))):
        programs[name] = os.path.join(work, name + ".vm")
        subprocess.run([sys.executable, os.path.join(CH14, "asm.py"), path, programs[name]], check=True)
    print("best of 5 runs, milliseconds: the whole run, and the collector's part of it")
    for name, collectors in (("trees", ("mark", "next", "copy", "compact")), ("fit", ("mark", "next"))):
        for g in collectors:
            whole, gc = best([exe, "-g", g, "-s", programs[name]])
            print(f"  {name:6} {g:8} {whole:6.0f} {gc:6.0f}")
