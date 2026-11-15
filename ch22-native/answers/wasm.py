#!/usr/bin/env python3
"""
Exercise 22.4: compiled to WebAssembly instead of to native code, by way of
the same C, beside chapter 23's machine, which interprets in WebAssembly.

    python3 wasm.py [times]

For each benchmark, and for HALT alone, to show what starting costs: the
C from vm2c.py, compiled by Clang to wasm32 with wasm/libc.c in place of a
C library, run by Node.js with wasm/run.mjs; checked against the expected
output, with its size. With times, best of seven, in milliseconds: native
code, as make builds it; the program compiled to WebAssembly; and chapter
23's machine, its core.c as WebAssembly, interpreting the program.
"""

import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
WASM = os.path.join(CHAPTER, "..", "ch23-wasm")
BENCHMARKS = ["empty", "fib", "loop", "sieve", "closures", "enkel-sieve", "basal-loop"]


def best(command):
    times = []
    for _ in range(7):
        start = time.perf_counter()
        subprocess.run(command, stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


def main():
    subprocess.run(["make", "-s", "-C", CHAPTER, "benchmarks"], check=True)
    subprocess.run(["make", "-s", "-C", WASM, "web/vm.wasm"], check=True)
    with tempfile.TemporaryDirectory() as w:
        empty_asm = os.path.join(w, "empty.asm")
        open(empty_asm, "w").write("        HALT\n")
        rows = []
        for b in BENCHMARKS:
            if b == "empty":
                vm = os.path.join(w, "empty.vm")
                subprocess.run([sys.executable, os.path.join(CHAPTER, "asm.py"), empty_asm, vm],
                               check=True)
                native = os.path.join(w, "empty")
                with open(native + ".c", "w") as f:
                    subprocess.run([sys.executable, os.path.join(CHAPTER, "vm2c.py"), vm],
                                   stdout=f, check=True)
                subprocess.run(["cc", "-O2", "-w", "-I", CHAPTER, native + ".c", "-o", native],
                               check=True)
                want = ""
            else:
                vm = os.path.join(CHAPTER, "bench", b + ".vm")
                native = os.path.join(CHAPTER, "bench", b)
                want = open(os.path.join(CHAPTER, "bench", b + ".out")).read()
            c, wasm = os.path.join(w, b + ".c"), os.path.join(w, b + ".wasm")
            with open(c, "w") as f:
                subprocess.run([sys.executable, os.path.join(CHAPTER, "vm2c.py"), vm], stdout=f,
                               check=True)
            subprocess.run(["clang", "--target=wasm32", "-ffreestanding", "-nostdlib", "-O2",
                            "-w", "-isystem", os.path.join(HERE, "wasm", "include"),
                            "-I", CHAPTER, "-Wl,--no-entry", "-o", wasm, c,
                            os.path.join(HERE, "wasm", "libc.c")], check=True)
            run = ["node", os.path.join(HERE, "wasm", "run.mjs"), wasm]
            got = subprocess.run(run, capture_output=True, text=True).stdout
            print("%-12s compiled to WebAssembly: %s, %d bytes" % (
                b, "right" if got == want else "WRONG", os.path.getsize(wasm)))
            rows.append((b, native, run, ["node", os.path.join(WASM, "run.mjs"), vm]))
        if "times" in sys.argv[1:]:
            print()
            print("ms, best of 7      native   compiled to wasm   chapter 23 interpreting")
            for b, native, run, interp in rows:
                print("%-12s %12.0f %18.0f %25.0f" % (b, best([native]), best(run), best(interp)))


main()
