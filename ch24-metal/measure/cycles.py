"""Clock cycles against instructions, and how fast the simulation runs.

    python3 measure/cycles.py

Run from the chapter's folder, after make test, on mains power. For each
program in samples/, it takes the cycles the simulated CPU needed
(vrun.py -c), the instructions chapter 18's C machine executed for the
same program (a copy of ../ch18-dispatch/vm.c with a counter at the
fetch, built here), and the best of three wall-clock times of the
simulation, which includes starting vvp and loading the program.
"""

import os
import subprocess
import tempfile
import time

C = "../ch18-dispatch"
SAMPLES = sorted(f[:-4] for f in os.listdir("samples") if f.endswith(".asm"))

COUNTER = r"""
static long long counted;

__attribute__((destructor)) static void report_counts(void) {
    fprintf(stderr, "count %lld\n", counted);
}

static void run(void) {"""


def counting_build(work):
    source = open(os.path.join(C, "vm.c")).read()
    marker = "#define UNKNOWN     default:\n\nstatic void run(void) {"
    fetch = "        op = code[pc++];\n        switch (op) {"
    assert source.count(marker) == 1 and source.count(fetch) == 1
    source = source.replace(marker, "#define UNKNOWN     default:\n" + COUNTER)
    source = source.replace(fetch, "        op = code[pc++];\n        counted++;\n"
                                   "        switch (op) {")
    path = os.path.join(work, "vm.c")
    open(path, "w").write(source)
    os.symlink(os.path.abspath(os.path.join(C, "ops.h")), os.path.join(work, "ops.h"))
    binary = os.path.join(work, "vm-count")
    subprocess.run(["cc", "-std=c99", "-O2", "-DDISPATCH=SWITCH", "-o", binary, path],
                   check=True)
    return binary


def last_number(stderr, word):
    for line in stderr.splitlines():
        if line.startswith(word + " "):
            return int(line.split()[1])
    raise SystemExit("no %s line" % word)


with tempfile.TemporaryDirectory() as work:
    counter = counting_build(work)
    print("%-26s %10s %12s %9s %12s" %
          ("", "cycles", "instructions", "seconds", "cycles/s"))
    for s in SAMPLES:
        vm = "samples/%s.vm" % s
        times = []
        for _ in range(3):
            start = time.perf_counter()
            p = subprocess.run(["python3", "vrun.py", "-c", vm],
                               capture_output=True, text=True)
            times.append(time.perf_counter() - start)
        cycles = last_number(p.stderr, "cycles")
        q = subprocess.run([counter, vm], capture_output=True, text=True)
        count = last_number(q.stderr, "count")
        print("%-26s %10d %12d %9.2f %12.0f" %
              (s, cycles, count, min(times), cycles / min(times)))
