"""Break the verifier one rule at a time, and see what notices.

    python3 measure/mutants.py [seeds]

Run from the chapter's folder. For each of the verifier's refusals in
vm.c, a copy is made in which that refusal is taken out: where it would
refuse, it accepts, and stops following that path. Each copy is built
twice, as ./vm and as the sanitizer build of fuzz.sh, and tried three
ways: the suite's list of verdicts (tests/verdicts.txt), the conformance
suite, and the fuzzer with the given number of seeds of 600 programs
(default 3). The unbroken verifier is tried the same way first.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
HERE = os.getcwd()


def build(source, folder):
    for f in ["loop.h", "ops.h"]:
        if not os.path.exists(os.path.join(folder, f)):
            os.symlink(os.path.join(HERE, f), os.path.join(folder, f))
    path = os.path.join(folder, "vm.c")
    open(path, "w").write(source)
    vm, fuzz = os.path.join(folder, "vm"), os.path.join(folder, "vm-fuzz")
    subprocess.run(["cc", "-std=gnu99", "-O2", "-o", vm, path], check=True,
                   stderr=subprocess.DEVNULL)
    subprocess.run(["cc", "-std=gnu99", "-O1", "-g", "-fsanitize=address,undefined",
                    "-fno-sanitize-recover=all", "-DSTEP_LIMIT=20000", "-o", fuzz, path],
                   check=True, stderr=subprocess.DEVNULL)
    return vm, fuzz


def verdicts(vm, folder):
    lines = []
    for asm in sorted(f for f in os.listdir("suite") if f.endswith(".asm")):
        v = os.path.join(folder, "v.vm")
        subprocess.run([sys.executable, "asm.py", "suite/" + asm, v], check=True)
        r = subprocess.run([vm, "-V", v], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                           text=True)
        m = re.search(r"not verified: (.*)", r.stderr)
        lines.append("%s: %s" % (asm[:-4], m.group(1) if m else "verified"))
    return "\n".join(lines) + "\n" != open("tests/verdicts.txt").read()


def conform(vm):
    r = subprocess.run([sys.executable, "conform.py", vm], capture_output=True, text=True)
    m = re.search(r"(\d+) of (\d+) passed", r.stdout + r.stderr)
    return int(m.group(1)), int(m.group(2))


def fuzz(fuzzvm, dirs):
    caught = 0
    for d in dirs:
        r = subprocess.run(["./fuzz.sh", fuzzvm, d], capture_output=True, text=True)
        caught += len([l for l in r.stdout.splitlines() if l.endswith(("differ", "complained"))])
    return caught


def main():
    source = open("vm.c").read()
    messages = re.findall(r'ok = refuse\(pc, "([^"]+)"\);', source)
    with tempfile.TemporaryDirectory() as top:
        dirs = []
        for seed in range(1, SEEDS + 1):
            d = os.path.join(top, "fuzz%d" % seed)
            subprocess.run([sys.executable, "fuzz.py", str(seed), "600", d], check=True,
                           stdout=subprocess.DEVNULL)
            dirs.append(d)
        print("%d fuzz programs, seeds 1 to %d" % (600 * SEEDS, SEEDS))
        print("%-58s %9s %8s %6s" % ("refusal taken out", "verdicts", "suite", "fuzz"))
        for message in [None] + messages:
            folder = tempfile.mkdtemp(dir=top)
            text = source
            if message:
                old = 'ok = refuse(pc, "%s");' % message
                assert text.count(old) == 1, message
                text = text.replace(old, "(void) 0;")
            vm, fuzzvm = build(text, folder)
            v = "changed" if verdicts(vm, folder) else "same"
            passed, total = conform(vm)
            f = fuzz(fuzzvm, dirs)
            print("%-58s %9s %4d/%d %6d" % (message or "(none: the verifier as it is)", v,
                                             passed, total, f))
            sys.stdout.flush()
            shutil.rmtree(folder)


main()
