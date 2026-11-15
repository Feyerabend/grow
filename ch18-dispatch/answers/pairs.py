#!/usr/bin/env python3
"""
Count which instruction follows which in bench/loop.asm, for exercise 18.1.

    python3 pairs.py [benchmark]

Uses measure/bench.py's counting build, the switch build with a count of
every pair, without running bench.py's timings: its source is read and run
here without its last line, the call of main.
"""

import collections
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "loop"
    os.chdir(CHAPTER)
    source = open("measure/bench.py").read()
    assert source.endswith("\nmain()\n")
    bench = {}
    exec(compile(source[:-len("main()\n")], "measure/bench.py", "exec"), bench)
    subprocess.run(["make", "-s", "bench/%s.vm" % name], check=True)
    with tempfile.TemporaryDirectory() as folder:
        counter = bench["counting_build"](folder)
        run = subprocess.run([counter, "bench/%s.vm" % name], stdout=subprocess.DEVNULL,
                             stderr=subprocess.PIPE, text=True, check=True)
    names = bench["NAMES"]
    pairs = collections.Counter()
    for line in run.stderr.splitlines():
        m = re.match(r"pair (\d+) (\d+) (\d+)", line)
        if m and int(m.group(1)) < len(names):
            pairs[(names[int(m.group(1))], names[int(m.group(2))])] = int(m.group(3))
    total = sum(pairs.values())
    print("%s: %s pairs" % (name, "{:,}".format(total)))
    for (a, b), n in pairs.most_common():
        print("  %-6s %-6s %12s  %5.1f%%" % (a, b, "{:,}".format(n), 100 * n / total))


main()
