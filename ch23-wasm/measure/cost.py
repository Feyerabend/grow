"""The same core as a C program and as WebAssembly: the time each
benchmark takes.

    python3 measure/cost.py

Run from the chapter's folder, after make, on a quiet computer on mains
power. The benchmarks in measure/bench are chapter 22's, copied, and
empty.asm is HALT alone, to show what starting costs. Each runs seven
times, and the best is kept, with its output checked against the .out
file, on:

    C host      ./vm, the core with host.c, as make builds it, with
                step() forced inline into vm_run()'s loop;
    stepping    the same with step() kept out of line, so that every
                instruction is a call, as in the first version of
                core.c, where vm_run() called vm_step();
    wasm        the core compiled to WebAssembly here, as the Makefile
                does (step() not inlined), run by run.mjs;
    wasm inl.   the same with step() forced inline there too;
    native      the program compiled by chapter 22's vm2c.py, if
                ../ch22-native is there.
"""

import os
import shutil
import subprocess
import tempfile
import time

RUNS = 7
BENCHMARKS = ["empty", "fib", "loop", "sieve", "closures", "enkel-sieve", "basal-loop"]
NATIVE = "../ch22-native"

FORCED = "#define STEP static inline __attribute__((always_inline)) int"
WASM = "#if defined __wasm__\n#define STEP static int\n#else"


def best(args, expect):
    times = []
    for _ in range(RUNS):
        start = time.perf_counter()
        r = subprocess.run(args, stdout=subprocess.PIPE, check=True)
        times.append(time.perf_counter() - start)
        if r.stdout != expect:
            raise SystemExit("%s: wrong output" % " ".join(args))
    return min(times) * 1000


def variant(where, old, new):
    """core.c with one change, and ops.h beside it, in a folder of its own."""
    with open("core.c") as f:
        s = f.read()
    assert s.count(old) == 1
    os.makedirs(where)
    with open(os.path.join(where, "core.c"), "w") as f:
        f.write(s.replace(old, new))
    shutil.copy("ops.h", where)
    return os.path.join(where, "core.c")


def c_host(source):
    exe = os.path.join(os.path.dirname(source), "vm")
    subprocess.run(["cc", "-std=c99", "-O2", "-o", exe, source, "host.c"], check=True)
    return exe


def wasm(source, where):
    """A folder holding run.mjs and web/, with source compiled to vm.wasm."""
    os.makedirs(os.path.join(where, "web"))
    subprocess.run(["clang", "--target=wasm32", "-std=c99", "-O2", "-nostdlib",
                    "-Wl,--no-entry", "-o", os.path.join(where, "web", "vm.wasm"),
                    source], check=True)
    shutil.copy("web/machine.js", os.path.join(where, "web"))
    shutil.copy("run.mjs", where)
    return os.path.join(where, "run.mjs")


def native(vm, work):
    c = vm[:-3] + ".c"
    exe = vm[:-3]
    with open(c, "w") as f:
        subprocess.run(["python3", os.path.join(NATIVE, "vm2c.py"), vm],
                       stdout=f, check=True)
    subprocess.run(["cc", "-O2", "-w", "-I" + NATIVE, c, "-o", exe], check=True)
    return exe


with tempfile.TemporaryDirectory() as work:
    have_native = os.path.exists(os.path.join(NATIVE, "vm2c.py"))
    stepping = c_host(variant(os.path.join(work, "stepping"), FORCED,
                              "#define STEP static __attribute__((noinline)) int"))
    plain_wasm = wasm("core.c", os.path.join(work, "plain"))
    forced_wasm = wasm(variant(os.path.join(work, "forced"), WASM, "#if 0\n#else"),
                       os.path.join(work, "forced", "out"))
    print("best of %d runs, milliseconds" % RUNS)
    print("%-12s %7s %9s %7s %10s %7s" %
          ("", "C host", "stepping", "wasm", "wasm inl.", "native"))
    for b in BENCHMARKS:
        vm = os.path.join(work, b + ".vm")
        subprocess.run(["python3", "asm.py", "measure/bench/%s.asm" % b, vm], check=True)
        with open("measure/bench/%s.out" % b, "rb") as f:
            expect = f.read()
        c = best(["./vm", vm], expect)
        s = best([stepping, vm], expect)
        w = best(["node", plain_wasm, vm], expect)
        wi = best(["node", forced_wasm, vm], expect)
        n = best([native(vm, work)], expect) if have_native else float("nan")
        print("%-12s %7.0f %9.0f %7.0f %10.0f %7.0f" % (b, c, s, w, wi, n))
