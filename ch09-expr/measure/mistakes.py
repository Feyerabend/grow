#!/usr/bin/env python3
"""
Seven wrong parsers, and how many of the random expressions each one gets wrong.

Each mistake is a small change to one or two methods of expr.py's Parser, the
kind of change a first parser is likely to have. The random programs are
fuzz.py's, as `make test` makes them (seed 1, 500 expressions), and then nine
more seeds. Every program goes the whole way: the changed compiler, asm.py,
and the machine, ./vm. A line counts as wrong when the machine prints something
other than what fuzz.py worked out.

    usage: python3 measure/mistakes.py          (run in code/ch09-expr, after make vm)
"""

import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.getcwd())
import expr                                      # noqa: E402
import fuzz                                      # noqa: E402
from expr import Binary, Negate                  # noqa: E402

Parser = expr.Parser
RIGHT = dict(expression=Parser.expression, term=Parser.term, unary=Parser.unary)


def right_expression(self):
    node = self.term()
    if self.peek().kind in ("+", "-"):
        token = self.take(self.peek().kind)
        return Binary(token.kind, node, self.expression(), token)
    return node


def right_term(self):
    node = self.unary()
    if self.peek().kind in ("*", "/", "%"):
        token = self.take(self.peek().kind)
        return Binary(token.kind, node, self.term(), token)
    return node


def one_level(self):
    node = self.unary()
    while self.peek().kind in ("+", "-", "*", "/", "%"):
        token = self.take(self.peek().kind)
        node = Binary(token.kind, node, self.unary(), token)
    return node


def swapped_expression(self):                    # * / % outside, + - inside
    node = self.term()
    while self.peek().kind in ("*", "/", "%"):
        token = self.take(self.peek().kind)
        node = Binary(token.kind, node, self.term(), token)
    return node


def swapped_term(self):
    node = self.unary()
    while self.peek().kind in ("+", "-"):
        token = self.take(self.peek().kind)
        node = Binary(token.kind, node, self.unary(), token)
    return node


def signed(self):                                # -2 * 3 read as -(2 * 3), 8 / -2 / 2 as 8 / -(2 / 2)
    if self.peek().kind == "-":
        token = self.take("-")
        return Negate(self.signed(), token)
    return self.term()


def loose_minus_expression(self):
    node = self.signed()
    while self.peek().kind in ("+", "-"):
        token = self.take(self.peek().kind)
        node = Binary(token.kind, node, self.signed(), token)
    return node


def loose_minus_term(self):                      # 2 * -3 * 4 read as 2 * -(3 * 4)
    node = self.factor()
    while self.peek().kind in ("*", "/", "%"):
        token = self.take(self.peek().kind)
        right = self.signed() if self.peek().kind == "-" else self.factor()
        node = Binary(token.kind, node, right, token)
    return node


def mod_expression(self):                        # % with + and -
    node = self.term()
    while self.peek().kind in ("+", "-", "%"):
        token = self.take(self.peek().kind)
        node = Binary(token.kind, node, self.term(), token)
    return node


def mod_term(self):
    node = self.unary()
    while self.peek().kind in ("*", "/"):
        token = self.take(self.peek().kind)
        node = Binary(token.kind, node, self.unary(), token)
    return node


MISTAKES = [
    ("+ and - group to the right", dict(expression=right_expression)),
    ("* / % group to the right", dict(term=right_term)),
    ("all five operators at one level", dict(expression=one_level)),
    ("+ binds tighter than *", dict(expression=swapped_expression, term=swapped_term)),
    ("% at the level of + and -", dict(expression=mod_expression, term=mod_term)),
    ("minus takes the whole term after it", dict(expression=loose_minus_expression,
                                       term=loose_minus_term)),
]


def value(node):
    """What the machine prints for one tree, worked out by fuzz.py's rules."""
    def tuple_of(n):
        if isinstance(n, expr.Number):
            return ("num", n.value)
        if isinstance(n, Negate):
            return ("neg", tuple_of(n.operand))
        return (n.op, tuple_of(n.left), tuple_of(n.right))
    try:
        return str(fuzz.evaluate(tuple_of(node)))
    except ZeroDivisionError:
        return "trap"


def one_by_one(source, want):
    """Expressions wrong on their own: a wrong value, or a trap."""
    trees = expr.parse(expr.scan(source))
    return sum(value(t) != w for t, w in zip(trees, want))


def run(source, work):
    asm = os.path.join(work, "p.asm")
    vm = os.path.join(work, "p.vm")
    with open(asm, "w") as f:
        f.write(expr.compile_program(expr.parse(expr.scan(source))))
    subprocess.run([sys.executable, "asm.py", asm, vm], check=True)
    out = subprocess.run(["./vm", vm], capture_output=True, text=True)
    return out.stdout.splitlines()


def main():
    Parser.signed = signed
    seeds = range(1, 11)
    with tempfile.TemporaryDirectory() as work:
        programs = []
        for seed in seeds:
            p, e = os.path.join(work, "f.expr"), os.path.join(work, "f.out")
            fuzz.main.__globals__["sys"].argv = ["fuzz.py", str(seed), "500", p, e]
            fuzz.main()
            programs.append((open(p).read(), open(e).read().splitlines()))
        right = [run(src, work) for src, _ in programs]
        for (src, want), got in zip(programs, right):
            assert got == want, "the right parser is wrong"
        print("of 500 expressions, seed 1, and the least and most over seeds 1 to 10:")
        print("lines the whole program prints wrong; expressions wrong one by one\n")
        for name, change in MISTAKES:
            for method, f in change.items():
                setattr(Parser, method, f)
            whole, alone = [], []
            for src, want in programs:
                got = run(src, work)
                whole.append(sum(a != b for a, b in zip(got, want)) + abs(len(got) - len(want)))
                alone.append(one_by_one(src, want))
            for method, f in RIGHT.items():
                setattr(Parser, method, f)
            print(f"  {name:36} {whole[0]:4} ({min(whole):3} to {max(whole):3})"
                  f"   {alone[0]:4} ({min(alone):3} to {max(alone):3})")


if __name__ == "__main__":
    main()
