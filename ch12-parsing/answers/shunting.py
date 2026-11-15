"""
Parser 4: Dijkstra's shunting-yard algorithm, from chapter 9, with a stack
instead of recursion.

Operators wait on a stack of their own; operands, as they are made into
trees, on another. An operator coming in first sends to the trees every
operator waiting that binds at least as tightly (that "at least" makes them
group to the left), then waits itself. A '(' waits until its ')' comes, and
shields what is under it. The minus in front of an operand is an operator of
one operand, binding tightest of all, and it sends nothing out, since there is
nothing to its left.

The program is read one token at a time, and whether an operand or an
operator is wanted next is the only thing the parser needs to know about the
grammar.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import Binary, CompileError, Negate, found, number   # noqa: E402

POWER = {"<": 10, "=": 10, "+": 20, "-": 20, "*": 30, "/": 30, "%": 30}
NEGATE = 40


def expression(tokens, i):
    """One expression from tokens[i]; returns its tree and where it stopped."""
    operators, trees = [], []         # operators: (kind, power, token)

    def reduce():
        kind, _, token = operators.pop()
        if kind == "neg":
            trees.append(Negate(trees.pop(), token))
        else:
            right, left = trees.pop(), trees.pop()
            trees.append(Binary(kind, left, right, token))

    want_operand = True
    while True:
        token = tokens[i]
        if want_operand:
            if token.kind == "number":
                trees.append(number(token))
                want_operand = False
            elif token.kind == "(":
                operators.append(("(", 0, token))
            elif token.kind == "-":
                operators.append(("neg", NEGATE, token))
            else:
                raise CompileError(f"expected a number or '(', found {found(token)}", token)
        elif token.kind in POWER:
            power = POWER[token.kind]
            while operators and operators[-1][0] != "(" and operators[-1][1] >= power:
                reduce()
            operators.append((token.kind, power, token))
            want_operand = True
        elif token.kind == ")" and any(op[0] == "(" for op in operators):
            while operators[-1][0] != "(":
                reduce()
            operators.pop()
        else:
            break                             # the end of this expression
        i += 1
    for kind, _, token in operators:
        if kind == "(":
            raise CompileError(f"expected ')', found {found(tokens[i])}", tokens[i])
    while operators:
        reduce()
    return trees[0], i


def parse(tokens):
    statements, i = [], 0
    while tokens[i].kind != "end":
        tree, i = expression(tokens, i)
        if tokens[i].kind != ";":
            raise CompileError(f"expected ';', found {found(tokens[i])}", tokens[i])
        statements.append(tree)
        i += 1
    return statements
