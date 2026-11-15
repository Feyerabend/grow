#!/usr/bin/env python3
"""
Chapter 3's tables. Programs are written here with labels, turned into the
machine's numbers, and run in a copy of chapter 3's machine that counts each
instruction, and the most frames and stack places in use at once.

    usage: python3 measure/calls.py      (from ch03-calls)
"""

import os
import re
import subprocess
import tempfile

OPERANDS = {"PUSH": 1, "JMP": 1, "JZ": 1, "LOAD": 1, "STORE": 1, "CALL": 2}
GROUPS = {
    "juggling": ["DUP", "DROP", "SWAP", "OVER", "ROT"],
    "locals": ["LOAD", "STORE"],
    "calls": ["CALL", "RET"],
    "jumps": ["JMP", "JZ"],
    "work": ["PUSH", "ADD", "SUB", "MUL", "PRINT", "LT", "EQ"],
    "stopping": ["HALT"],
}

# Chapter 2's program, as it is there.
FIB_JUGGLED = """
        PUSH 0  PUSH 1  PUSH 10
loop:   DUP  JZ end  PUSH 1  SUB  ROT  ROT  OVER  PRINT  SWAP  OVER  ADD  ROT  JMP loop
end:    HALT
"""

# The same, with its three values in a frame: n, a, b as locals 0, 1, 2.
FIB_LOCALS = """
        PUSH 10  CALL fibs 1  DROP  HALT
fibs:   PUSH 0  PUSH 1
loop:   LOAD 0  JZ end
        LOAD 1  PRINT
        LOAD 1  LOAD 2  ADD  LOAD 2  STORE 1  STORE 2
        LOAD 0  PUSH 1  SUB  STORE 0
        JMP loop
end:    PUSH 0  RET
"""

FACT_RECURSIVE = """
        PUSH N  CALL fact 1  PRINT  HALT
fact:   LOAD 0  JZ one
        LOAD 0  LOAD 0  PUSH 1  SUB  CALL fact 1  MUL  RET
one:    PUSH 1  RET
"""

FACT_LOOP = """
        PUSH N  CALL fact 1  PRINT  HALT
fact:   PUSH 1
loop:   LOAD 0  JZ done
        LOAD 1  LOAD 0  MUL  STORE 1
        LOAD 0  PUSH 1  SUB  STORE 0
        JMP loop
done:   LOAD 1  RET
"""


def assemble(text):
    words = text.split()
    labels, at, items = {}, 0, []
    i = 0
    while i < len(words):              # first pass: where each label is
        w = words[i]
        if w.endswith(":"):
            labels[w[:-1]] = at
            i += 1
            continue
        n = OPERANDS.get(w, 0)
        items.append(words[i:i + 1 + n])
        at += 1 + n
        i += 1 + n
    out = []
    for item in items:
        out.append(item[0])
        out += [str(labels.get(x, x)) for x in item[1:]]
    return out


def run(text):
    source = open("vm.c").read()
    names = re.search(r"enum \{(.*?)\};", source, re.S).group(1)
    names = [n.strip() for n in re.sub(r"/\*.*?\*/", "", names, flags=re.S).split(",") if n.strip()]
    source = source.replace("        int op = code[pc++];",
                            "        int op = code[pc++];\n        counts[op]++;\n"
                            "        if (sp > deepest) deepest = sp;\n"
                            "        if (fsp > most_frames) most_frames = fsp;", 1)
    source = source.replace("static void run(", "static long counts[64];\nstatic int deepest, most_frames;\n\nstatic void run(", 1)
    start = source.index("static const int program[] = {")
    end = source.index("};", start) + 2
    source = source[:start] + "static const int program[] = {\n    " + ", ".join(assemble(text)) + "\n};" + source[end:]
    report = "".join(f'    printf("count {n} %ld\\n", counts[{i}]);\n' for i, n in enumerate(names))
    report += '    printf("deepest %d\\nframes %d\\n", deepest, most_frames);\n'
    source = source.replace("    run(program);\n", "    run(program);\n" + report, 1)
    with tempfile.TemporaryDirectory() as folder:
        c, exe = os.path.join(folder, "vm.c"), os.path.join(folder, "vm")
        open(c, "w").write(source)
        subprocess.run(["cc", "-std=c99", "-O1", "-o", exe, c], check=True)
        out = subprocess.run([exe], capture_output=True, text=True, check=True).stdout
    counts = {m.group(1): int(m.group(2)) for m in re.finditer(r"count (\w+) (\d+)", out)}
    printed = [l for l in out.splitlines() if not l.startswith(("count", "deepest", "frames"))]
    deepest = int(re.search(r"deepest (\d+)", out).group(1))
    frames = int(re.search(r"frames (\d+)", out).group(1))
    return printed, counts, deepest, frames


def mix(name, text):
    printed, counts, deepest, frames = run(text)
    total = sum(counts.values())
    print(f"{name}: prints {' '.join(printed)}; {total} instructions")
    for group, members in GROUPS.items():
        n = sum(counts.get(m, 0) for m in members)
        if n:
            print(f"   {group:<9} {n:>4}  {100 * n / total:3.0f}%")


def main():
    mix("Fibonacci, juggled", FIB_JUGGLED)
    mix("Fibonacci, locals", FIB_LOCALS)
    print()
    print("factorial      n  value      instructions  most frames  deepest stack")
    for n in (1, 5, 10, 12):
        for name, text in (("recursive", FACT_RECURSIVE), ("loop", FACT_LOOP)):
            printed, counts, deepest, frames = run(text.replace("PUSH N", f"PUSH {n}"))
            print(f"{name:<12} {n:>3}  {printed[0]:>10} {sum(counts.values()):>13} {frames:>12} {deepest:>14}")


if __name__ == "__main__":
    main()
