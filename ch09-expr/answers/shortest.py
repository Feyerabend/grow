#!/usr/bin/env python3
"""
Exercise 9.5: the planted mistake "a minus takes the whole term after it",
written into a copy of expr.py's parser, and a search for the shortest
expressions that show it: every expression of one-digit numbers and the
grammar's tokens, shortest first, compiled both ways and evaluated by
fuzz.py's rules, until the two disagree.

    usage: python3 shortest.py
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import expr                                     # noqa: E402
import fuzz                                     # noqa: E402
from expr import Binary, Negate, Number         # noqa: E402


class Mistaken(expr.Parser):
    """unary minus takes the whole term after it: -2 * 3 is -(2 * 3)."""

    def term(self):
        node = self.signed()
        while self.peek().kind in ("*", "/", "%"):
            token = self.take(self.peek().kind)
            node = Binary(token.kind, node, self.signed(), token)
        return node

    def signed(self):
        if self.peek().kind == "-":
            token = self.take("-")
            return Negate(self.term(), token)       # the mistake: a term, not a unary
        return self.factor()


def value(node):
    def as_tuple(n):
        if isinstance(n, Number):
            return ("num", n.value)
        if isinstance(n, Negate):
            return ("neg", as_tuple(n.operand))
        return (n.op, as_tuple(n.left), as_tuple(n.right))
    try:
        return fuzz.evaluate(as_tuple(node))
    except ZeroDivisionError:
        return "trap"


def both(text):
    try:
        right = expr.Parser(expr.scan(text + ";")).program()
        wrong = Mistaken(expr.scan(text + ";")).program()
    except expr.CompileError:
        return None
    return value(right[0]), value(wrong[0])


TOKENS = ["1", "2", "3", "-", "+", "*", "/", "%"]
for length in range(1, 8):
    found = []
    for words in itertools.product(TOKENS, repeat=length):
        text = "".join(words)
        if any(a.isdigit() and b.isdigit() for a, b in zip(words, words[1:])):
            continue                            # 1 2 would scan as 12
        r = both(text)
        if r and r[0] != r[1]:
            found.append(f"{text}: right {r[0]}, mistaken {r[1]}")
    if found:
        print(f"the shortest, {length} tokens, {len(found)} of them; the first five:")
        print("\n".join(found[:5]))
        break
    print(f"{length} tokens: none")
