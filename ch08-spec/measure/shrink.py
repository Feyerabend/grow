#!/usr/bin/env python3
"""
Shrinking, the other half of property-based testing. The property is that
vm.c and a machine agree on a program. Programs are tried until one
breaks it, from two generators: fuzz.py's random ones, and programs shaped for
the property, which compute something and print it; then the program is made smaller, a word at a time and by making
operands smaller, for as long as it still breaks the property. What is left is
a program short enough to read.

Run against each planted mistake of fuzz.py.

    usage: python3 measure/shrink.py [seed] [computing]      (from ch08-spec)
"""

import os
import random
import subprocess
import sys
import tempfile

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "measure"))
import fuzz       # noqa: E402
import isa        # noqa: E402
import vmfile     # noqa: E402


def computing(rng):
    """A program shaped for the property: two numbers, one operation, print, halt.
    The numbers are small, negative, or anywhere in 32 bits."""
    def number():
        return rng.choice([rng.randrange(-9, 10), rng.randrange(-2**31, 2**31)])
    op = rng.choice(["ADD", "SUB", "MUL", "DIV", "MOD", "LT", "EQ"])
    code = isa.BY_NAME
    return [code["PUSH"][0], number(), code["PUSH"][0], number(), code[op][0],
            code["PRINT"][0], code["HALT"][0]]


def differs(words, exe, mutant, folder):
    path = os.path.join(folder, "s.vm")
    vmfile.write(path, words or [0])
    return fuzz.run([exe], path) != fuzz.run([sys.executable, mutant], path)


def smaller(words):
    """Candidates a little simpler than words: one word gone, or one made smaller."""
    for i in range(len(words)):
        yield words[:i] + words[i + 1:]
    for i, w in enumerate(words):
        for v in (0, 1, -1, int(w / 2)):          # towards zero, never the same
            if abs(v) < abs(w):
                yield words[:i] + [v] + words[i + 1:]


def shrink(words, test):
    changed = True
    while changed:
        changed = False
        for candidate in smaller(words):
            if test(candidate):
                words, changed = candidate, True
                break
    return words


def show(words):
    out, i = [], 0
    while i < len(words):
        name, kinds = isa.BY_CODE.get(words[i], (".word", ()))
        out.append(" ".join([name] + [str(w) for w in words[i + 1:i + 1 + len(kinds)]]))
        i += 1 + len(kinds)
    return "; ".join(out)


GENERATORS = [("random", fuzz.program), ("computing", computing)]


def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    if sys.argv[2:] == ["computing"]:          # the random ones take half an hour
        GENERATORS[:] = [g for g in GENERATORS if g[0] == "computing"]
    source = open("vm.py").read()
    with tempfile.TemporaryDirectory() as folder:
        exe = os.path.join(folder, "vm")
        subprocess.run(["cc", "-std=c99", "-O1", "-o", exe, "vm.c"], check=True)
        mutant = os.path.join(os.getcwd(), "_mutant.py")
        try:
            for what, (old, new) in fuzz.MUTANTS.items():
                open(mutant, "w").write(source.replace(old, new))
                test = lambda w: differs(w, exe, mutant, folder)     # noqa: E731
                print(f"{what}:")
                for kind, make in GENERATORS:
                    for tries in range(1, 2001):
                        words = make(rng)
                        if test(words):
                            small = shrink(words, test)
                            print(f"    {kind}: found after {tries}, {len(words)} words;"
                                  f" shrunk to {len(small)}: {show(small)}")
                            break
                    else:
                        print(f"    {kind}: not found in 2000 programs")
        finally:
            if os.path.exists(mutant):
                os.remove(mutant)


if __name__ == "__main__":
    main()
