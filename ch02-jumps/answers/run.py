#!/usr/bin/env python3
"""
Run a program on chapter 2's machine, written as words with labels, and count
what it spends its instructions on, as measure/mix.py does.

    usage: python3 run.py program.txt [jnz] [relative]

A program is words: instruction names, numbers, and labels, written
"name:" where they are defined and "name" where they are used. With jnz, the
machine gets JNZ, jump if not zero; with relative, JMP, JZ and JNZ take an
offset from their own address instead of an address.
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GROUPS = {"work": ["PUSH", "ADD", "SUB", "MUL", "PRINT"],
          "jumps": ["JMP", "JZ", "JNZ"],
          "juggling": ["DUP", "DROP", "SWAP", "OVER", "ROT"],
          "comparing": ["LT", "EQ"], "stopping": ["HALT"]}
JUMPS = ("JMP", "JZ", "JNZ")


def assemble(words, names, relative):
    labels, place, items = {}, 0, []
    for w in words:
        if w.endswith(":"):
            labels[w[:-1]] = place
        else:
            items.append((place, w))
            place += 1
    code, last = [], None
    for place, w in items:
        if w in names:
            code.append(w)
            last = (place, w)
        elif re.fullmatch(r"-?\d+", w):
            code.append(w)
        else:
            target = labels[w]
            # an operand of a jump: an address, or an offset from the jump
            code.append(str(target - last[0]) if relative and last[1] in JUMPS else str(target))
    return code


def main():
    args = sys.argv[1:]
    words = [w for line in open(args[0]) for w in line.split(";")[0].split()]
    source = open(os.path.join(HERE, "..", "vm.c")).read()
    if "jnz" in args:
        source = source.replace("    EQ          /* a b     -> (a == b) as 1 or 0               */\n",
                                "    EQ,\n    JNZ         /* JNZ addr: pop a, continue at addr if a != 0 */\n")
        source = source.replace("        case DUP:",
                                "        case JNZ:\n            a = pop();\n            if (a != 0)\n"
                                "                pc = code[pc];\n            else\n                pc++;\n"
                                "            break;\n        case DUP:", 1)
    if "relative" in args:
        # pc has passed the opcode: the jump's own address is pc - 1
        source = source.replace("pc = code[pc];", "pc = pc - 1 + code[pc];")
    names = re.search(r"enum \{(.*?)\};", source, re.S).group(1)
    names = [n.strip() for n in re.sub(r"/\*.*?\*/", "", names, flags=re.S).split(",") if n.strip()]
    code = assemble(words, names, "relative" in args)
    program = "static const int program[] = {\n    " + ", ".join(code) + "\n};\n"
    a, b = source.index("static const int program[]"), source.index("int main(void)")
    source = source[:a] + program + "\n" + source[b:]
    source = source.replace("        int op = code[pc++];", "        int op = code[pc++];\n        counts[op]++;", 1)
    source = source.replace("static void run(", "static long counts[64];\n\nstatic void run(", 1)
    report = "".join(f'    fprintf(stderr, "count {n} %ld\\n", counts[{i}]);\n' for i, n in enumerate(names))
    source = source.replace("    run(program);\n", "    run(program);\n" + report, 1)
    with tempfile.TemporaryDirectory() as folder:
        c, exe = os.path.join(folder, "vm.c"), os.path.join(folder, "vm")
        open(c, "w").write(source)
        subprocess.run(["cc", "-std=c99", "-O1", "-w", "-o", exe, c], check=True)
        r = subprocess.run([exe], capture_output=True, text=True, check=True)
    counts = {m.group(1): int(m.group(2)) for m in re.finditer(r"count (\w+) (\d+)", r.stderr)}
    print("printed:", " ".join(r.stdout.split()))
    print("words:", len(code))
    print("code:", " ".join(code))
    for g, ns in GROUPS.items():
        print(f"{g:<10} {sum(counts.get(n, 0) for n in ns):>4}")
    print(f"{'all':<10} {sum(counts.values()):>4}")


main()
