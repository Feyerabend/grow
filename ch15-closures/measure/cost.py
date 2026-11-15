#!/usr/bin/env python3
"""
What do functions as values cost, against chapter 10's procedures?

The same three functions written in lambda/0 and in enkel/0, compiled by
lambda.py and by ../ch10-enkel/enkel.py, and run on this chapter's machine:
the instructions executed (lines of ./vm -t), and the blocks and places made
(./vm -s). fib takes one argument; gcd and ack take two, so in lambda/0
every call of them first makes a closure holding the first argument.

Then how deep lambda/0 can recurse: the largest n for which
'sum n = n + sum (n - 1)' still runs, and the longest list, made by the
range of samples/data.lam, that its sum can fold.

    usage: python3 measure/cost.py      (run in code/ch15-closures, after make)
"""

import os
import re
import subprocess
import sys
import tempfile

STEP = re.compile(r"\s*\d+\s+\d+\s")
ENKEL = os.path.join("..", "ch10-enkel", "enkel.py")

PROGRAMS = {
    "fib 20": (
        "let rec fib n = if n < 2 then n else fib (n - 1) + fib (n - 2) in\n"
        "print (fib 20)\n",
        """procedure fib[n];
  var a;
  begin
    if n < 2 then return n;
    call fib[n - 1]; a is rval;
    call fib[n - 2];
    rval is a + rval
  end;
begin call fib[20]; print rval end.
"""),
    "gcd 1836311903 1134903170": (
        "let rec gcd a b = if b = 0 then a else gcd b (a % b) in\n"
        "print (gcd 1836311903 1134903170)\n",
        """procedure gcd[a, b];
  begin
    if b = 0 then return a;
    call gcd[b, a % b]
  end;
begin call gcd[1836311903, 1134903170]; print rval end.
"""),
    "ack 2 3": (
        "let rec ack m n =\n"
        "    if m = 0 then n + 1\n"
        "    else if n = 0 then ack (m - 1) 1\n"
        "    else ack (m - 1) (ack m (n - 1)) in\n"
        "print (ack 2 3)\n",
        """procedure ack[m, n];
  begin
    if m = 0 then return n + 1;
    if n = 0 then begin call ack[m - 1, 1]; return rval end;
    call ack[m, n - 1];
    call ack[m - 1, rval]
  end;
begin call ack[2, 3]; print rval end.
"""),
}


def build(tmp, name, text, compiler):
    src = os.path.join(tmp, name)
    with open(src, "w") as f:
        f.write(text)
    asm, vm = src + ".asm", src + ".vm"
    with open(asm, "w") as f:
        r = subprocess.run([sys.executable, compiler, src], stdout=f, stderr=subprocess.PIPE)
    if r.returncode:
        raise SystemExit(r.stderr.decode())
    subprocess.run([sys.executable, "asm.py", asm, vm], check=True)
    return vm


def run(vm):
    """Output, status, executed instructions, blocks made, places made."""
    t = subprocess.run(["./vm", "-t", vm], capture_output=True, text=True)
    s = subprocess.run(["./vm", "-s", vm], capture_output=True, text=True)
    m = re.search(r"(\d+) blocks made, (\d+) places", s.stderr)
    steps = sum(1 for line in t.stderr.splitlines() if STEP.match(line))
    return t.stdout, t.returncode, steps, int(m.group(1)), int(m.group(2)), s.stderr


def deepest(tmp, make):
    """The largest n for which the program make(n) runs, by bisection."""
    def ok(n):
        out, status, *_ = run(build(tmp, f"d{n}.lam", make(n), "lambda.py"))
        return status == 0
    lo, hi = 1, 2
    while ok(hi):
        lo, hi = hi, hi * 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if ok(mid) else (lo, mid)
    return lo, run(build(tmp, f"d{hi}.lam", make(hi), "lambda.py"))[5].splitlines()[0]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        print(f"{'call':27} {'lambda/0':>9} {'enkel/0':>8} {'blocks':>7} {'places':>7}")
        for k, (name, (lam, enk)) in enumerate(PROGRAMS.items()):
            a = run(build(tmp, f"p{k}.lam", lam, "lambda.py"))
            b = run(build(tmp, f"p{k}.p", enk, ENKEL))
            assert a[0] == b[0] and a[1] == b[1] == 0, (name, a[:2], b[:2])
            print(f"{name:27} {a[2]:9} {b[2]:8} {a[3]:7} {a[4]:7}   enkel/0:"
                  f" {b[3]} blocks   prints {a[0].split()[0]}")
        n, why = deepest(tmp, lambda n:
                         f"let rec sum n = if n = 0 then 0 else n + sum (n - 1) in print (sum {n})")
        print(f"sum n recurses to n = {n}; at {n + 1}: {why}")
        n, why = deepest(tmp, lambda n:
                         "let nil = fun f z -> z in\n"
                         "let cons h t = fun f z -> f h (t f z) in\n"
                         "let rec range n = if n = 0 then nil else cons n (range (n - 1)) in\n"
                         f"print ((range {n}) (fun h acc -> h + acc) 0)\n")
        print(f"a list folds up to {n} elements; at {n + 1}: {why}")


if __name__ == "__main__":
    main()
