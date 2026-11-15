#!/usr/bin/env python3
"""
basal.py with the additions of exercises 11.1, 11.2 and 11.6:

  INPUT X       reads a number into X, with the machine's new READ
                instruction (code 27, in this chapter's copy only);
  FOR           evaluates its limit once, into a hidden variable that no
                program can name, since its name has a space in it;
  GOTO          out of a subroutine is reported, where the compiler can tell:
                see subroutines() below.

    usage: basal_more.py program.bas > program.asm
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import basal                                    # noqa: E402
from basal import CompileError, make            # noqa: E402

basal.KEYWORDS.add("INPUT")


class Translator(basal.Translator):
    def statement(self):
        if self.at("INPUT"):
            token = self.take("INPUT")
            self.out.append(f"; {token.line}")
            name = self.take("name")
            self.emit(f"PUSH {self.address(name.text)}")
            self.emit("READ")
            self.emit("STOREM")
            if not self.at("end of file"):
                self.take("newline")
            return
        super().statement()


# 11.2: FOR's limit into a hidden variable, evaluated once.
hidden = [0]


def desugar_for(words, newline, loops):
    tokens = basal_desugar_for(words, newline, loops)
    # tokens: LET v = start NL  WHILE v cmp limit... DO NL
    w = next(i for i, t in enumerate(tokens) if t.kind == "WHILE")
    do = next(i for i, t in enumerate(tokens) if t.kind == "DO")
    limit = tokens[w + 3:do]
    hidden[0] += 1
    name = make("name", words[0], f"for limit {hidden[0]}")
    return (tokens[:w] + [make("LET", words[0]), name, make("=", words[0])] + limit + [newline] +
            tokens[w:w + 3] + [name] + tokens[do:])


basal_desugar_for = basal.desugar_for
basal.desugar_for = desugar_for


# 11.6: GOTO out of a subroutine.
def subroutines(tokens):
    """
    A subroutine, here, is the lines from a label that some GOSUB names to the
    first RETURN after it. A GOTO on those lines to a label outside them is an
    error. The compiler can tell only for this shape: it cannot when code is
    reached both by GOSUB and by GOTO, when a subroutine has more than one
    RETURN on different paths, or when the jump is ON ... GOTO, decided while
    running; then the span it finds is a guess, and a GOTO it passes may still
    leave the subroutine.
    """
    lines, _ = basal.statement_lines(tokens)
    labels = {}                                 # label -> its line index
    gosub, gotos = set(), []
    for k, (words, _) in enumerate(lines):
        kinds = [w.kind for w in words]
        if kinds[:1] == ["!"] and len(words) > 1:
            labels[words[1].text] = k
        if "GOSUB" in kinds:
            gosub.add(words[kinds.index("GOSUB") + 1].text)
        if "GOTO" in kinds:
            target = words[kinds.index("GOTO") + 1]
            gotos.append((k, target))
    for name in gosub:
        if name not in labels:
            continue
        start = labels[name]
        end = next((k for k in range(start, len(lines))
                    if any(w.kind == "RETURN" for w in lines[k][0])), len(lines) - 1)
        for k, target in gotos:
            if start <= k <= end and target.text in labels and not start <= labels[target.text] <= end:
                raise CompileError(f"GOTO {target.text} leaves the subroutine {name}, "
                                   f"lines {lines[start][0][0].line} to {lines[end][0][0].line}", target)


def main():
    path = sys.argv[1]
    text = open(path).read()
    try:
        tokens = basal.desugar(basal.scan(text))
        subroutines(tokens)
        sys.stdout.write(Translator(tokens).program())
    except CompileError as error:
        basal.report(path, text, error)
        sys.exit(1)


if __name__ == "__main__":
    main()
