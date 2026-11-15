#!/usr/bin/env python3
"""The benchmarks, timed: each the best of five runs, in wall-clock time,
on chapter 10's machine, on this JVM, and on Java, interpreting only
(-Xint) and as it is, compiling hot code to native code.

    usage: bench/time.py [java]        run from appE-jvm, after make check
"""

import os
import subprocess
import sys
import time

ENKEL = "../ch10-enkel"
BENCH = ["fib30", "sort4000", "hello"]


def best(command, runs=5):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
        times.append(time.perf_counter() - start)
    return min(times)


def main():
    java = sys.argv[1] if len(sys.argv) > 1 else None
    os.makedirs("build/bench", exist_ok=True)
    print(f"{'':10} {'chapter 10':>11} {'this JVM':>9}" +
          (f" {'Java -Xint':>11} {'Java':>7}" if java else ""))
    for b in BENCH:
        subprocess.run([sys.executable, "enkelj.py", f"bench/{b}.p", "build/bench"], check=True)
        with open(f"build/bench/{b}.asm", "w") as f:
            subprocess.run([sys.executable, f"{ENKEL}/enkel.py", f"bench/{b}.p"], stdout=f, check=True)
        subprocess.run([sys.executable, f"{ENKEL}/asm.py", f"build/bench/{b}.asm",
                        f"build/bench/{b}.vm"], check=True)
        cls = b[:1].upper() + b[1:]
        row = [best([f"{ENKEL}/vm", f"build/bench/{b}.vm"]),
               best(["build/jvm", f"build/bench/{cls}.class"])]
        if java:
            row += [best([java, "-Xint", "-cp", "build/bench", cls]),
                    best([java, "-cp", "build/bench", cls])]
        print(f"{b:10}" + "".join(f" {t:>{w}.3f}" for t, w in zip(row, (11, 9, 11, 7))))


if __name__ == "__main__":
    main()
