#!/usr/bin/env python3
"""
Exercise 11.5: basal.py taking its tokens one at a time and writing its output
as it goes. The scanner reads a line at a time, desugaring works a line at a
time (it already did), and the translator asks for each token as it needs it,
with one token of lookahead, and writes each line of assembly the moment it
has it. basal.py's own code is used for every stage; only what holds the
tokens and the output is new.

    usage: basal_stream.py program.bas > program.asm
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import basal                                    # noqa: E402
from basal import CompileError                  # noqa: E402


def scan_lines(lines):
    """basal.scan, a line at a time: each line's tokens, its newline included."""
    number = 0
    for number, line in enumerate(lines, 1):
        tokens = basal.scan(line.rstrip("\n"))[:-1]     # not that line's end of file
        for token in tokens:
            token.line = number
            yield token
    yield basal.Token("end of file", "", number + 1, 1)


def desugar_stream(tokens):
    """basal.desugar, a line at a time."""
    loops, line = [], []
    for token in tokens:
        if token.kind not in ("newline", "end of file"):
            line.append(token)
            continue
        if token.kind == "end of file" and line:
            yield from one_line(line, token, loops)
        elif token.kind == "newline":
            yield from one_line(line, token, loops)
        line = []
        if token.kind == "end of file":
            if loops:
                raise CompileError("FOR without NEXT", loops[-1][2])
            yield token


def one_line(words, newline, loops):
    if words and words[0].kind == "FOR":
        return basal.desugar_for(words, newline, loops)
    if words and words[0].kind == "NEXT":
        return basal.desugar_next(words, newline, loops)
    if words and words[0].kind == "ON":
        return basal.desugar_on(words, newline)
    return words + [newline]


class Tokens:
    """What the translator indexes as a list: only the current token is kept."""

    def __init__(self, stream):
        self.stream = stream
        self.at, self.token = -1, None

    def __getitem__(self, i):
        while self.at < i:
            self.token = next(self.stream)
            self.at += 1
        return self.token


class Output:
    """What the translator appends its lines to: each is written at once."""

    def __init__(self, sink):
        self.sink = sink

    def append(self, line):
        self.sink.write(line + "\n")

    def __iadd__(self, lines):
        for line in lines:
            self.append(line)
        return self


class Translator(basal.Translator):
    def __init__(self, tokens, sink):
        super().__init__(Tokens(tokens))
        self.out = Output(sink)

    def program(self):
        self.statements(until=("end of file",))
        self.emit("HALT")
        for name, token in self.labels_used:
            if name not in self.labels_defined:
                raise CompileError(f"there is no label '{name}'", token)
        if self.needs_print:
            self.out += basal.PRINT_ROUTINE


def compile_stream(lines, sink):
    Translator(desugar_stream(scan_lines(lines)), sink).program()


def main():
    path = sys.argv[1]
    try:
        with open(path) as f:
            compile_stream(f, sys.stdout)
    except CompileError as error:
        basal.report(path, open(path).read(), error)
        sys.exit(1)


if __name__ == "__main__":
    main()
