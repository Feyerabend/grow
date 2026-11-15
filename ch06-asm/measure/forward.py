#!/usr/bin/env python3
"""
How many uses of a label come before the label is defined? Those are the ones
a one-pass assembler cannot fill in on the spot. Counted over every assembly
file of the chapters in the book's code, by line order, each distinct file
once, leaving out the one test made only to nest 256 calls; not the answers,
and not the appendices, some of whose machines have assembly languages of
their own.

    usage: python3 measure/forward.py [code]     (default .., the book's code)
"""

import os
import re
import sys

LABEL = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_.]*):")
WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_.]*")


def scan(path):
    lines = []
    for raw in open(path, encoding="utf-8", errors="replace"):
        line = raw.split(";")[0]
        labels = []
        while True:
            m = LABEL.match(line)
            if not m:
                break
            labels.append(m.group(1))
            line = line[m.end():]
        lines.append((labels, line))
    defined = {}
    for i, (labels, _) in enumerate(lines):
        for name in labels:
            defined.setdefault(name, i)
    forward = backward = 0
    for i, (_, rest) in enumerate(lines):
        words = WORD.findall(rest)
        for w in words[1:]:                    # operands, not the instruction's name
            if w in defined:
                if defined[w] > i:
                    forward += 1
                else:
                    backward += 1
    return forward, backward


def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else ".."
    files = forward = backward = 0
    seen = set()
    for top, dirs, names in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in ("archive", ".git", "build", "book", "answers")
                   and not (top == repo and d.startswith("app"))]
        for n in names:
            if n.endswith(".asm") and ".dis." not in n:
                path = os.path.join(top, n)
                text = open(path, "rb").read()
                if text in seen:            # the same file, copied into another chapter
                    continue
                seen.add(text)
                if n == "trap-too-deep.asm":    # 256 nested calls, made to trap: not a program
                    continue
                f, b = scan(path)
                files += 1
                forward += f
                backward += b
    total = forward + backward
    print(f"{files} files, {total} uses of labels")
    print(f"forward, used before defined:  {forward} ({100 * forward / total:.0f}%)")
    print(f"backward, used after defined:  {backward} ({100 * backward / total:.0f}%)")


if __name__ == "__main__":
    main()
