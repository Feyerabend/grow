#!/usr/bin/env python3
"""
Exercise 16.7: walk as Python's generators would need it. A generator can
yield only from its own body, not from under a call it makes; so each subtree
gets a coroutine of its own, and each level passes its children's leaves up,
one at a time, to the level above. (lambda/0 has no loops, so the passing on
is itself a small recursive function, relay; what matters is that a leaf now
goes up through every level between it and the root.)

For measure/fringe.py's two trees of 16 leaves, the same but for one leaf:
the switches (RESUMEs that start or go on with a coroutine, from -s), the
instructions and places, for chapter 16's walk and for this one.

    usage: python3 generators.py [leaves]
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(HERE, "..")
sys.path.insert(0, CH)
sys.path.insert(0, os.path.join(CH, "measure"))
os.chdir(CH)                                    # fringe.py runs ./vm and asm.py from here
import fringe                                   # noqa: E402

GENERATORS = """
let rec relay c =
  let x = resume c 0 in
  if finished c then 0 else (yield x; relay c) in
let rec leaves t =
  coroutine (fun ignored ->
    t (fun x -> yield x)
      (fun a b -> relay (leaves a); relay (leaves b))) in
let rec same a b =
  let x = resume a 0 in
  let y = resume b 0 in
  if finished a then finished b
  else if finished b then 0
  else if x = y then same a b
  else 0 in
print (same (leaves s) (leaves t))
"""


def switches(source, folder):
    node = fringe.compiler.Parser(fringe.compiler.scan(source)).program()
    path = os.path.join(folder, "p")
    with open(path + ".asm", "w") as f:
        f.write(fringe.compiler.Generator().program(node))
    subprocess.run([sys.executable, "asm.py", path + ".asm", path + ".vm"], check=True)
    r = subprocess.run(["./vm", "-s", path + ".vm"], capture_output=True, text=True)
    return r.stdout.split()[-1], int(re.search(r"(\d+) switches", r.stderr).group(1))


def main():
    leaves = fringe.LEAVES
    print(f"two trees of {leaves} leaves")
    print("differs at   way          prints  switches  instructions  places")
    with tempfile.TemporaryDirectory() as folder:
        for differ, name in ((1, "first"), (leaves // 2 + 1, "middle"), (0, "none")):
            trees = fringe.TREES.replace("DIFFER", str(differ)).replace("LEAVES", str(leaves))
            base = fringe.run(trees + fringe.ONLY, folder)
            for way, program in (("chapter 16", fringe.COROUTINES), ("generators", GENERATORS)):
                printed, n = switches(trees + program, folder)
                steps, places = fringe.run(trees + program, folder)
                print(f"{name:<12} {way:<12} {printed:>6} {n:>9} {steps - base[0]:>13} {places - base[1]:>7}")


if __name__ == "__main__":
    main()
