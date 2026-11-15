#!/usr/bin/env python3
"""
Exercises 23.4 to 23.6: core.c, built in several ways, as a C program and as
WebAssembly: its size, whether it passes the suite, and its speed.

    python3 core.py [times]

  as it is     core.c at -O2, as the Makefile builds it; and at -O0 and -Os
  loop         exercise 5: vm_run() a loop of its own (build.py loop)
  state        exercise 6: the machine in a struct, passed to every function
               (build.py state)

Every build at -O2 runs the suite, with both collectors and stress, as a C
program and under Node.js; the loop build also one vm_step() at a time, by
step.mjs, as the playground steps. With times, the benchmarks of
measure/bench run on each, best of seven, in milliseconds.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
BENCHMARKS = ["empty", "fib", "loop", "sieve", "closures", "enkel-sieve", "basal-loop"]


def best(command, expect):
    times = []
    for _ in range(7):
        start = time.perf_counter()
        r = subprocess.run(command, stdout=subprocess.PIPE, check=True)
        times.append(time.perf_counter() - start)
        if r.stdout != expect:
            raise SystemExit("%s: wrong output" % " ".join(command))
    return min(times) * 1000


def build(folder, level):
    """The C host and vm.wasm, from the core.c in folder."""
    core = os.path.join(folder, "core.c")
    exe = os.path.join(folder, "vm" + level)
    subprocess.run(["cc", "-std=c99", level, "-Wall", "-Wextra", "-o", exe, core,
                    os.path.join(folder, "host.c")], check=True)
    wasm = os.path.join(folder, "web", "vm%s.wasm" % level)
    subprocess.run(["clang", "--target=wasm32", "-std=c99", level, "-Wall", "-Wextra",
                    "-nostdlib", "-Wl,--no-entry", "-o", wasm, core], check=True)
    return exe, wasm


def runner(folder, wasm):
    """A copy of run.mjs and machine.js that loads this vm.wasm."""
    shutil.copy(wasm, os.path.join(folder, "web", "vm.wasm"))
    return os.path.join(folder, "run.mjs")


def conform(*command):
    r = subprocess.run([sys.executable, "conform.py", *command], cwd=CHAPTER,
                       capture_output=True, text=True)
    return r.stdout.strip().splitlines()[-1].rsplit(": ", 1)[1]


def main():
    timing = "times" in sys.argv[1:]
    with tempfile.TemporaryDirectory() as w:
        plain = os.path.join(w, "plain")
        os.makedirs(os.path.join(plain, "web"))
        for f in ["core.c", "ops.h", "host.c", "run.mjs"]:
            shutil.copy(os.path.join(CHAPTER, f), plain)
        shutil.copy(os.path.join(CHAPTER, "web", "machine.js"), os.path.join(plain, "web"))
        for v in ["loop", "state"]:
            subprocess.run([sys.executable, os.path.join(HERE, "build.py"), v,
                            os.path.join(w, v)], check=True)
        builds = []
        for name, folder, level in [("-O0", plain, "-O0"), ("-O2", plain, "-O2"),
                                    ("-Os", plain, "-Os"), ("loop", os.path.join(w, "loop"), "-O2"),
                                    ("state", os.path.join(w, "state"), "-O2")]:
            sub = os.path.join(w, "run-" + name.strip("-"))
            shutil.copytree(folder, sub)
            exe, wasm = build(sub, level)
            builds.append((name, sub, exe, wasm))
        print("%-6s %10s" % ("", "vm.wasm"))
        for name, sub, exe, wasm in builds:
            print("%-6s %10d bytes" % (name, os.path.getsize(wasm)))
        print()
        for name, sub, exe, wasm in builds:
            if name in ("-O0", "-Os"):
                continue
            run = runner(sub, wasm)
            line = "%-6s C %s, %s; Node.js %s, %s" % (
                name, conform(exe), conform(exe, "-g", "copy", "-S"),
                conform("node", run), conform("node", run, "-g", "copy", "-S"))
            if name == "loop":
                step = os.path.join(HERE, "step.mjs")
                line += "; stepping %s, %s" % (conform("node", step, sub),
                                               conform("node", step, sub, "-g", "copy", "-S"))
            print(line)
        if timing:
            print()
            print("ms, best of 7  " + "".join("%7s C %6s js" % (n, "") for n, *_ in builds))
            for b in BENCHMARKS:
                vm = os.path.join(w, b + ".vm")
                subprocess.run([sys.executable, os.path.join(CHAPTER, "asm.py"),
                                os.path.join(CHAPTER, "measure", "bench", b + ".asm"), vm],
                               check=True)
                expect = open(os.path.join(CHAPTER, "measure", "bench", b + ".out"), "rb").read()
                cells = []
                for name, sub, exe, wasm in builds:
                    run = runner(sub, wasm)
                    cells.append("%9.0f %9.0f" % (best([exe, vm], expect),
                                                  best(["node", run, vm], expect)))
                print("%-12s" % b + "".join(cells))


main()
