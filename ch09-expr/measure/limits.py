#!/usr/bin/env python3
"""
How deep can an expression go before the compiler or the machine gives up,
and how fast are the three stages?

Depth. Three shapes, each made deeper one step at a time:
    nested    ((((1))))           parentheses only
    minus     ----1               unary minus only
    right     1-(1-(1-(1-1)))     each subtraction waits for the one inside it
The compiler is expr.py, run as `make` runs it, so a failure is what a user sees.
The machine is ./vm, with its 256-value stack.

Speed. fuzz.py's expressions, 20000 of them, through each stage in turn,
the best of five runs.

    usage: python3 measure/limits.py          (run in code/ch09-expr, after make vm)
"""

import os
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.getcwd())
import expr                                      # noqa: E402

SHAPES = {
    "nested": lambda n: "(" * n + "1" + ")" * n,
    "minus": lambda n: "-" * n + "1",
    "right": lambda n: "1-(" * n + "1" + ")" * n,
}


def compiles(source, work):
    path = os.path.join(work, "p.expr")
    with open(path, "w") as f:
        f.write(source + ";\n")
    r = subprocess.run([sys.executable, "expr.py", path], capture_output=True, text=True)
    last = r.stderr.strip().splitlines()[-1] if r.returncode else ""
    return r.returncode == 0, last, r.stdout


def runs(asm, work):
    a, v = os.path.join(work, "p.asm"), os.path.join(work, "p.vm")
    with open(a, "w") as f:
        f.write(asm)
    subprocess.run([sys.executable, "asm.py", a, v], check=True)
    r = subprocess.run(["./vm", v], capture_output=True, text=True)
    return r.returncode == 0, r.stderr.strip()


def first_failure(test, lo=1, hi=4096):
    """The smallest n for which test(n) fails, by bisection (test passes at lo)."""
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if test(mid)[0]:
            lo = mid
        else:
            hi = mid
    return hi


def main():
    with tempfile.TemporaryDirectory() as work:
        print("depth at which it first fails\n")
        for name, make in SHAPES.items():
            n = first_failure(lambda k: compiles(make(k), work))
            ok, message, _ = compiles(make(n), work)
            print(f"  {name:7} compiler fails at {n:4}: {message[:70]}")
            def machine(k):
                ok, _, asm = compiles(make(k), work)
                return runs(asm, work) if ok else (False, "")
            m = first_failure(machine, 1, n - 1)
            if m < n - 1:
                print(f"  {'':7} machine fails at  {m:4}: {runs(compiles(make(m), work)[2], work)[1]}")
            else:
                print(f"  {'':7} machine runs every depth the compiler takes")

        p, e = os.path.join(work, "f.expr"), os.path.join(work, "f.out")
        subprocess.run([sys.executable, "fuzz.py", "1", "20000", p, e], check=True)
        text = open(p).read()
        best = {}
        for _ in range(5):
            t0 = time.perf_counter()
            tokens = expr.scan(text)
            t1 = time.perf_counter()
            trees = expr.parse(tokens)
            t2 = time.perf_counter()
            expr.compile_program(trees)
            t3 = time.perf_counter()
            for stage, t in (("scan", t1 - t0), ("parse", t2 - t1), ("generate", t3 - t2)):
                best[stage] = min(best.get(stage, t), t)
        total = sum(best.values())
        print(f"\n20000 expressions, {len(text)} characters, {len(tokens)} tokens\n")
        for stage, t in best.items():
            print(f"  {stage:9} {t * 1000:7.1f} ms  {100 * t / total:4.0f}%"
                  f"  {len(tokens) / t / 1e6:5.2f} million tokens a second")
        print(f"  {'all':9} {total * 1000:7.1f} ms")


if __name__ == "__main__":
    main()
