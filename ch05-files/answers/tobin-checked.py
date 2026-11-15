#!/usr/bin/env python3
"""
Turn a text listing of a program into a .vm file.

The listing is a sequence of words separated by spaces or new lines.
A word is either an instruction name, which becomes its code, or a
number, which is written as it is. Everything from '#' to the end of
a line is a comment.

    PUSH 2 PUSH 3 ADD PRINT HALT     # prints 5

This is deliberately not an assembler: there are no labels, so jump
addresses are still counted by hand. Chapter 6 fixes that.

    usage: tobin.py program.txt program.vm
"""

import struct
import sys

NAMES = [
    "HALT", "PUSH", "ADD", "SUB", "MUL", "PRINT",
    "JMP", "JZ", "DUP", "DROP", "SWAP", "OVER", "ROT", "LT", "EQ",
    "LOAD", "STORE", "CALL", "RET",
    "DIV", "MOD",
]
CODES = {name: code for code, name in enumerate(NAMES)}


def words(text):
    for line_no, line in enumerate(text.splitlines(), 1):
        for word in line.split("#", 1)[0].split():
            yield line_no, word


# How many numbers follow each instruction that takes any.
OPERANDS = {"PUSH": 1, "JMP": 1, "JZ": 1, "LOAD": 1,
            "STORE": 1, "CALL": 2}


def translate(text, path):
    code = []
    due = 0                     # operands still owed to the last instruction
    for line_no, word in words(text):
        name = word.upper()
        if name in CODES:
            if due:
                sys.exit(f"{path}:{line_no}: '{word}' where a number was due")
            code.append(CODES[name])
            due = OPERANDS.get(name, 0)
            continue
        if not due:
            sys.exit(f"{path}:{line_no}: a number where an instruction was due '{word}'")
        due -= 1
        try:
            n = int(word)
        except ValueError:
            sys.exit(f"{path}:{line_no}: unknown instruction '{word}'")
        if not -2**31 <= n < 2**31:
            sys.exit(f"{path}:{line_no}: number out of range '{word}'")
        code.append(n)
    if due:
        sys.exit(f"{path}: the last instruction is missing a number")
    if not code:
        sys.exit(f"{path}: no code")
    return code


def write(code, path):
    with open(path, "wb") as f:
        f.write(b"SVM\x01")
        f.write(struct.pack("<i", len(code)))
        f.write(struct.pack(f"<{len(code)}i", *code))


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: tobin.py program.txt program.vm")
    source, target = sys.argv[1], sys.argv[2]
    with open(source) as f:
        code = translate(f.read(), source)
    write(code, target)


if __name__ == "__main__":
    main()
