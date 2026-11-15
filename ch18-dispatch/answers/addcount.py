#!/usr/bin/env python3
"""
Count the machine instructions of one ADD, for exercise 18.3.

    python3 addcount.py

Compiles the threaded build to assembly twice, at -O2 and again at -O0: as it is, and with
push, push_int, pop and number made static inline. ADD's code starts at the
label in the third place of run's table, and ends at the first jump that
leaves it: its own indirect jump, or a jump to one shared by all. The
instructions are counted, and the calls among them, and the calls to push,
pop and number left in all of run. Run from this folder; arm64 only, since it reads
arm64 assembly.
"""

import os
import re
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
CC = os.environ.get("CC", "cc")


def count(source, folder, name, level):
    path = os.path.join(folder, name + ".c")
    open(path, "w").write(source)
    out = os.path.join(folder, name + ".s")
    subprocess.run([CC, "-std=gnu99", level, "-I", CHAPTER, "-DDISPATCH=THREADED",
                    "-S", "-o", out, path], check=True)
    lines = open(out).read().splitlines()
    table = lines.index("_run.table:")
    add = lines[table + 3].split()[1]          # HALT, PUSH, ADD
    at = [i for i, line in enumerate(lines) if line.startswith(add + ":")][0]
    n, inside, end = 0, 0, ""
    for line in lines[at + 1:]:
        if re.match(r"\t[a-z]", line):         # an instruction, not a label
            n += 1                             # or a directive
            if re.match(r"\tbl\t", line):
                inside += 1
            if re.match(r"\tbr\t", line):
                end = "its own indirect jump"
                break
            if re.match(r"\tb\t", line):
                end = "a jump to a shared one"
                break
    calls = sum(1 for line in lines if re.match(r"\tbl\t_(push|push_int|pop|number)\b", line))
    return n, inside, end, calls


def main():
    source = open(os.path.join(CHAPTER, "vm.c")).read()
    inline = source
    for f in ["static void push(", "static void push_int(", "static struct value pop(",
              "static int number("]:
        assert inline.count(f) == 1, f
        inline = inline.replace(f, f.replace("static", "static inline"))
    with tempfile.TemporaryDirectory() as folder:
        for level in ["-O2", "-O0"]:
            for name, text in [("as it is", source), ("static inline", inline)]:
                n, inside, end, calls = count(text, folder, name.replace(" ", "_"),
                                              level)
                print("%s %-14s ADD: %d instructions, %d of them calls, ending in %s;"
                      % (level, name, n, inside, end))
                print("    calls to push, push_int, pop or number in all of run: %d" % calls)


main()
