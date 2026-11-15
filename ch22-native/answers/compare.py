#!/usr/bin/env python3
"""
Exercises 22.1 and 22.2, checked beyond the suite: random programs, run on
the interpreter and compiled each of the three ways by vm2c_more.py.

    python3 compare.py [count]

The programs are made by chapter 21's answers/fuzz_more.py, which calls a
function, sometimes with too few arguments: seed 1, the first 200 unless
told. A program that runs for more than a second either way is left out,
since the compiled code has no step limit. What it prints, its traps and its
status must be the same.
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
FUZZ = os.path.join(CHAPTER, "..", "ch21-verify", "answers", "fuzz_more.py")
MODES = [["-cache"], ["-calls"], ["-cache", "-calls"]]


def run(command):
    try:
        r = subprocess.run(command, capture_output=True, timeout=1)
    except subprocess.TimeoutExpired:
        return None
    return r.stdout, r.stderr, r.returncode


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    subprocess.run(["make", "-s", "-C", CHAPTER, "vm"], check=True)
    with tempfile.TemporaryDirectory() as w:
        subprocess.run([sys.executable, FUZZ, "1", str(count), w], check=True)
        compared = skipped = differ = 0
        verified = 0
        for name in sorted(os.listdir(w)):
            if not name.endswith(".vm"):
                continue
            program = os.path.join(w, name)
            want = run([os.path.join(CHAPTER, "vm"), "-C", program])
            if want is None:
                skipped += 1
                continue
            r = subprocess.run([os.path.join(CHAPTER, "vm"), "-V", program], capture_output=True)
            verified += r.returncode != 2
            for mode in MODES:
                c, exe = os.path.join(w, "p.c"), os.path.join(w, "p")
                with open(c, "w") as f:
                    subprocess.run([sys.executable, os.path.join(HERE, "vm2c_more.py"), *mode,
                                    program], stdout=f, check=True)
                subprocess.run(["cc", "-O1", "-w", "-I", CHAPTER, c, "-o", exe], check=True)
                got = run([exe])
                if got is None:
                    skipped += 1
                    continue
                compared += 1
                if got != want:
                    differ += 1
                    print("%s %s: differs" % (" ".join(mode), name))
        print("%d programs, %d of them verified; %d runs compared, %d differ, %d too long" % (
            count, verified, compared, differ, skipped))


main()
