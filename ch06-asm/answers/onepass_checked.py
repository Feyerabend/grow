#!/usr/bin/env python3
"""
Exercise 6.5: measure/onepass.py with the checks of asm.py. Each check is made
as soon as it can be: most at once, on the line itself. Only a label used before
it is defined must wait, and its error is known only at the end, when the
label has still not come; so each hole remembers the line that made it.
Errors are sorted by line, as asm.py's are, and must read the same.

    usage: python3 onepass_checked.py program.asm
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import asm      # noqa: E402
import isa      # noqa: E402


def one_pass(path, text):
    code, labels, holes, errors = [], {}, {}, []

    def error(line, message):
        errors.append((line.number, f"{path}:{line.number}: {message}"))

    def operand(line, kind, word):
        n = asm.number(word)
        if kind == "addr" and n is None and asm.NAME.match(word):
            if word in labels:
                return labels[word]
            holes.setdefault(word, []).append((len(code), line))
            return 0
        if n is None:
            error(line, f"expected a number, found '{word}'")
            return 0
        if not -2**31 <= n < 2**31:
            error(line, f"number out of range: {word}")
            return 0
        if kind == "k" and n < 0:
            error(line, f"a local number cannot be negative: {n}")
        return n

    for i, t in enumerate(text.splitlines(), 1):
        line = asm.parse_line(i, t)
        for name in line.labels:
            if name in labels:
                error(line, f"label '{name}' is defined twice")
                continue
            labels[name] = len(code)
            for place, _ in holes.pop(name, []):
                code[place] = len(code)
        if line.op is None:
            continue
        if line.op.lower() == ".word":
            if len(line.operands) != 1:
                error(line, ".word takes one number")
                code.append(0)
            else:
                code.append(operand(line, "n", line.operands[0]))
            continue
        entry = isa.BY_NAME.get(line.op.upper())
        if entry is None:
            error(line, f"unknown instruction '{line.op}'")
            code.append(0)
            continue
        op, kinds = entry
        if len(line.operands) != len(kinds):
            error(line, f"{line.op.upper()} takes {len(kinds)} "
                        f"operand{'' if len(kinds) == 1 else 's'}, found {len(line.operands)}")
            code.extend([op] + [0] * len(kinds))
            continue
        code.append(op)
        for kind, word in zip(kinds, line.operands):
            code.append(operand(line, kind, word))
    # Only now is it known which labels never came.
    for name, places in holes.items():
        for _, line in places:
            error(line, f"undefined label '{name}'")
    if not code and not errors:
        errors.append((0, f"{path}: no code"))
    errors.sort(key=lambda e: e[0])
    return code, errors


def main():
    path = sys.argv[1]
    text = open(path).read()
    code, errors = one_pass(path, text)
    two = asm.Assembler(path)
    _, expected = two.assemble(text)
    print("\n".join(m for _, m in errors) or "no errors")
    same = [m for _, m in errors] == [m for _, m in two.errors] and (errors or code == expected)
    print("asm.py says the same" if same else "asm.py differs:\n" + "\n".join(m for _, m in two.errors))


if __name__ == "__main__":
    main()
