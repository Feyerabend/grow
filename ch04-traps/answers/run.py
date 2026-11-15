#!/usr/bin/env python3
"""
Run a program on chapter 4's machine, with or without the changes of the
exercises, and print what it printed, and its trap if it had one.

    usage: python3 run.py program.txt [overflow] [divide] [steps]

A program is words: instruction names and numbers. overflow makes ADD, SUB and
MUL trap with "overflow" when the result does not fit; divide makes DIV and MOD
trap with "overflow" on INT_MIN / -1; steps makes the machine trap with "too
many steps" after a million instructions.
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "measure"))
import harness                                  # noqa: E402


def patch(source, args):
    if "overflow" in args:
        for op, fn in (("ADD", "add"), ("SUB", "sub"), ("MUL", "mul")):
            sign = {"add": "+", "sub": "-", "mul": "*"}[fn]
            old = f"        case {op}:\n            b = pop();\n            a = pop();\n            push(a {sign} b);\n"
            new = (f"        case {op}: {{\n            int r;\n            b = pop();\n            a = pop();\n"
                   f"            if (__builtin_{fn}_overflow(a, b, &r))\n                trap(\"overflow\");\n"
                   f"            push(r);\n            break;\n        }}\n        case {op}_DONE_:\n")
            assert source.count(old) == 1, op
            source = source.replace(old, new)
        # the labels made above only keep the old "break;" lines legal
        source = re.sub(r"        case \w+_DONE_:\n            break;\n", "", source)
    if "divide" in args:
        for op in ("DIV", "MOD"):
            old = (f"        case {op}:\n            b = pop();\n            a = pop();\n"
                   "            if (b == 0)\n                trap(\"division by zero\");\n")
            assert source.count(old) == 1, op
            source = source.replace(old, old + "            if (a == INT_MIN && b == -1)\n"
                                    "                trap(\"overflow\");\n")
        source = "#include <limits.h>\n" + source
    if "steps" in args:
        old = "        start = pc;\n"
        assert source.count(old) == 1
        source = source.replace(old, old + "        if (++steps > 1000000)\n"
                                "            trap(\"too many steps\");\n")
        source = source.replace("static void run(void) {", "static long steps;\n\nstatic void run(void) {", 1)
    return source


def main():
    args = sys.argv[1:]
    source = open(os.path.join(HERE, "..", "vm.c")).read()
    names = re.search(r"enum \{(.*?)\};", source, re.S).group(1)
    names = [n.strip() for n in re.sub(r"/\*.*?\*/", "", names, flags=re.S).split(",") if n.strip()]
    words = [w for line in open(args[0]) for w in line.split(";")[0].split()]
    numbers = [str(names.index(w)) if w in names else w for w in words]
    with tempfile.TemporaryDirectory() as folder:
        exe = harness.build(checked(patch(source, args)), os.path.join(folder, "vm"), ["-O1"])
        path = os.path.join(folder, "p.txt")
        open(path, "w").write(" ".join(numbers))
        r = subprocess.run([exe, path], capture_output=True, text=True)
    print("printed:", " ".join(r.stdout.split()))
    print("then:", r.stderr.strip() or "halted")


def checked(source):
    """harness.checked, for a source already read."""
    with tempfile.NamedTemporaryFile("w", suffix=".c", delete=False) as f:
        f.write(source)
    try:
        return harness.checked(f.name)
    finally:
        os.unlink(f.name)


if __name__ == "__main__":
    main()
