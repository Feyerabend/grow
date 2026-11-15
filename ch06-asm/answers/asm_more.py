#!/usr/bin/env python3
"""
asm.py with two additions, for exercises 6.2 and 6.4:

  * 'name EQU n' makes name stand for the number n, in any operand;
  * a warning, on standard error, for an instruction that can never be
    reached: one that follows JMP, RET or HALT and has no label.

    usage: asm_more.py program.asm program.vm
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import asm      # noqa: E402
import vmfile   # noqa: E402

NO_FALL_THROUGH = {"JMP", "RET", "HALT"}


def is_equ(line):
    return line.op is not None and len(line.operands) == 2 and line.operands[0].upper() == "EQU"


class Assembler(asm.Assembler):
    def __init__(self, path):
        super().__init__(path)
        self.constants = {}
        self.warnings = []

    def pass1(self, lines):
        # EQU first: a constant may be used above the line that gives it.
        for line in lines:
            if is_equ(line):
                name, value = line.op, asm.number(line.operands[1])
                if value is None:
                    self.error(line, f"EQU needs a number, found '{line.operands[1]}'")
                elif name in self.constants:
                    self.error(line, f"'{name}' is given twice")
                else:
                    self.constants[name] = value
                line.op, line.operands = None, []     # it writes no code
        super().pass1(lines)
        for name in self.constants:
            if name in self.labels:
                self.errors.append((0, f"{self.path}: '{name}' is both a label and a constant"))

    def operand(self, line, kind, word):
        if word in self.constants:
            return self.constants[word]
        return super().operand(line, kind, word)

    def pass2(self, lines):
        code = super().pass2(lines)
        previous = None
        for line in lines:
            if line.op is None:
                if line.labels:
                    previous = None             # a label: something may jump here
                continue
            if previous in NO_FALL_THROUGH and not line.labels:
                self.warnings.append(f"{self.path}:{line.number}: warning: "
                                     f"'{line.op}' can never be reached")
            previous = line.op.upper()
        return code


def main():
    source, target = sys.argv[1:]
    a = Assembler(source)
    _, code = a.assemble(open(source).read())
    for w in a.warnings:
        print(w, file=sys.stderr)
    if a.errors:
        sys.exit("\n".join(m for _, m in a.errors))
    vmfile.write(target, code)


if __name__ == "__main__":
    main()
