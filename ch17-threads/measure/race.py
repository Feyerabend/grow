#!/usr/bin/env python3
"""
What a race loses, and what a lock costs. Two threads each add 1000 to one
place, in turns of different length, in three ways: with no lock, with a lock
they spin on, and with a lock they give up their turn for.

    usage: python3 measure/race.py [totals]     (with ./vm built)
"""

import os
import re
import subprocess
import sys
import tempfile

NONE = ""
SPIN = "lock:   PUSH 1\n        TAS\n        JZ got\n        JMP lock\ngot:\n"
GIVE = "lock:   PUSH 1\n        TAS\n        JZ got\n        PUSH 0\n        YIELD\n        DROP\n        JMP lock\ngot:\n"
UNLOCK = "        PUSH 1\n        PUSH 0\n        STOREM\n"


def program(turn, lock):
    source = open("suite/race.asm").read()
    source = source.replace("main:   PUSH 5", f"main:   PUSH {turn}").replace("t:      PUSH 20", "t:      PUSH 1000")
    source = source.replace("        JZ done\n", "        JZ done\n" + lock)
    if lock:
        source = source.replace("        STOREM\n", "        STOREM\n" + UNLOCK)
    return source


def run(source, folder):
    path = os.path.join(folder, "p")
    with open(path + ".asm", "w") as f:
        f.write(source)
    subprocess.run([sys.executable, "asm.py", path + ".asm", path + ".vm"], check=True)
    result = subprocess.run(["./vm", "-t", path + ".vm"], capture_output=True, text=True, check=True)
    steps = sum(1 for line in result.stderr.splitlines() if re.match(r"\s*\d+\s+\d+\s+[A-Z]", line))
    stats = subprocess.run(["./vm", "-s", path + ".vm"], capture_output=True, text=True).stderr
    switches = re.search(r"(\d+) switches", stats).group(1)
    return result.stdout.strip(), steps, switches


def main():
    print("turn  way    total  instructions  switches")
    with tempfile.TemporaryDirectory() as folder:
        for turn in (0, 2, 3, 5, 7, 10, 14, 15, 20, 50, 200):
            for name, lock in (("none", NONE), ("spin", SPIN), ("give", GIVE)):
                total, steps, switches = run(program(turn, lock), folder)
                print(f"{turn:>4}  {name:<5} {total:>6} {steps:>13} {switches:>9}")


def totals():
    """The total with no lock, for every turn from 1 to 80: the chapter's plot."""
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "p")
        for turn in range(1, 81):
            with open(path + ".asm", "w") as f:
                f.write(program(turn, NONE))
            subprocess.run([sys.executable, "asm.py", path + ".asm", path + ".vm"], check=True)
            result = subprocess.run(["./vm", path + ".vm"], capture_output=True, text=True, check=True)
            print(turn, result.stdout.strip())


if __name__ == "__main__":
    if sys.argv[1:] == ["totals"]:
        totals()
    else:
        main()
