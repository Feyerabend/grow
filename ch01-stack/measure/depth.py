#!/usr/bin/env python3
"""
How deep the stack goes, for one sum or product in different orders.

Each expression is turned into the machine's code in the order it is written,
and also in the best order, where for + and * the deeper side is done first.
Then the code is run in a copy of chapter 1's machine, built with a counter of
the deepest the stack goes, and that is what is printed. Ershov's number for
the tree is printed beside it: the best order should reach it, and no order
less.

    usage: python3 measure/depth.py      (from ch01-stack)
"""

import os
import subprocess
import sys
import tempfile

OPS = {"+": "ADD", "-": "SUB", "*": "MUL"}


def parse(text):
    """A tiny parser for fully parenthesised expressions: (a op b), numbers."""
    tokens = text.replace("(", " ( ").replace(")", " ) ").split()

    def expr(i):
        if tokens[i] == "(":
            left, i = expr(i + 1)
            op = tokens[i]
            right, i = expr(i + 1)
            assert tokens[i] == ")"
            return (op, left, right), i + 1
        return int(tokens[i]), i + 1

    tree, i = expr(0)
    assert i == len(tokens)
    return tree


def ershov(t):
    if isinstance(t, int):
        return 1
    l, r = ershov(t[1]), ershov(t[2])
    return max(l, r) if l != r else l + 1


def code(t, best):
    """The machine's code for t, as C array items."""
    if isinstance(t, int):
        return ["PUSH", str(t)]
    op, a, b = t
    if best and op != "-" and ershov(b) > ershov(a):
        a, b = b, a                     # the same value: + and * do not care
    return code(a, best) + code(b, best) + [OPS[op]]


def run(items, folder):
    """Run the code in chapter 1's machine, counting the deepest point."""
    source = open("vm.c").read()
    source = source.replace("static void push(int v) {\n    stack[sp++] = v;",
                            "static int deepest = 0;\n\nstatic void push(int v) {\n"
                            "    stack[sp++] = v;\n    if (sp > deepest)\n        deepest = sp;")
    start = source.index("static const int program[] = {")
    end = source.index("};", start) + 2
    program = "static const int program[] = {\n    " + ", ".join(items + ["PRINT", "HALT"]) + "\n};"
    source = source[:start] + program + source[end:]
    source = source.replace("    run(program);\n", "    run(program);\n    printf(\"deepest %d\\n\", deepest);\n")
    c = os.path.join(folder, "vm.c")
    with open(c, "w") as f:
        f.write(source)
    exe = os.path.join(folder, "vm")
    subprocess.run(["cc", "-std=c99", "-O1", "-o", exe, c], check=True)
    out = subprocess.run([exe], capture_output=True, text=True, check=True).stdout.split()
    return int(out[0]), int(out[2])


EXPRESSIONS = [
    "((((1 + 2) + 3) + 4) + 5)",
    "(1 + (2 + (3 + (4 + 5))))",
    "(((1 + 2) + (3 + 4)) + 5)",
    "(((1 + 2) * (3 + 4)) - ((5 + 6) * (7 + 8)))",
    "(1 - (2 - (3 - (4 - 5))))",
]


def main():
    print(f"{'expression':<46} {'value':>6} {'as written':>10} {'best':>5} {'Ershov':>7}")
    with tempfile.TemporaryDirectory() as folder:
        for text in EXPRESSIONS:
            tree = parse(text)
            value, written = run(code(tree, False), folder)
            value2, best = run(code(tree, True), folder)
            assert value == value2
            print(f"{text:<46} {value:>6} {written:>10} {best:>5} {ershov(tree):>7}")


if __name__ == "__main__":
    main()
