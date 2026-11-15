#!/usr/bin/env python3
"""
Exercise 13.5: full.asm against measure/mutants.py's mutant "out of memory one
block early", and against the right machines, vm.c and vm.py. full.asm fills
the heap exactly, so the right machines print 4096 and then trap; the mutant
traps one block sooner, before printing anything.

    usage: python3 oom_check.py
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH13 = os.path.join(HERE, "..")
sys.path.insert(0, CH13)
sys.path.insert(0, os.path.join(CH13, "measure"))
import mutants                                  # noqa: E402

with tempfile.TemporaryDirectory() as work:
    program = os.path.join(work, "full.vm")
    subprocess.run([sys.executable, os.path.join(CH13, "asm.py"), os.path.join(HERE, "full.asm"), program], check=True)
    source = open(os.path.join(CH13, "vm.c")).read()
    machines = {"vm.c": source}
    for name, old, new in mutants.MUTANTS:
        if name == "out of memory one block early":
            assert source.count(old) == 1
            machines["the mutant"] = source.replace(old, new)
    runs = []
    for name, text in machines.items():
        c, exe = os.path.join(work, "m.c"), os.path.join(work, name.replace(" ", "_"))
        open(c, "w").write(text)
        subprocess.run(["cc", "-std=c99", "-O2", "-w", "-o", exe, c], check=True)
        runs.append((name, [exe, program]))
    runs.append(("vm.py", [sys.executable, os.path.join(CH13, "vm.py"), program]))
    for name, command in runs:
        r = subprocess.run(command, capture_output=True, text=True)
        print(f"{name:10} prints {r.stdout.split() or 'nothing'}; {r.stderr.strip()}")
