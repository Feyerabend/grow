#!/usr/bin/env python3
"""
expr.py with the additions of exercises 9.1, 9.2 and 9.4:

  * a missing ';' is reported where it was missing, just after the
    expression, not at the token that follows it;
  * '^' for powers, right-associative and binding tighter than unary minus:
    -2 ^ 2 is -(2 ^ 2), and 2 ^ 3 ^ 2 is 2 ^ 9;
  * an expression that needs more than the machine's 256 stack places is
    refused, and so is nesting deeper than MAX_NESTING, before Python's
    own limit is reached.

The grammar, with the new rule:

    unary  = "-" unary | power .
    power  = factor [ "^" unary ] .

    usage: expr_more.py program.expr
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import expr                                     # noqa: E402
from expr import Binary, CompileError, Negate, Number   # noqa: E402

STACK = 256
MAX_NESTING = 150       # this parser survives 164 levels, with Python's limit of 1000 calls

expr.OPERATORS += "^"


class Parser(expr.Parser):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.nesting = 0

    def program(self):
        statements = []
        while self.peek().kind != "end":
            node = self.expression()
            if self.peek().kind != ";":
                before = self.tokens[self.i - 1]
                raise CompileError("missing ';' after this expression",
                                   before.line, before.col + len(before.text))
            self.take(";")
            check_depth(node)
            statements.append(node)
        return statements

    def unary(self):
        if self.peek().kind == "-":
            token = self.take("-")
            return Negate(self.unary(), token)
        return self.power()

    def power(self):
        node = self.factor()
        if self.peek().kind == "^":
            token = self.take("^")
            node = Binary("^", node, self.unary(), token)   # right recursion: right-associative
        return node

    def factor(self):
        if self.peek().kind == "(":
            self.nesting += 1
            if self.nesting > MAX_NESTING:
                token = self.peek()
                raise CompileError(f"parentheses nested deeper than {MAX_NESTING}",
                                   token.line, token.col)
            node = super().factor()
            self.nesting -= 1
            return node
        return super().factor()


def depth(node):
    """The most stack places the code for node uses, in the order generate() writes it."""
    if isinstance(node, Number):
        return 1
    if isinstance(node, Negate):
        return max(1, 1 + depth(node.operand))         # PUSH 0, then the operand
    return max(depth(node.left), 1 + depth(node.right))


def check_depth(node):
    # Walk down to the deepest point, to say where the expression gets too deep.
    need = depth(node)
    if need <= STACK:
        return
    while True:
        if isinstance(node, Negate):
            node = node.operand
        elif isinstance(node, Binary) and 1 + depth(node.right) > STACK:
            node = node.right
        elif isinstance(node, Binary) and depth(node.left) > STACK:
            node = node.left
        else:
            break
    raise CompileError(f"this expression needs {need} stack places; the machine has {STACK}",
                       node.token.line, node.token.col)


# '^' as a call of a small function, pow(b, e): e times b, and 1 when e <= 0.
POW = """pow:    PUSH 1                  ; local 2: the product
powl:   LOAD 1
        PUSH 0
        SWAP
        LT                      ; 0 < e ?
        JZ powd
        LOAD 2
        LOAD 0
        MUL
        STORE 2
        LOAD 1
        PUSH 1
        SUB
        STORE 1
        JMP powl
powd:   LOAD 2
        RET
"""


def generate(node, out):
    if isinstance(node, Binary) and node.op == "^":
        generate(node.left, out)
        generate(node.right, out)
        out.append("        CALL pow 2")
    elif isinstance(node, Number):
        out.append(f"        PUSH {node.value}")
    elif isinstance(node, Negate):
        out.append("        PUSH 0")
        generate(node.operand, out)
        out.append("        SUB")
    else:
        generate(node.left, out)
        generate(node.right, out)
        out.append(f"        {expr.OPCODES[node.op]}")


def compile_program(statements):
    out = []
    for node in statements:
        out.append(f"; line {node.token.line}")
        generate(node, out)
        out.append("        PRINT")
    out.append("        HALT")
    return "\n".join(out) + "\n" + POW


def main():
    path = sys.argv[1]
    text = open(path).read()
    try:
        sys.stdout.write(compile_program(Parser(expr.scan(text)).program()))
    except CompileError as error:
        expr.report(path, text, error)
        sys.exit(1)


if __name__ == "__main__":
    main()
