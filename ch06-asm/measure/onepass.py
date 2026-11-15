#!/usr/bin/env python3
"""
The same assembler in one pass. It reads the source once, writing words as it
goes; a label not yet defined becomes a hole, a 0 with a note of where it is,
and every hole is filled when its label turns up. It uses asm.py's own reading
of a line and its table of instructions, and only correct programs: the checks
are asm.py's business. Checked against asm.py on every sample here and every
file of chapter 8's suite: the words must be the same.

    usage: python3 measure/onepass.py      (from ch06-asm)
"""

import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asm      # noqa: E402
import isa      # noqa: E402


def one_pass(text):
    code, labels, holes = [], {}, {}       # holes: label -> places waiting for it
    for i, t in enumerate(text.splitlines(), 1):
        line = asm.parse_line(i, t)
        for name in line.labels:
            labels[name] = len(code)
            for place in holes.pop(name, []):
                code[place] = len(code)    # fill every hole left for it
        if line.op is None:
            continue
        if line.op.lower() == ".word":
            code.append(int(line.operands[0], 0))
            continue
        op, kinds = isa.BY_NAME[line.op.upper()]
        code.append(op)
        for kind, word in zip(kinds, line.operands):
            if kind == "addr" and not word.lstrip("-").isdigit():
                if word in labels:
                    code.append(labels[word])
                else:
                    holes.setdefault(word, []).append(len(code))
                    code.append(0)
            else:
                code.append(int(word, 0))
    assert not holes, f"labels never defined: {sorted(holes)}"
    return code, sum(1 for _ in labels)


def main():
    files = sorted(f for f in glob.glob("samples/*.asm") if ".dis." not in f)
    files += sorted(glob.glob("../ch08-spec/suite/*.asm"))
    same = 0
    for path in files:
        text = open(path).read()
        two = asm.Assembler(path)
        _, expected = two.assemble(text)
        if two.errors:
            continue                       # a test of the checks, not a program
        got, _ = one_pass(text)
        assert got == expected, path
        same += 1
    print(f"{same} programs: one pass and two passes give the same words")


if __name__ == "__main__":
    main()
