"""
The changes made to pcom.p and pint.p before they are compiled. The two
files here are kept exactly as they were downloaded from Pemberton's
page; the Makefile passes them through this.

    python3 adapt.py pcom < pcom.p > build/pcom.p   for Free Pascal
    python3 adapt.py self < pcom.p > build/self.p   for pcom itself
    python3 adapt.py pint < pint.p > build/pint.p   for Free Pascal

Both forms of pcom get one change of meaning:

    ordmaxchar = 63 becomes 127. P4 was written for the CDC 6000, whose
    characters were six bits, so its char runs from 0 to 63. In ASCII
    every capital letter is above 63, and passing 'A' to a parameter of
    type char fails the range check. pcom fills its tables of
    characters from 0 to ordmaxchar, and nothing in it is a set of
    char, so nothing else changes.

pcom for Free Pascal: two changes, neither of which changes the code it
makes.

1. The debug dump of the compiler's tables (lines 720 to 830) prints
   pointers as numbers with ord, which Free Pascal refuses. ptrint is
   its name for the same thing.
2. genlabel(pfname) passes a field of a packed record as a var
   parameter, which Free Pascal refuses. The two lines do what genlabel
   does, in place.

pcom for itself: four lines go.

1. The two Pemberton's page says to comment out, since the machine, not
   the program, declares and opens prr.
2. The two that make mark and release procedures that do nothing (lines
   300 and 301), put there for compilers that have neither, as Free
   Pascal has not. P4 has both, and without these lines pcom uses them:
   the heap it takes for each procedure's names it gives back when the
   procedure is compiled. With the empty ones, pcom compiling itself
   needs about 22300 words of stack and heap, and pint has 13650.

pint for Free Pascal: one problem, in two parts. Its store is an array
of variant records, one variant for each type, and it was written, a
note at its head says, "for the case where all the fundamental types take
one storage unit", as they did on the CDC 6000. pint writes a word as one
variant and sometimes reads it as another: an address written as va is
read as vi by eof, a character written as vc is read as vi by chk, xjp
and ixa. Under Free Pascal the variants differ in size: an integer is
four bytes, the address subrange two, a char and a boolean one. A
narrow write leaves the rest of the word as it was, and the wide read
sees it.

1. The address type becomes integer, as wide as vi.
2. Every assignment to a char or boolean variant writes the whole word:
   store[x].vc := e becomes store[x].vi := ord(e). Read back as vc or
   vb, the word gives the char or the boolean again, since this
   computer (arm64) is little-endian and they are its lowest byte.
"""

import re
import sys


def replace(lines, number, old, new):
    """Replace old by new on the line with this number, which must hold it."""
    assert old in lines[number - 1], (number, old)
    lines[number - 1] = lines[number - 1].replace(old, new)


def ascii(lines):
    replace(lines, 52, "ordmaxchar  =     63;", "ordmaxchar  =    127;")


def pcom(text):
    lines = text.split("\n")
    ascii(lines)
    for n in range(720, 831):
        lines[n - 1] = lines[n - 1].replace("ord(", "ptrint(")
    for n in (3787, 3793):
        replace(lines, n, "genlabel(pfname)",
                "intlabel := intlabel + 1; pfname := intlabel")
    return "\n".join(lines)


def itself(text):
    lines = text.split("\n")
    ascii(lines)
    replace(lines, 194, "prr: text;", "(* prr: text; *)")
    replace(lines, 3995, "rewrite(prr);", "(* rewrite(prr); *)")
    for n in (300, 301):
        assert lines[n - 1].strip().startswith(("procedure mark", "procedure release"))
        lines[n - 1] = "(* " + lines[n - 1] + " *)"
    return "\n".join(lines)


WORDS = re.compile(r"\b(end|else|until)\b")


def statement_end(text, i):
    """Where the expression that starts at i ends: at a ; or an end, else
    or until outside brackets."""
    depth = 0
    while i < len(text):
        c = text[i]
        if c in "([":
            depth += 1
        elif c in ")]":
            if depth == 0:
                return i
            depth -= 1
        elif depth == 0:
            if c == ";":
                return i
            if WORDS.match(text, i) and not text[i - 1].isalnum():
                return i
        i += 1
    raise ValueError("no end of statement")


def pint(text):
    old = "address     = -1..maxstr;"
    assert text.count(old) == 1
    text = text.replace(old, "address     = integer;")
    out = []
    i = 0
    count = 0
    for m in re.finditer(r"\.v[cb] *:=", text):
        end = statement_end(text, m.end())
        rhs = text[m.end():end].rstrip()
        rest = text[m.end() + len(rhs):end]
        out.append(text[i:m.start()])
        out.append(".vi := ord(" + rhs.strip() + ")" + rest)
        i = end
        count += 1
    out.append(text[i:])
    assert count == 55, count
    return "".join(out)


if __name__ == "__main__":
    change = {"pcom": pcom, "self": itself, "pint": pint}[sys.argv[1]]
    sys.stdout.write(change(sys.stdin.read()))
