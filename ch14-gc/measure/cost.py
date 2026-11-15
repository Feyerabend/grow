#!/usr/bin/env python3
"""
The chapter's two tables: the collectors on samples/trees.asm, with the
long-lived tree of depth 10, 11 and 12 (8188, 16380 and 32764 places).

For each depth and collector: the statistics of ./vm -s (collections, places
freed or copied), the time collecting, and the whole run, the best of seven.
vm.c prints its time collecting to a thousandth of a second, too coarse here,
so this script compiles a copy that prints it to a millionth; nothing else in
the copy is changed. The time collecting is also the best of the seven runs.

    usage: python3 measure/cost.py      (run in code/ch14-gc, after make)
"""

import os
import re
import subprocess
import sys
import tempfile
import time


def main():
    source = open("vm.c").read()
    coarse = 'fprintf(stderr, "gc: %.3f seconds collecting\\n"'
    assert source.count(coarse) == 1
    trees = open("samples/trees.asm").read()
    first = "main:   PUSH 10\n"
    assert trees.count(first) == 1
    with tempfile.TemporaryDirectory() as tmp:
        vm = os.path.join(tmp, "vm")
        with open(vm + ".c", "w") as f:
            f.write(source.replace(coarse, coarse.replace("%.3f", "%.6f")))
        subprocess.run(["cc", "-std=c99", "-Wall", "-Wextra", "-O2", "-o", vm, vm + ".c"],
                       check=True)
        print(f"{'depth':5} {'collector':9} {'collections':>11} {'places':>10}"
              f" {'collecting':>11} {'whole run':>10} {'share':>6}")
        for depth in (10, 11, 12):
            asm = os.path.join(tmp, f"trees{depth}.asm")
            program = os.path.join(tmp, f"trees{depth}.vm")
            with open(asm, "w") as f:
                f.write(trees.replace(first, f"main:   PUSH {depth}\n"))
            subprocess.run([sys.executable, "asm.py", asm, program], check=True)
            for collector in ("mark", "copy"):
                runs, gcs = [], []
                for _ in range(7):
                    t = time.perf_counter()
                    r = subprocess.run([vm, "-g", collector, "-s", program],
                                       capture_output=True, text=True, check=True)
                    runs.append(time.perf_counter() - t)
                    gcs.append(float(re.search(r"gc: ([0-9.]+) seconds", r.stderr).group(1)))
                n = re.search(r"(\d+) collections", r.stderr).group(1)
                places = re.search(r"(\d+) places (freed|copied)", r.stderr).group(1)
                run, gc = min(runs), min(gcs)
                print(f"{depth:5} {collector:9} {n:>11} {int(places):10}"
                      f" {1000 * gc:8.2f} ms {1000 * run:7.0f} ms {100 * gc / run:5.1f}%")


if __name__ == "__main__":
    main()
