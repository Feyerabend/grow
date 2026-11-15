#!/usr/bin/env python3
"""
What a round trip costs: one RESUME and one YIELD, a million times, with the
coroutine waiting under calls of different depth, and for comparison a million
plain calls. Times are from this computer, best of three, and differ each time.
The chapter's table is one run of this.

    usage: python3 measure/cost.py [mark | copy]     (with ./vm built)
"""

import os
import re
import subprocess
import sys
import tempfile
import time

ROUNDS = 1000000

CALL = f"""main:   PUSH {ROUNDS}
loop:   DUP
        JZ end
        CALL f 0
        DROP
        PUSH 1
        SUB
        JMP loop
end:    HALT
f:      PUSH 1
        RET
"""


def yields(depth):
    return f"""main:   CORO body
        PUSH {ROUNDS}
loop:   DUP
        JZ end
        OVER
        PUSH 0
        RESUME
        DROP
        PUSH 1
        SUB
        JMP loop
end:    HALT
body:   PUSH {depth}
        CALL go 1
go:     LOAD 0
        JZ here
        LOAD 0
        PUSH 1
        SUB
        CALL go 1
here:
again:  PUSH 1
        YIELD
        DROP
        JMP again
"""


def measure(source, collector, folder):
    path = os.path.join(folder, "p")
    with open(path + ".asm", "w") as f:
        f.write(source)
    subprocess.run([sys.executable, "asm.py", path + ".asm", path + ".vm"], check=True)
    best = None
    for _ in range(3):
        start = time.perf_counter()
        result = subprocess.run(["./vm", "-s", "-g", collector, path + ".vm"],
                                capture_output=True, text=True, check=True)
        elapsed = time.perf_counter() - start
        best = elapsed if best is None else min(best, elapsed)
    made = int(re.search(r"(\d+) places in all", result.stderr).group(1))
    collections = int(re.search(r"(\d+) collections", result.stderr).group(1))
    collecting = re.search(r"([\d.]+) seconds collecting", result.stderr).group(1)
    return made, collections, collecting, best


def main():
    collector = sys.argv[1] if len(sys.argv) > 1 else "mark"
    print("                 places/trip  collections  collecting s  whole run ms")
    with tempfile.TemporaryDirectory() as folder:
        cases = [("a plain call", CALL)] + [(f"depth {d}", yields(d)) for d in (0, 5, 20, 60)]
        for name, source in cases:
            made, collections, collecting, best = measure(source, collector, folder)
            print(f"{name:<16} {made // ROUNDS:>11} {collections:>12} {collecting:>13} {best * 1000:>13.0f}")


if __name__ == "__main__":
    main()
