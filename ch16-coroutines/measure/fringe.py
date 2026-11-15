#!/usr/bin/env python3
"""
What the same-fringe program costs, against flattening both trees first.

Two balanced trees of 16 leaves, the same but for one leaf: the first, the
one in the middle, or none. Each way is run, and so is a program that only builds
the trees, and what that one costs is taken off. Instructions are counted
from the machine's trace, the rest is what -s reports.

    usage: python3 measure/fringe.py [leaves]     (with ./vm built)
"""

import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, ".")
compiler = __import__("lambda")

LEAVES = int(sys.argv[1]) if len(sys.argv) > 1 else 16

TREES = """
let leaf x = fun l n -> l x in
let node a b = fun l n -> n a b in
let rec build lo n d =
  if n = 1 then leaf (if lo = d then 0 else lo)
  else node (build lo (n / 2) d) (build (lo + n / 2) (n - n / 2) d) in
let s = build 1 LEAVES 0 in
let t = build 1 LEAVES DIFFER in
"""

ONLY = "0\n"

COROUTINES = """
let rec walk t = t (fun x -> yield x) (fun a b -> walk a; walk b) in
let leaves t = coroutine (fun ignored -> walk t) in
let rec same a b =
  let x = resume a 0 in
  let y = resume b 0 in
  if finished a then finished b
  else if finished b then 0
  else if x = y then same a b
  else 0 in
print (same (leaves s) (leaves t))
"""

FLATTEN = """
let nil = fun c e -> e 0 in
let cons h r = fun c e -> c h r in
let rec fringe t rest =
  t (fun x -> cons x rest) (fun a b -> fringe a (fringe b rest)) in
let rec same a b =
  a (fun x r -> b (fun y q -> if x = y then same r q else 0) (fun u -> 0))
    (fun u -> b (fun y q -> 0) (fun u -> 1)) in
print (same (fringe s nil) (fringe t nil))
"""


def run(source, folder):
    node = compiler.Parser(compiler.scan(source)).program()
    path = os.path.join(folder, "p")
    with open(path + ".asm", "w") as f:
        f.write(compiler.Generator().program(node))
    asm_args = [sys.executable, "asm.py", path + ".asm", path + ".vm"]
    subprocess.run(asm_args, check=True)
    trace = subprocess.run(["./vm", "-t", path + ".vm"], capture_output=True, text=True)
    if trace.returncode:
        sys.exit(trace.stderr.splitlines()[-1])
    steps = sum(1 for line in trace.stderr.splitlines() if re.match(r"\s*\d+\s+\d+\s+[A-Z]", line))
    stats = subprocess.run(["./vm", "-s", path + ".vm"], capture_output=True, text=True).stderr
    places = int(re.search(r"(\d+) places in all", stats).group(1))
    return steps, places


def main():
    print("differs at   way          instructions  places")
    with tempfile.TemporaryDirectory() as folder:
        for differ, name in ((1, "first"), (LEAVES // 2 + 1, "middle"), (0, "none")):
            trees = TREES.replace("DIFFER", str(differ)).replace("LEAVES", str(LEAVES))
            base = run(trees + ONLY, folder)
            for way, program in (("coroutines", COROUTINES), ("flatten", FLATTEN)):
                steps, places = run(trees + program, folder)
                print(f"{name:<12} {way:<12} {steps - base[0]:>12} {places - base[1]:>7}")


if __name__ == "__main__":
    main()
