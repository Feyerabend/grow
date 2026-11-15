#!/usr/bin/env python3
"""
Exercise 21.5: the four refusals that nothing noticed.

    python3 holes.py [seeds]

Run from this folder. First, as measure/mutants.py does for the refusal of
a function called with different numbers of arguments: the verifier with it
taken out, and the verifier as it is, tried with fuzz.py's programs and with
fuzz_more.py's, the given number of seeds of 600 (default 3).

Then the other three, each with a program written to show what taking it
out does, run as fuzz.sh runs a program, verified and checked, with
sanitizers. Each is taken out in two ways: as mutants.py does it, where
the verifier accepts the whole program at the point where it would have
refused; and by deleting the test, so that the verifier goes on as if it
had passed.
"""

import os
import subprocess
import sys
import tempfile

import shrink

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)

DELETE = {
    "a jump into the middle of an instruction": """        if (!begins[pc]) {
            ok = refuse(pc, "a jump into the middle of an instruction");
            break;
        }
""",
    "more values than the stack has room for": """        if (after > STACK_SIZE) {
            ok = refuse(pc, "more values than the stack has room for");
            break;
        }
""",
    "code shared by two functions": """            else if (owner[pc] != fn)
                ok = refuse(pc, "code shared by two functions");
""",
}
PROGRAMS = [("a jump into the middle of an instruction", "middle.asm"),
            ("more values than the stack has room for", "room-full.asm"),
            ("code shared by two functions", "shared.asm"),
            ("code shared by two functions", "shared-ret.asm")]


def deleted(folder, message):
    os.makedirs(folder)
    for f in ["loop.h", "ops.h"]:
        os.symlink(os.path.join(CHAPTER, f), os.path.join(folder, f))
    s = open(os.path.join(CHAPTER, "vm.c")).read()
    assert s.count(DELETE[message]) == 1, message
    open(os.path.join(folder, "vm.c"), "w").write(s.replace(DELETE[message], ""))
    vm = os.path.join(folder, "vm-fuzz")
    subprocess.run(["cc", "-std=gnu99", *shrink.FUZZ, "-o", vm, os.path.join(folder, "vm.c")],
                   check=True, stderr=subprocess.DEVNULL)
    return vm


def unbroken(folder):
    os.makedirs(folder)
    vm = os.path.join(folder, "vm-fuzz")
    subprocess.run(["cc", "-std=gnu99", *shrink.FUZZ, "-I", CHAPTER, "-o", vm,
                    os.path.join(CHAPTER, "vm.c")], check=True, stderr=subprocess.DEVNULL)
    return vm


def caught(vm, dirs):
    n = 0
    for d in dirs:
        for name in sorted(os.listdir(d)):
            if shrink.failure(vm, os.path.join(d, name)):
                n += 1
    return n


def verdict(vm, program):
    r = subprocess.run([vm, "-V", program], capture_output=True, text=True)
    return "refused" if r.returncode == 2 and "not verified" in r.stderr else "verified"


def main():
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    with tempfile.TemporaryDirectory() as w:
        plain, more = [], []
        for seed in range(1, seeds + 1):
            for gen, dirs in [(os.path.join(CHAPTER, "fuzz.py"), plain),
                              (os.path.join(HERE, "fuzz_more.py"), more)]:
                d = os.path.join(w, "%s%d" % (os.path.basename(gen)[:-3], seed))
                subprocess.run([sys.executable, gen, str(seed), "600", d], check=True)
                dirs.append(d)
        message = "a function called with different numbers of arguments"
        vms = [("the verifier as it is", unbroken(os.path.join(w, "as-is"))),
               ("taken out: " + message, shrink.mutant(os.path.join(w, "args"), message))]
        print("%d programs from each generator; how many fail" % (600 * seeds))
        print("%-68s %8s %10s" % ("", "fuzz.py", "fuzz_more"))
        for name, vm in vms:
            print("%-68s %8d %10d" % (name, caught(vm, plain), caught(vm, more)))
        print()
        for n, (message, name) in enumerate(PROGRAMS):
            src = os.path.join(HERE, name)
            program = os.path.join(w, name[:-4] + ".vm")
            subprocess.run([sys.executable, os.path.join(CHAPTER, "asm.py"), src, program],
                           check=True)
            print("%s, taken out of the verifier, and %s:" % (message, name))
            for way, vm in [("as the verifier is", vms[0][1]),
                            ("as mutants.py takes it out",
                             shrink.mutant(os.path.join(w, "m%d" % n), message)),
                            ("with the test deleted", deleted(os.path.join(w, "d%d" % n),
                                                              message))]:
                f = shrink.failure(vm, program)
                print("  %-28s %-9s %s" % (way, verdict(vm, program),
                                           f or "verified and checked runs the same"))


main()
