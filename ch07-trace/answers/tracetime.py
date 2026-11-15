#!/usr/bin/env python3
"""
Exercise 7.4: measure/tracecost.py's loop, about 210,000 steps, traced into a
file with -t and with -T, best of three; and the two traces compared.

    usage: python3 tracetime.py [times]
"""

import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "measure"))
import tracecost                                # noqa: E402  (its LOOP and timed)


with tempfile.TemporaryDirectory() as folder:
    src, prog, c, exe = (os.path.join(folder, x) for x in ("loop.asm", "loop.vm", "vm.c", "vm"))
    open(src, "w").write(tracecost.LOOP.format(n=30_000))
    subprocess.run([sys.executable, os.path.join(HERE, "..", "asm.py"), src, prog], check=True)
    with open(c, "w") as f:
        subprocess.run([sys.executable, os.path.join(HERE, "build.py")], stdout=f, check=True)
    subprocess.run(["cc", "-std=c99", "-O2", "-o", exe, c], check=True)
    times, traces = {}, {}
    for flag in ("-t", "-T"):
        path = os.path.join(folder, "trace" + flag + ".txt")
        with open(path, "w") as f:
            times[flag] = tracecost.timed([exe, flag, prog], f)
        traces[flag] = open(path).read()
    if "times" in sys.argv[1:]:                 # they differ from run to run
        print(f"-t, unbuffered:  {times['-t']:.2f} s")
        print(f"-T, buffered:    {times['-T']:.2f} s, {times['-t'] / times['-T']:.0f} times faster")
    print("the same trace" if traces["-t"] == traces["-T"] else "the traces differ")
