#!/usr/bin/env python3
"""
Exercises 15.1, 15.4 and 15.5, measured as measure/cost.py measures: its three
programs, compiled with each of lambda_more.py's options and with all three,
run on the machine with TAILCALLI; instructions run (lines of -t), blocks
made, and the most frames at once (the deepest recursion the run needs).
Then the samples, with and without -once; and with all three options, under
the copying collector with stress, they must print what they printed before.

    usage: python3 measure_more.py
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH15 = os.path.join(HERE, "..")
sys.path.insert(0, CH15)
sys.path.insert(0, os.path.join(CH15, "measure"))
import isa                                      # noqa: E402

isa.INSTRUCTIONS.append((32, "TAILCALLI", ("n",)))
isa.BY_NAME["TAILCALLI"] = (32, ("n",))
isa.BY_CODE[32] = ("TAILCALLI", ("n",))
import asm                                      # noqa: E402
import cost                                     # noqa: E402
import vmfile                                   # noqa: E402

STEP = re.compile(r"\s*\d+\s+\d+\s")
OPTIONS = [("as in lambda.py", []), ("-once", ["-once"]), ("-direct", ["-direct"]),
           ("-tail", ["-tail"]), ("all three", ["-tail", "-once", "-direct"])]


def build(work, text, flags):
    src = os.path.join(work, "p.lam")
    open(src, "w").write(text)
    r = subprocess.run([sys.executable, os.path.join(HERE, "lambda_more.py"), *flags, src],
                       capture_output=True, text=True, check=True)
    a = asm.Assembler(src)
    _, code = a.assemble(r.stdout)
    assert not a.errors, a.errors
    vm = os.path.join(work, "p.vm")
    vmfile.write(vm, code)
    return vm


def run(exe, vm, *options):
    t = subprocess.run([exe, "-t", *options, vm], capture_output=True, text=True)
    s = subprocess.run([exe, "-s", *options, vm], capture_output=True, text=True)
    steps = [line for line in t.stderr.splitlines() if STEP.match(line)]
    frames = max(line.count("|") for line in steps)
    blocks = int(re.search(r"(\d+) blocks made", s.stderr).group(1))
    return t.stdout.split(), len(steps), blocks, frames


def main():
    with tempfile.TemporaryDirectory() as work:
        c, exe = os.path.join(work, "vm_more.c"), os.path.join(work, "vm")
        with open(c, "w") as f:
            subprocess.run([sys.executable, os.path.join(HERE, "build.py"), "c"], stdout=f, check=True)
        subprocess.run(["cc", "-std=c99", "-O2", "-o", exe, c], check=True)
        print(f"{'call':27} {'compiled':16} {'instructions':>12} {'blocks':>7} {'frames':>7}")
        for name, (text, _) in cost.PROGRAMS.items():
            for label, flags in OPTIONS:
                out, steps, blocks, frames = run(exe, build(work, text, flags))
                print(f"{name:27} {label:16} {steps:12} {blocks:7} {frames:7}   prints {out[0]}")
        print(f"\n{'sample':16} {'instructions':>12} {'-once':>8} {'blocks':>7} {'-once':>7}")
        for path in sorted(os.listdir(os.path.join(CH15, "samples"))):
            if path.endswith(".lam"):
                text = open(os.path.join(CH15, "samples", path)).read()
                _, s0, b0, _ = run(exe, build(work, text, []))
                _, s1, b1, _ = run(exe, build(work, text, ["-once"]))
                print(f"{path:16} {s0:12} {s1:8} {b0:7} {b1:7}")
        print()
        for path in sorted(os.listdir(os.path.join(CH15, "samples"))):
            if not path.endswith(".lam"):
                continue
            vm = build(work, open(os.path.join(CH15, "samples", path)).read(), ["-tail", "-once", "-direct"])
            r = subprocess.run([exe, "-g", "copy", "-S", vm], capture_output=True, text=True)
            want = open(os.path.join(CH15, "samples", path[:-4] + ".out")).read()
            print(f"{path}: all three, copying, stress: {'the same' if r.stdout + r.stderr == want else 'DIFFERENT'}")


if __name__ == "__main__":
    main()
