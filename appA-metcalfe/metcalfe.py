#!/usr/bin/env python3
"""
Howard Metcalfe's syntax machine and editor machine, as his report of
1964 defines them ("A parameterized compiler based on mechanical
linguistics", Annual Review in Automatic Programming 4). Appendix A of
the book describes them.

The syntax machine has an input tape, an output tape, a flag of one bit,
a stack, and a program. Each entry on the stack holds a return address,
the place on each tape when the call was made, and a set of marks.
Its instructions, one to a line, with an optional label first:

    CALL l      push an entry, with its marks clear; go to l
    RETURN      if the flag is false, put both tapes back where they were
                at the call; then pop the entry and go back
    MATCH s     if the next input symbol is s, move past it and set the
                flag; if not, clear the flag
    TRUE l      go to l if the flag is set
    FALSE l     go to l if the flag is clear
    FLAG        set the flag
    STOP        stop, and show the flag
    PRINT s     write s on the output tape
    COPY        write the input symbol just read
    NULL        write a null symbol, which the editor leaves out
    EDIT c      write an edit code for the editor: C, X or W
    MARK n      set mark n in the caller's entry (the next to top)
    TEST n      set the flag to mark n of this routine's entry (the top)

The editor reads the syntax machine's output tape. A symbol is pushed
on its stack, whose entries are strings; C combines the top two into
one, the lower first; X exchanges them; W writes the whole stack out,
bottom first, and empties it. Emptying it is ours: Metcalfe's W writes
the stack, and his section on tape movement clears the stacks after
each W, for translating a statement at a time.

The input is one tape for each line of standard input. Each symbol is
one character, and blanks are left out, as in his programming language;
with -w, each symbol is a word, as in his English examples. Each line
shows the flag at STOP, where the machine stopped reading if it did not
read to the end (Metcalfe's machine shows only the flag), and what the
editor wrote, if it wrote anything.

    python3 metcalfe.py [-w] [-t] program.syn < lines

-t traces every instruction before it runs, as his report does: the
location, the flag, the stack of return addresses, the stack of input
positions, the input position, and the instruction. Positions count
from 1, as his do.
"""

import sys

OPERANDS = {"CALL": "label", "RETURN": None, "MATCH": "symbol", "TRUE": "label",
            "FALSE": "label", "FLAG": None, "STOP": None, "PRINT": "symbol",
            "COPY": None, "NULL": None, "EDIT": "code", "MARK": "mark", "TEST": "mark"}
NULL = object()


class Error(Exception):
    pass


def assemble(text):
    """A list of (function, data), and the labels' locations. A line is
    [label] function [data]; anything after ';' is a comment."""
    code, labels, lines = [], {}, []
    for number, line in enumerate(text.splitlines(), 1):
        words = line.split(";")[0].split()
        if not words:
            continue
        if words[0] not in OPERANDS:
            label, words = words[0], words[1:]
            if label in labels:
                raise Error(f"line {number}: label {label} twice")
            labels[label] = len(code)
            if not words:
                raise Error(f"line {number}: a label needs an instruction")
        function, data = words[0], words[1:]
        if function not in OPERANDS:
            raise Error(f"line {number}: no instruction {function}")
        kind = OPERANDS[function]
        if (kind is None) != (not data) or len(data) > 1:
            raise Error(f"line {number}: {function} takes "
                        f"{'no data' if kind is None else 'one ' + kind}")
        data = data[0] if data else None
        if kind == "code" and data not in ("C", "X", "W"):
            raise Error(f"line {number}: the edit codes are C, X and W")
        if kind == "mark":
            if not data.isdigit():
                raise Error(f"line {number}: a mark is a number")
            data = int(data)
        code.append((function, data))
        lines.append(number)
    for k, (function, data) in enumerate(code):
        if OPERANDS[function] == "label":
            if data not in labels:
                raise Error(f"line {lines[k]}: no label {data}")
            code[k] = (function, labels[data])
    return code, labels


def syntax(code, tape, trace=None, names=None):
    """Run the syntax machine on one input tape. Return the flag at STOP,
    the output tape, and how many input symbols were read."""
    pc, flag, at, out = 0, False, 0, []
    # The entry for the main routine is at the bottom, so that MARK and
    # TEST have an entry to use there too.
    stack = [{"ret": None, "at": 0, "out": 0, "marks": set()}]
    steps = 0
    while True:
        if pc >= len(code):
            raise Error("ran off the end of the program")
        function, data = code[pc]
        if trace is not None:
            shown = names.get(data, data) if OPERANDS[function] == "label" else data
            trace.append("%4d  %-5s  %-14s  %-14s  %3d   %s" % (
                pc, "True" if flag else "False",
                ",".join(str(e["ret"]) for e in stack[1:]),
                ",".join(str(e["at"] + 1) for e in stack[1:]),
                at + 1, function + ("" if shown is None else " " + str(shown))))
        steps += 1
        if steps > 1000000:
            raise Error("more than a million steps")
        pc += 1
        if function == "CALL":
            stack.append({"ret": pc, "at": at, "out": len(out), "marks": set()})
            pc = data
        elif function == "RETURN":
            if len(stack) == 1:
                raise Error("RETURN with no CALL")
            entry = stack.pop()
            if not flag:
                at = entry["at"]
                del out[entry["out"]:]
            pc = entry["ret"]
        elif function == "MATCH":
            flag = at < len(tape) and tape[at] == data
            if flag:
                at += 1
        elif function == "TRUE":
            if flag:
                pc = data
        elif function == "FALSE":
            if not flag:
                pc = data
        elif function == "FLAG":
            flag = True
        elif function == "STOP":
            return flag, out, at
        elif function == "PRINT":
            out.append(data)
        elif function == "COPY":
            if at == 0:
                raise Error("COPY with nothing read")
            out.append(tape[at - 1])
        elif function == "NULL":
            out.append(NULL)
        elif function == "EDIT":
            out.append(("EDIT", data))
        elif function == "MARK":
            if len(stack) < 2:
                raise Error("MARK in the main routine, which has no caller")
            stack[-2]["marks"].add(data)
        elif function == "TEST":
            flag = data in stack[-1]["marks"]


def editor(tape):
    """Run the editor on the syntax machine's output tape. Return what it
    wrote, a list of strings, one for each W."""
    stack, written = [], []
    for cell in tape:
        if isinstance(cell, tuple):
            code = cell[1]
            if code in ("C", "X") and len(stack) < 2:
                raise Error(f"edit code {code} with fewer than two entries")
            if code == "C":
                b, a = stack.pop(), stack.pop()
                stack.append(a + b)
            elif code == "X":
                stack[-1], stack[-2] = stack[-2], stack[-1]
            else:
                written.append(" ".join("".join(s for s in entry if s is not NULL)
                                        for entry in stack
                                        if any(s is not NULL for s in entry)))
                stack = []
        else:
            stack.append([cell])
    return written


def main(args):
    words = "-w" in args
    tracing = "-t" in args
    args = [a for a in args if a not in ("-w", "-t")]
    if len(args) != 1:
        sys.exit("usage: metcalfe.py [-w] [-t] program.syn < lines")
    try:
        with open(args[0]) as f:
            code, labels = assemble(f.read())
        names = {v: k for k, v in labels.items()}
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            tape = line.split() if words else [c for c in line if not c.isspace()]
            trace = [] if tracing else None
            flag, out, read = syntax(code, tape, trace, names)
            if tracing:
                print("loc   flag   return stack    tape stack      cell  instruction")
                print("\n".join(trace))
            written = [w for w in editor(out) if w]
            shown = "flag " + ("true" if flag else "false")
            if read < len(tape):
                shown += f", stopped at symbol {read + 1} of {len(tape)}"
            print(f"{line}  =>  {shown}" + "".join(f"; {w}" for w in written))
    except Error as e:
        sys.exit(f"metcalfe: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
