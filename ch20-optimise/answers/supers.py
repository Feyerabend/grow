#!/usr/bin/env python3
"""
Superinstructions made by a program, for exercises 20.2 and 20.3.

    import supers
    binary = supers.build(folder, [("LOAD", "PUSH"), ("LOAD", "PUSH", "SUB"), ...])

Each superinstruction is the bodies of its instructions, taken from ops.h
as they are, one after another, with start = pc++ between them, as in the
chapter's super.h: start moves on to the next instruction, so that a trap
there names its address, and pc steps over its opcode. The NEXT at the end
of each body but the last is left out. Since the code is the instructions'
own, every check and every trap is theirs, in the same order; what is lost
is only what the hand-written super.h gains by not pushing a value that is
popped at once.

Where several superinstructions could begin at an address, the longest is
used, and among those of one length, the one listed first. No instruction
but the last may change pc: HALT, JMP, JZ, CALL, CALLI and RET can only
end one.
"""

import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
CC = os.environ.get("CC", "cc")
CONTROL = {"HALT", "JMP", "JZ", "CALL", "CALLI", "RET"}


def bodies():
    ops = open(os.path.join(CHAPTER, "ops.h")).read()
    out = {}
    for m in re.finditer(r"OP\((\w+)\) \{\n(.*?)\n\}\n", ops, re.S):
        out[m.group(1)] = m.group(2)
    return out


def header(sequences):
    body = bodies()
    lines = ["/* Made by answers/supers.py: each superinstruction is the bodies of",
             " * its instructions from ops.h, one after another. */", ""]
    for seq in sequences:
        assert all(op not in CONTROL for op in seq[:-1]), seq
        lines.append("L_%s: {" % "_".join(seq))
        for k, op in enumerate(seq):
            text = body[op]
            if k < len(seq) - 1:
                assert text.rstrip().endswith("NEXT;"), op
                text = text.rstrip()[:-len("NEXT;")].rstrip()
            if k > 0:
                lines.append("    start = pc++;                       /* %s */" % op)
            lines.append("    {")
            lines += ["    " + line for line in text.splitlines()]
            lines.append("    }")
        lines.append("}")
    return "\n".join(lines) + "\n"


def fusing(sequences):
    """The C that replaces vm.c's chain of ifs: try the longest first."""
    lines = []
    for seq in sorted(sequences, key=len, reverse=True):
        tests = []
        for k, op in enumerate(seq):
            tests.append("n >= %d && ops[%d] == %s" % (k + 1, k, op))
        lines.append("        if (fused == NULL && %s)" % " && ".join(tests))
        lines.append("            fused = &&L_%s;" % "_".join(seq))
    return "\n".join(lines)


OLD_FUSE_START = "    for (a = 0; a < code_len; a++) {\n        int op1 = code[a], b, op2;"
OLD_FUSE_END = "        if (fused != NULL)\n            thread[a] = fused;\n    }"

NEW_FUSE = """    for (a = 0; a < code_len; a++) {
        int ops[3], n = 0, b = a;
        void *fused = NULL;

        /* The next three complete instructions from a, as far as they go. */
        while (n < 3 && b < code_len && code[b] >= 0 && code[b] < NOPS
               && b + noperands[code[b]] < code_len) {
            ops[n++] = code[b];
            b += 1 + noperands[code[b]];
        }
%s
        if (fused != NULL)
            thread[a] = fused;
    }"""


def source(sequences):
    s = open(os.path.join(CHAPTER, "vm.c")).read()
    i = s.index(OLD_FUSE_START)
    j = s.index(OLD_FUSE_END, i) + len(OLD_FUSE_END)
    return s[:i] + NEW_FUSE % fusing(sequences) + s[j:]


def build(folder, sequences, name="vm-auto"):
    os.makedirs(folder, exist_ok=True)
    open(os.path.join(folder, "vm.c"), "w").write(source(sequences))
    open(os.path.join(folder, "super.h"), "w").write(header(sequences))
    ops = os.path.join(folder, "ops.h")
    if not os.path.exists(ops):
        os.symlink(os.path.join(CHAPTER, "ops.h"), ops)
    binary = os.path.join(folder, name)
    subprocess.run([CC, "-std=gnu99", "-O2", "-Wall", "-Wextra", "-DDISPATCH=THREADED",
                    "-DSUPER", "-o", binary, os.path.join(folder, "vm.c")], check=True)
    return binary


CHAPTER_EIGHT = [("LOAD", "PUSH"), ("LOAD", "LOAD"), ("LOAD", "ADD"), ("LT", "JZ"),
                 ("PUSH", "SUB"), ("PUSH", "ADD"), ("PUSH", "LOADM"), ("ADD", "STORE")]
