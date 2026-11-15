#!/usr/bin/env python3
"""
Exercises 20.1 and 20.4: the optimiser's two new rules, from build.py.

    python3 rules.py [times]

Run from this folder. First, as same.sh does, every program of the suite,
the samples, the benchmarks, tests/super and this folder is run as it is and
optimised, with no new rule, -dup, -dup-anywhere and -assoc in turn, on
vm-threaded; what
it prints, its status and its trap message must be the same, all but the
trap's address. Each difference is printed. Then how often each rule was
used, and, for storeload.asm, the dispatches on vm-threaded and vm-super,
as it is and with -dup; with times, also the times, best of seven.
"""

import glob
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
RULES = ["", "-dup", "-dup-anywhere", "-assoc"]   # "": the chapter's rules alone


def assemble(src, out):
    r = subprocess.run([sys.executable, os.path.join(CHAPTER, "asm.py"), src, out],
                       capture_output=True)
    return r.returncode == 0


def behaviour(machine, program):
    r = subprocess.run([machine, program], capture_output=True)
    err = re.sub(rb"^(trap: .*) at \d+$", rb"\1", r.stderr, flags=re.M)
    return r.stdout, err, r.returncode


def best(command):
    times = []
    for _ in range(7):
        start = time.perf_counter()
        subprocess.run(command, stdout=subprocess.DEVNULL, check=True)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


def steps(machine, program):
    r = subprocess.run([machine, "-c", program], stdout=subprocess.DEVNULL,
                       stderr=subprocess.PIPE, text=True)
    return int(re.search(r"steps: (\d+)", r.stderr).group(1))


def main():
    subprocess.run(["make", "-s", "-C", CHAPTER, "all"], check=True)
    vm = os.path.join(CHAPTER, "vm-threaded")
    programs = []
    for pattern in ["suite/*.asm", "samples/*.asm", "bench/*.asm", "tests/super/*.asm"]:
        programs += sorted(p for p in glob.glob(os.path.join(CHAPTER, pattern))
                           if not p.endswith(".opt.asm"))
    programs += sorted(glob.glob(os.path.join(HERE, "*.asm")))
    with tempfile.TemporaryDirectory() as w:
        subprocess.run([sys.executable, os.path.join(HERE, "build.py"), w], check=True)
        opt = os.path.join(w, "opt_more.py")
        used = {r: {} for r in RULES}
        for p in programs:
            plain = os.path.join(w, "p.vm")
            if not assemble(p, plain):
                continue
            want = behaviour(vm, plain)
            for rule in RULES:
                o = subprocess.run([sys.executable, opt, *([rule] if rule else []), "-s", p],
                                   capture_output=True, text=True, check=True)
                for m in re.finditer(r"  (store, load made dup, store|multiplications "
                                     r"joined): (\d+)", o.stderr):
                    used[rule][os.path.relpath(p, CHAPTER)] = int(m.group(2))
                src = os.path.join(w, "o.asm")
                open(src, "w").write(o.stdout)
                out = os.path.join(w, "o.vm")
                assert assemble(src, out), p
                if behaviour(vm, out) != want:
                    print("%s %s: behaves differently" % (rule or "no new rule",
                                                          os.path.relpath(p, CHAPTER)))
        print("%d programs, each optimised four ways" % len(programs))
        for rule in RULES[1:]:
            print("%s used in: %s" % (rule, ", ".join(
                "%s (%d)" % (p, n) for p, n in sorted(used[rule].items())) or "none"))

        print()
        sl = os.path.join(HERE, "storeload.asm")
        plain, dup = os.path.join(w, "sl.vm"), os.path.join(w, "sl-dup.vm")
        assemble(sl, plain)
        o = subprocess.run([sys.executable, opt, "-dup", sl], capture_output=True, text=True,
                           check=True)
        open(os.path.join(w, "sl-dup.asm"), "w").write(o.stdout)
        assemble(os.path.join(w, "sl-dup.asm"), dup)
        machines = [("vm-threaded", vm), ("vm-super", os.path.join(CHAPTER, "vm-super"))]
        print("storeload       %15s %15s" % ("as it is", "-dup"))
        for name, m in machines:
            print("%-15s %15s %15s   dispatched" % (name, "{:,}".format(steps(m, plain)),
                                                    "{:,}".format(steps(m, dup))))
        if "times" in sys.argv[1:]:
            for name, m in machines:
                print("%-15s %12.0f ms %12.0f ms   best of 7" % (name, best([m, plain]),
                                                               best([m, dup])))


main()
