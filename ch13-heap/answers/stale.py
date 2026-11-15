#!/usr/bin/env python3
"""
Exercise 13.3: stale.asm on chapter 14's machine with mark and sweep, under
stress, as it is and with NEW not zeroing its fields: the line
heap[b + HEADER + i] = integer(0); made empty, as measure/README.md says.

    usage: python3 stale.py
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH14 = os.path.join(HERE, "..", "..", "ch14-gc")

with tempfile.TemporaryDirectory() as work:
    program = os.path.join(work, "stale.vm")
    subprocess.run([sys.executable, os.path.join(CH14, "asm.py"), os.path.join(HERE, "stale.asm"), program],
                   check=True)
    source = open(os.path.join(CH14, "vm.c")).read()
    line = "heap[b + HEADER + i] = integer(0);"
    assert source.count(line) == 1
    for name, text in (("NEW zeroes", source), ("NEW does not zero", source.replace(line, ";"))):
        c, exe = os.path.join(work, "vm.c"), os.path.join(work, "vm")
        open(c, "w").write(text)
        subprocess.run(["cc", "-std=c99", "-O2", "-w", "-o", exe, c], check=True)
        r = subprocess.run([exe, "-g", "mark", "-S", program], capture_output=True, text=True)
        print(f"{name:18} prints {r.stdout.split() or 'nothing'}; {r.stderr.strip() or 'halts'}")
