#!/usr/bin/env python3
"""
Run a program on chapter 3's machine, written with labels, and count what it
does, as measure/calls.py does: instructions by group, the most frames and the
deepest stack.

    usage: python3 run.py program.txt [mod] [asan] [N=value]

mod adds MOD, the remainder (pop b, pop a, push a % b). asan builds the machine
with AddressSanitizer, which stops it at the first read or write outside its
arrays. N=value puts value wherever the program says PUSH N.
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "measure"))
import calls                                    # noqa: E402  (its assembler and groups)


def main():
    args = sys.argv[1:]
    text = open(args[0]).read()
    text = "\n".join(line.split(";")[0] for line in text.splitlines())
    for a in args[1:]:
        if a.startswith("N="):
            text = text.replace("PUSH N", "PUSH " + a[2:])
    source = open(os.path.join(HERE, "..", "vm.c")).read()
    if "mod" in args:
        source = source.replace("    RET         /* pop result, drop the frame, push result     */\n",
                                "    RET,\n    MOD         /* a b -> a % b                                */\n")
        source = source.replace("        case LOAD:", "        case MOD:\n            b = pop();\n"
                                "            a = pop();\n            push(a % b);\n            break;\n"
                                "        case LOAD:", 1)
    names = re.search(r"enum \{(.*?)\};", source, re.S).group(1)
    names = [n.strip() for n in re.sub(r"/\*.*?\*/", "", names, flags=re.S).split(",") if n.strip()]
    source = source.replace("        int op = code[pc++];",
                            "        int op = code[pc++];\n        counts[op]++;\n"
                            "        if (sp > deepest) deepest = sp;\n"
                            "        if (fsp > most_frames) most_frames = fsp;", 1)
    source = source.replace("static void run(", "static long counts[64];\nstatic int deepest, most_frames;\n\nstatic void run(", 1)
    start = source.index("static const int program[] = {")
    end = source.index("};", start) + 2
    source = source[:start] + "static const int program[] = {\n    " + ", ".join(calls.assemble(text)) + "\n};" + source[end:]
    report = "".join(f'    fprintf(stderr, "count {n} %ld\\n", counts[{i}]);\n' for i, n in enumerate(names))
    report += '    fprintf(stderr, "deepest %d\\nframes %d\\n", deepest, most_frames);\n'
    source = source.replace("    run(program);\n", "    run(program);\n" + report, 1)
    flags = ["-O0", "-g", "-fsanitize=address"] if "asan" in args else ["-O1"]
    with tempfile.TemporaryDirectory() as folder:
        c, exe = os.path.join(folder, "vm.c"), os.path.join(folder, "vm")
        open(c, "w").write(source)
        subprocess.run(["cc", "-std=c99", "-w", *flags, "-o", exe, c], check=True)
        r = subprocess.run([exe], capture_output=True, text=True,
                           env=dict(os.environ, ASAN_OPTIONS="detect_leaks=0"))
    if r.returncode != 0:
        m = re.search(r"ERROR: AddressSanitizer: ([\w-]+).*?\n(?:.*\n)*?.*?is located (\d+) bytes after global variable '(\w+)'", r.stderr)
        print("printed:", " ".join(r.stdout.split()))
        print("stopped:", f"{m.group(1)}, {m.group(2)} bytes after {m.group(3)}" if m else f"status {r.returncode}")
        return
    counts = {m.group(1): int(m.group(2)) for m in re.finditer(r"count (\w+) (\d+)", r.stderr)}
    total = sum(counts.values())
    print("printed:", " ".join(r.stdout.split()))
    print("instructions:", total)
    for group, members in calls.GROUPS.items():
        n = sum(counts.get(x, 0) for x in members)
        if n:
            print(f"   {group:<9} {n:>4}")
    print("most frames:", re.search(r"frames (\d+)", r.stderr).group(1))
    print("deepest stack:", re.search(r"deepest (\d+)", r.stderr).group(1))


main()
