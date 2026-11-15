#!/usr/bin/env python3
"""
Chapter 8's measurements: random programs on both machines, and planted
mistakes.

Random programs are 32 words of this machine's instructions with operands
from 0 to 40, and now and then a PUSH of a number anywhere in 32 bits, so
that overflow happens. Each runs on vm.c and on vm.py, a second at most, and
what they print, their status and their message are compared.

Then five copies of vm.py, each with one mistake planted in it (a mutant),
are run against the conformance suite and against the same random programs.
For each: how many suite tests fail, and how many random programs show it.

    usage: python3 measure/fuzz.py [count] [seed]      (from ch08-spec)
"""

import os
import random
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.getcwd())
import isa
import vmfile

MUTANTS = {
    "division rounds down, as Python's // does":
        ("    q = abs(a) // abs(b)\n    return q if (a < 0) == (b < 0) else -q",
         "    return a // b"),
    "STORE checks its local before popping, as in chapter 7":
        ("            v = self.pop()\n            if k < 0 or self.fp + k >= len(self.stack):\n"
         "                raise Trap(\"no such local\")\n",
         "            if k < 0 or self.fp + k >= len(self.stack):\n"
         "                raise Trap(\"no such local\")\n            v = self.pop()\n"),
    "arithmetic does not wrap at 32 bits":
        ("        self.push(wrap(f(a, b)))", "        self.push(f(a, b))"),
    "the stack holds 255 values, not 256":
        ("STACK_SIZE = 256", "STACK_SIZE = 255"),
    "LT is less than or equal":
        ("self.binary(lambda a, b: int(a < b))", "self.binary(lambda a, b: int(a <= b))"),
}


def program(rng):
    words = []
    while len(words) < 32:
        code, name, kinds = rng.choice(isa.INSTRUCTIONS)
        words.append(code)
        for _ in kinds:
            if name == "PUSH" and rng.random() < 0.2:
                words.append(rng.randrange(-2**31, 2**31))
            else:
                words.append(rng.randrange(41))
    return words[:32]


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
        subprocess.run(["cc", "-std=c99", "-O1", "-o", exe, "vm.c"], check=True)
        programs = []
        for i in range(count):
            path = os.path.join(folder, f"r{i}.vm")
            vmfile.write(path, program(rng))
            programs.append(path)
        c_results = [run([exe], p) for p in programs]
        py_results = [run([sys.executable, "vm.py"], p) for p in programs]
        differ = sum(a != b for a, b in zip(c_results, py_results))
        print(f"{count} random programs: vm.c and vm.py differ on {differ}")
        print()
        source = open("vm.py").read()
        for what, (old, new) in MUTANTS.items():
            assert source.count(old) == 1, what
            mutant = os.path.join(os.getcwd(), "_mutant.py")
            open(mutant, "w").write(source.replace(old, new))
            try:
                out = subprocess.run([sys.executable, "conform.py", sys.executable, mutant],
                                     capture_output=True, text=True).stdout
                m = re.search(r"(\d+) of (\d+) passed", out)
                failed = int(m.group(2)) - int(m.group(1))
                shown = sum(run([sys.executable, mutant], p) != c
                            for p, c in zip(programs, c_results))
            finally:
                os.remove(mutant)
            print(f"{what}:\n    suite fails {failed} of {m.group(2)}; "
                  f"random programs show it {shown} of {count}")


if __name__ == "__main__":
    main()
