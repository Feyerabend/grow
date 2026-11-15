#!/usr/bin/env python3
"""
Exercise 10.2: enkel.py with calls as expressions, print gcd[15, 6].

  grammar    factor = ... | name "[" [ expression { "," expression } ] "]" .
             A name followed by "[" is a call, wherever a value may stand.
  resolver   a call in an expression is checked as a call statement is:
             the procedure exists, and gets as many arguments as it takes.
  generator  a call in an expression leaves the value its RET carries on the
             stack, instead of dropping it; and return e carries e back that
             way, so rval is no longer needed, and no longer set.

    usage: enkel_calls.py program.p > program.asm
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import enkel                                    # noqa: E402
from enkel import Call, Return                  # noqa: E402


class Parser(enkel.Parser):
    def factor(self):
        if self.at("name") and self.tokens[self.i + 1].kind == "[":
            token = self.peek()
            name = self.take("name")
            self.take("[")
            args = []
            if not self.at("]"):
                args.append(self.expression())
                while self.at(","):
                    self.take(",")
                    args.append(self.expression())
            self.take("]")
            return Call(token, name=name, args=args)
        return super().factor()


class Resolver(enkel.Resolver):
    def value(self, node, assigning=False):
        if type(node) is Call:
            self.statement(node)                 # the same checks as a call statement
        else:
            super().value(node, assigning)


class Generator(enkel.Generator):
    def value(self, node):
        if type(node) is Call:
            for arg in node.args:
                self.value(arg)
            self.emit(f"CALL p_{node.procedure.name.text} {len(node.args)}")
        else:
            super().value(node)

    def statement(self, node):
        if type(node) is Return and node.in_procedure:
            self.note(node.token)
            if node.value:
                self.value(node.value)
            else:
                self.emit("PUSH 0")
            self.emit("RET")
        else:
            super().statement(node)


enkel.Parser, enkel.Resolver, enkel.Generator = Parser, Resolver, Generator
enkel.main()
