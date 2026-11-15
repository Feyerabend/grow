#!/usr/bin/env python3
"""
Exercises 21.1 and 21.2: the machine of build.py, with kinds (-DKINDS) and
with the room checked at each CALL (-DROOM).

    python3 kinds.py [times] [fuzz]

Run from this folder. Builds both, runs the conformance suite on each, and
counts, with -K, the arithmetic instructions found to be given two numbers
in each benchmark. With fuzz, also runs the chapter's fuzzer, three seeds
of 600 programs, on sanitizer builds of both, and on a copy of the kinds
build broken on purpose (NEW said to leave a number), to show that the
fuzzer can see a wrong kind. With times, the benchmarks are timed, best of
seven: checked (-C), verified, verified with kinds, verified with room.
"""

import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
BENCHMARKS = ["fib", "loop", "sieve", "enkel-sieve", "basal-loop"]
FUZZ = ["-O1", "-g", "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
        "-DSTEP_LIMIT=20000"]


def cc(folder, out, *flags):
    subprocess.run(["cc", "-std=gnu99", "-Wall", "-Wextra", *flags, "-o", out,
                    os.path.join(folder, "vm.c")], check=True)
    return out


def best(command):
    times = []
    for _ in range(7):
        start = time.perf_counter()
        subprocess.run(command, stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


def conform(vm, *extra):
    r = subprocess.run([sys.executable, "conform.py", vm, *extra], cwd=CHAPTER,
                       capture_output=True, text=True)
    return re.sub(r".*/", "", r.stdout.strip().splitlines()[-1])


def fuzz(vm, dirs):
    caught, verified = 0, 0
    for d in dirs:
        r = subprocess.run(["./fuzz.sh", vm, d], cwd=CHAPTER, capture_output=True, text=True)
        caught += len([l for l in r.stdout.splitlines() if l.endswith(("differ", "complained"))])
        verified += int(re.search(r"(\d+) of them verified", r.stdout).group(1))
    return caught, verified


def main():
    subprocess.run(["make", "-s", "-C", CHAPTER, "vm", "benchmarks"], check=True)
    with tempfile.TemporaryDirectory() as w:
        subprocess.run([sys.executable, os.path.join(HERE, "build.py"), w], check=True)
        kinds = cc(w, os.path.join(w, "vm-kinds"), "-O2", "-DKINDS")
        room = cc(w, os.path.join(w, "vm-room"), "-O2", "-DROOM")
        for vm in [kinds, room]:
            print(conform(vm))
            print(conform(vm, "-g", "copy", "-S"))
        for b in BENCHMARKS:
            program = os.path.join(CHAPTER, "bench", b + ".vm")
            want = open(os.path.join(CHAPTER, "bench", b + ".out")).read()
            for vm in [kinds, room]:
                got = subprocess.run([vm, "-V", program], capture_output=True, text=True).stdout
                assert got == want, (vm, b)
            r = subprocess.run([kinds, "-K", program], stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE, text=True)
            print("%-12s %s" % (b, r.stderr.strip()))
        if "fuzz" in sys.argv[1:]:
            dirs = []
            for seed in [1, 2, 3]:
                d = os.path.join(w, "fuzz%d" % seed)
                subprocess.run([sys.executable, "fuzz.py", str(seed), "600", d], cwd=CHAPTER,
                               check=True)
                dirs.append(d)
            broken = os.path.join(w, "broken")
            os.makedirs(broken)
            for f in ["loop.h", "ops.h"]:
                os.symlink(os.path.realpath(os.path.join(w, f)), os.path.join(broken, f))
            s = open(os.path.join(w, "vm.c")).read()
            old = "            case NEW:\n                s[d - 1] = 2;"
            assert s.count(old) == 1
            open(os.path.join(broken, "vm.c"), "w").write(
                s.replace(old, "            case NEW:\n                s[d - 1] = 1;"))
            for name, folder, flag in [("kinds", w, "-DKINDS"), ("room", w, "-DROOM"),
                                       ("kinds, broken", broken, "-DKINDS")]:
                vm = cc(folder, os.path.join(folder, "vm-fuzz-" + flag[2:]), *FUZZ, flag)
                caught, verified = fuzz(vm, dirs)
                print("fuzz, %-14s 1800 programs, %d verified, %d differ" % (
                    name + ":", verified, caught))
        if "times" in sys.argv[1:]:
            vm = os.path.join(CHAPTER, "vm")
            print("ms, best of 7     checked   verified      kinds       room")
            for b in BENCHMARKS:
                program = os.path.join(CHAPTER, "bench", b + ".vm")
                print("%-12s %12.0f %10.0f %10.0f %10.0f" % (
                    b, best([vm, "-C", program]), best([vm, program]), best([kinds, program]),
                    best([room, program])))


main()
