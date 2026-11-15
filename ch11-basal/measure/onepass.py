#!/usr/bin/env python3
"""
A tree, or none: what does each cost? The same program is written in enkel/0
and in basal/0, a long list of assignments of random arithmetic to 26
variables, and compiled by each compiler: chapter 10's enkel.py, which builds a
syntax tree, and basal.py, which builds none. Both scan the whole text into
tokens first.

For each, the peak memory Python allocates while compiling (tracemalloc), the
memory held by the tokens alone, and the time, the best of five runs without
tracemalloc. A shorter pair, 1000 lines, small enough for the machine's 65536
words, is compiled by both, assembled and run, and must print the same.

    usage: python3 measure/onepass.py [lines]     (run in code/ch11-basal; default 20000)
"""

import importlib.util
import os
import random
import subprocess
import sys
import time
import tracemalloc

sys.path.insert(0, os.getcwd())
import basal                                     # noqa: E402

spec = importlib.util.spec_from_file_location("enkel", "../ch10-enkel/enkel.py")
enkel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(enkel)

NAMES = [f"v{c}" for c in "abcdefghijklmnopqrstuvwxyz"]


def expression(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        return rng.choice([str(rng.randint(0, 999)), rng.choice(NAMES)])
    op = rng.choice("+-*")
    text = f"{expression(rng, depth - 1)} {op} {expression(rng, depth - 1)}"
    return f"({text})" if rng.random() < 0.4 else text


def programs(lines):
    rng = random.Random(1)
    body = [(rng.choice(NAMES), expression(rng, 4)) for _ in range(lines)]
    b = "".join(f"LET {v} = {e}\n" for v, e in body) + "".join(f"PRINT {v}\n" for v in NAMES)
    e = ("var " + ", ".join(NAMES) + ";\nbegin\n" +
         "".join(f"  {v} is {x};\n" for v, x in body) +
         ";\n".join(f"  print {v}" for v in NAMES) + "\nend.\n")
    return b, e


def compile_basal(text):
    return basal.Translator(basal.desugar(basal.scan(text))).program()


def compile_enkel(text):
    program = enkel.Parser(enkel.scan(text)).program()
    enkel.Resolver(program).resolve()
    return enkel.Generator(text.splitlines()).program(program)


def measure(name, scan, compile_, text):
    tracemalloc.start()
    tokens = scan(text)
    tokens_mem = tracemalloc.get_traced_memory()[0]
    del tokens
    tracemalloc.stop()
    tracemalloc.start()
    out = compile_(text)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    best = min(timed(compile_, text) for _ in range(5))
    ntokens = len(scan(text))
    print(f"  {name:9} {ntokens:8} tokens  peak {peak / 1e6:6.1f} MB"
          f"  tokens alone {tokens_mem / 1e6:6.1f} MB  {best * 1000:6.0f} ms")
    return out


def timed(f, text):
    t = time.perf_counter()
    f(text)
    return time.perf_counter() - t


def run(asm_text, tag):
    a, v = f"_{tag}.asm", f"_{tag}.vm"
    open(a, "w").write(asm_text)
    subprocess.run([sys.executable, "asm.py", a, v], check=True)
    out = subprocess.run(["./vm", v], capture_output=True, text=True, check=True).stdout
    os.remove(a)
    os.remove(v)
    return out


def main():
    lines = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    b, e = programs(lines)
    print(f"{lines} assignments, then 26 prints\n")
    out_e = measure("enkel.py", enkel.scan, compile_enkel, e)
    out_b = measure("basal.py", basal.scan, compile_basal, b)
    b, e = programs(1000)
    same = run(compile_enkel(e), "e") == run(compile_basal(b), "b")
    print(f"\n  1000 lines: same output from both: {same}")


if __name__ == "__main__":
    main()
