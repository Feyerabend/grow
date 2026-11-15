#!/usr/bin/env python3
"""
Does the suite catch mistakes in the heap?

Each mutant is vm.c with one small change to the code of this chapter: the
tags, the bounds checks, NEW, EQ and JZ on references. Each is compiled and
run twice: by conform.py on the suite of version 3, and by compare.py, whose
traces must agree with vm.py's on every suite program and sample. A mutant
that passes both is a mistake the tests cannot see.

    usage: python3 measure/mutants.py      (run in code/ch13-heap, after make)
"""

import os
import subprocess
import sys
import tempfile

MUTANTS = [
    ("NEW does not zero its fields",
     "heap[heap_used + HEADER + i] = integer(0);", ";"),
    ("bounds check one too late",
     "i >= heap[b].n", "i > heap[b].n"),
    ("no check for a negative index",
     "if (i < 0 || i >= heap[b].n)", "if (i >= heap[b].n)"),
    ("no check for a negative size",
     "if (n < 0)\n        trap(\"bad size\");\n", ""),
    ("out of memory one block early",
     "n > HEAP_SIZE - HEADER - heap_used", "n >= HEAP_SIZE - HEADER - heap_used"),
    ("arithmetic on references allowed",
     "if (v.is_ref)\n        trap(\"not a number\");", ""),
    ("GETF and SETF on numbers allowed",
     "if (!v.is_ref)\n        trap(\"not a reference\");", ""),
    ("EQ ignores the tag",
     "return a.is_ref == b.is_ref && a.n == b.n;", "return a.n == b.n;"),
    ("JZ ignores the tag",
     "if (!v.is_ref && v.n == 0)", "if (v.n == 0)"),
    ("SETF loses the tag",
     "heap[field(b, number(w))] = u;", "heap[field(b, number(w))] = integer(u.n);"),
    ("fields start one place early",
     "return b + HEADER + i;", "return b + HEADER - 1 + i;"),
    ("blocks numbered from 0",
     "integer(++blocks_made)", "integer(blocks_made++)"),
]


def passes(command):
    r = subprocess.run(command, capture_output=True, text=True)
    return r.returncode == 0


def main():
    source = open("vm.c").read()
    vms = sorted(f"build/{f}" for f in os.listdir("build")) + \
        sorted(f"samples/{f}" for f in os.listdir("samples") if f.endswith(".vm"))
    py = f"{sys.executable} vm.py"
    print(f"{'mutant':36} {'suite':>8} {'traces':>8}")
    survived = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, old, new in MUTANTS:
            assert source.count(old) == 1, name
            path = os.path.join(tmp, "vm.c")
            with open(path, "w") as f:
                f.write(source.replace(old, new))
            binary = os.path.join(tmp, "vm")
            subprocess.run(["cc", "-std=c99", "-O2", "-w", "-o", binary, path], check=True)
            suite = passes([sys.executable, "conform.py", "--known", "garbage", binary])
            traces = passes([sys.executable, "compare.py", binary, py] + vms)
            if suite and traces:
                survived += 1
            print(f"{name:36} {'missed' if suite else 'caught':>8}"
                  f" {'missed' if traces else 'caught':>8}")
    print(f"{len(MUTANTS) - survived} of {len(MUTANTS)} caught by one or the other")


if __name__ == "__main__":
    main()
