#!/usr/bin/env python3
"""
What the Fibonacci program spends its instructions on. It runs in a copy of
chapter 2's machine that counts each instruction as it is done, and the counts
are put in four groups: the work itself, the jumps, the comparisons and the
juggling of the stack.

    usage: python3 measure/mix.py      (from ch02-jumps)
"""

import os
import re
import subprocess
import tempfile

GROUPS = {
    "work": ["PUSH", "ADD", "SUB", "MUL", "PRINT"],
    "jumps": ["JMP", "JZ"],
    "juggling": ["DUP", "DROP", "SWAP", "OVER", "ROT"],
    "comparing": ["LT", "EQ"],
    "stopping": ["HALT"],
}


def main():
    source = open("vm.c").read()
    names = re.search(r"enum \{(.*?)\};", source, re.S).group(1)
    names = [n.strip() for n in re.sub(r"/\*.*?\*/", "", names, flags=re.S).split(",")]
    names = [n for n in names if n]
    source = source.replace("        int op = code[pc++];", "        int op = code[pc++];\n        counts[op]++;", 1)
    source = source.replace("static void run(", "static long counts[64];\n\nstatic void run(", 1)
    report = "".join(f'    printf("count {n} %ld\\n", counts[{i}]);\n' for i, n in enumerate(names))
    source = source.replace("    run(program);\n", "    run(program);\n" + report, 1)
    with tempfile.TemporaryDirectory() as folder:
        c, exe = os.path.join(folder, "vm.c"), os.path.join(folder, "vm")
        open(c, "w").write(source)
        subprocess.run(["cc", "-std=c99", "-O1", "-o", exe, c], check=True)
        out = subprocess.run([exe], capture_output=True, text=True, check=True).stdout
    counts = {m.group(1): int(m.group(2)) for m in re.finditer(r"count (\w+) (\d+)", out)}
    total = sum(counts.values())
    print("printed:", " ".join(l for l in out.splitlines() if not l.startswith("count")))
    for group, members in GROUPS.items():
        n = sum(counts.get(m, 0) for m in members)
        detail = ", ".join(f"{m} {counts[m]}" for m in members if counts.get(m))
        print(f"{group:<10} {n:>4}  {100 * n / total:5.1f}%   {detail}")
    print(f"{'all':<10} {total:>4}")


if __name__ == "__main__":
    main()
