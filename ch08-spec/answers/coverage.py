#!/usr/bin/env python3
"""
Exercise 8.4: which lines of vm.c the conformance suite runs. vm.c is built
with --coverage, conform.py runs the suite on it, and llvm-cov gcov (the gcov
of Apple's clang; with GCC, gcov) says how often each line ran. The lines that
never ran are counted by the function they are in.

    usage: python3 coverage.py
"""

import collections
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH08 = os.path.join(HERE, "..")

with tempfile.TemporaryDirectory() as folder:
    shutil.copy(os.path.join(CH08, "vm.c"), folder)
    subprocess.run(["cc", "-std=c99", "-O0", "--coverage", "-o", "vm", "vm.c"], cwd=folder, check=True)
    r = subprocess.run([sys.executable, "conform.py", os.path.join(folder, "vm")], cwd=CH08,
                       capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1].replace(folder + "/", ""))
    gcov = ["xcrun", "llvm-cov", "gcov"] if shutil.which("xcrun") else ["gcov"]
    subprocess.run(gcov + ["-o", ".", "vm-vm" if os.path.exists(os.path.join(folder, "vm-vm.gcno")) else "vm"],
                   cwd=folder, capture_output=True, check=True)
    lines = open(os.path.join(folder, "vm.c.gcov")).read().splitlines()

ran = never = 0
function, unrun = None, collections.Counter()
for line in lines:
    count, number, text = (part.strip() if i < 2 else part for i, part in enumerate(line.split(":", 2)))
    m = re.match(r"(?:static\s+)?[\w\s\*]+?\b(\w+)\(.*\)\s*\{", text)
    if m and not text.startswith(" "):
        function = m.group(1)
    if count == "-":
        continue
    if count == "#####":
        never += 1
        unrun[function] += 1
    else:
        ran += 1
print(f"lines run: {ran} of {ran + never}, {100 * ran / (ran + never):.0f}%")
print("lines never run, by function:")
for name, n in sorted(unrun.items(), key=lambda x: (-x[1], x[0])):
    print(f"  {n:>4}  {name}")
