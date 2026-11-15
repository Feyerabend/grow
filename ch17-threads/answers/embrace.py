#!/usr/bin/env python3
"""
Exercise 17.4: embrace.asm three ways: as written, in turns of 5, where the
scheduler finds the deadly embrace and prints -1; with no limit on turns,
where thread 1 finishes before thread 2 starts, and both end (0); and in turns
of 5 with the check taken out, where the two wait for ever, so the run is
stopped after two seconds.

    usage: python3 embrace.py
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(HERE, "..")
source = open(os.path.join(HERE, "embrace.asm")).read()
variants = [
    ("turns of 5, with the check", source),
    ("no limit on turns", source.replace("main:   PUSH 5\n        SLICE", "main:   PUSH 0\n        SLICE", 1)),
    ("turns of 5, without the check", source.replace("check:  CALL stuck 0\n        JZ loop",
                                                     "check:  JMP loop", 1)),
]
with tempfile.TemporaryDirectory() as work:
    vm = os.path.join(work, "vm")
    subprocess.run(["cc", "-std=c99", "-O2", "-w", "-o", vm, os.path.join(CH, "vm.c")], check=True)
    for name, text in variants:
        asm, prog = os.path.join(work, "e.asm"), os.path.join(work, "e.vm")
        open(asm, "w").write(text)
        subprocess.run([sys.executable, os.path.join(CH, "asm.py"), asm, prog], check=True)
        try:
            r = subprocess.run([vm, prog], capture_output=True, text=True, timeout=2)
            print(f"{name:32} prints {r.stdout.strip()}")
        except subprocess.TimeoutExpired:
            print(f"{name:32} still waiting after two seconds")
