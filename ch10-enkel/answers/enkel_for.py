#!/usr/bin/env python3
"""
Exercise 10.4: enkel.py with a for loop, made in the parser only.

    for i is a to b do S

is read as if it had been written

    begin i is a; while i <= b do begin S; i is i + 1 end end

so the resolver and the generator never see a for loop: the tree they get has
only nodes they know.

    usage: enkel_for.py program.p > program.asm
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import enkel                                    # noqa: E402
from enkel import (Assign, Binary, Block, Compare, Name, Number,   # noqa: E402
                   While)

enkel.KEYWORDS |= {"for", "to"}


class Parser(enkel.Parser):
    def statement(self):
        if not self.at("for"):
            return super().statement()
        token = self.take("for")
        name = self.take("name")
        self.take("is")
        first = self.expression()
        self.take("to")
        last = self.expression()
        self.take("do")
        body = self.statement()

        def var():                              # a fresh node for each use of i
            return Name(name, name=name.text)

        step = Assign(token, target=var(),
                      value=Binary(token, op="+", left=var(), right=Number(token, value=1)))
        loop = While(token, condition=Compare(token, op="<=", left=var(), right=last),
                     body=Block(token, statements=[body, step]))
        return Block(token, statements=[Assign(token, target=var(), value=first), loop])


enkel.Parser = Parser
enkel.main()
