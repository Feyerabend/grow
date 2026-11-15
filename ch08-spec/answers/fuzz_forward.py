#!/usr/bin/env python3
"""
Exercise 8.3: random programs that must halt, run on vm.c and vm.py and
compared. measure/fuzz.py stops a program after a second; here every jump
and call goes forward, to an address after its own, so the programs it makes
cannot loop, and no time limit is needed. How many still ran for a second is
counted, to check that.

    usage: python3 fuzz_forward.py [count] [seed]
"""

import os
import random
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import isa      # noqa: E402
import vmfile   # noqa: E402

LENGTH = 32


def program(rng):
    words = []
    while len(words) < LENGTH:
        code, name, kinds = rng.choice(isa.INSTRUCTIONS)
        at = len(words)
        words.append(code)
        for kind in kinds:
            if kind == "addr":
                words.append(rng.randrange(at + 1, LENGTH + 1))   # forward only
            elif name == "PUSH" and rng.random() < 0.2:
                words.append(rng.randrange(-2**31, 2**31))
            else:
                words.append(rng.randrange(41))
    return words[:LENGTH]


def run(command, path):
    try:
        r = subprocess.run(command + [path], capture_output=True, text=True, timeout=1)
    except subprocess.TimeoutExpired:
        return "still running"
    return (r.stdout, r.returncode, r.stderr)


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    with tempfile.TemporaryDirectory() as folder:
        exe = os.path.join(folder, "vm")
        subprocess.run(["cc", "-std=c99", "-O1", "-w", "-o", exe, os.path.join(HERE, "..", "vm.c")], check=True)
        path = os.path.join(folder, "p.vm")
        differ = running = halted = 0
        for _ in range(count):
            vmfile.write(path, program(rng))
            a = run([exe], path)
            b = run([sys.executable, os.path.join(HERE, "..", "vm.py")], path)
            running += "still running" in (a, b)
            differ += a != b
            halted += a != "still running" and a[1] == 0
    print(f"{count} programs, every jump and call forward")
    print(f"  still running after a second: {running}")
    print(f"  halted without a trap: {halted}")
    print(f"  vm.c and vm.py differ: {differ}")


if __name__ == "__main__":
    main()
