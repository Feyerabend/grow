#!/usr/bin/env python3
"""
Exercise 21.2: where a stack overflow is reported, checked at every push
(the chapter's machine, verified) and checked once at each CALL (build.py's
-DROOM). Runs room-where.asm and room-unused.asm on both, and prints the
last two lines of each run and its status.

    python3 room.py
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)


def run(vm, program):
    r = subprocess.run([vm, "-v", program], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    verdict = [l for l in out if "verified" in l]
    rest = [l for l in out if "verified" not in l]
    return "%s; %d line%s, the last %s; status %d" % (
        verdict[0].split(": ", 1)[1], len(rest), "" if len(rest) == 1 else "s",
        " / ".join(rest[-2:]), r.returncode)


def main():
    subprocess.run(["make", "-s", "-C", CHAPTER, "vm"], check=True)
    with tempfile.TemporaryDirectory() as w:
        subprocess.run([sys.executable, os.path.join(HERE, "build.py"), w], check=True)
        room = os.path.join(w, "vm-room")
        subprocess.run(["cc", "-std=gnu99", "-O2", "-DROOM", "-o", room,
                        os.path.join(w, "vm.c")], check=True)
        for name in ["room-where", "room-unused"]:
            vm = os.path.join(w, name + ".vm")
            subprocess.run([sys.executable, os.path.join(CHAPTER, "asm.py"),
                            os.path.join(HERE, name + ".asm"), vm], check=True)
            print(name)
            print("  at every push: " + run(os.path.join(CHAPTER, "vm"), vm))
            print("  at each CALL:  " + run(room, vm))


main()
