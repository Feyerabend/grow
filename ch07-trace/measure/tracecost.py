#!/usr/bin/env python3
"""
What a trace costs. A loop that counts a local down in a frame runs for about
two hundred thousand steps, three ways: plainly, traced into nothing (/dev/null), and
traced into a file; and then traced into a file by a copy of the machine whose
standard error is buffered, as standard output is. Timed best of three, with
the trace's size. The numbers
depend on the computer and its disk.

    usage: python3 measure/tracecost.py [count]     (from ch07-trace)
"""

import os
import subprocess
import sys
import tempfile
import time

LOOP = """
        PUSH {n}
        CALL count 1
        PRINT
        HALT
count:  LOAD 0
        JZ done
        LOAD 0
        PUSH 1
        SUB
        STORE 0
        JMP count
done:   PUSH 7
        RET
"""


def timed(args, out):
    best = None
    for _ in range(3):
        start = time.perf_counter()
        subprocess.run(args, stdout=subprocess.DEVNULL, stderr=out, check=True)
        t = time.perf_counter() - start
        best = t if best is None else min(best, t)
    return best


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30_000
    steps = 7 * n + 9
    with tempfile.TemporaryDirectory() as folder:
        src, prog, exe = (os.path.join(folder, x) for x in ("loop.asm", "loop.vm", "vm"))
        open(src, "w").write(LOOP.format(n=n))
        subprocess.run([sys.executable, "asm.py", src, prog], check=True)
        subprocess.run(["cc", "-std=c99", "-O2", "-o", exe, "vm.c"], check=True)
        plain = timed([exe, prog], subprocess.DEVNULL)
        null = timed([exe, "-t", prog], subprocess.DEVNULL)
        path = os.path.join(folder, "trace.txt")
        with open(path, "w") as f:
            to_file = timed([exe, "-t", prog], f)
        size = os.path.getsize(path)
        source = open("vm.c").read().replace(
            "int main(int argc, char *argv[]) {",
            "static char buffer[1 << 16];\n\nint main(int argc, char *argv[]) {\n"
            "    setvbuf(stderr, buffer, _IOFBF, sizeof buffer);", 1)
        c2, exe2 = os.path.join(folder, "vm_buffered.c"), os.path.join(folder, "vm_buffered")
        open(c2, "w").write(source)
        subprocess.run(["cc", "-std=c99", "-O2", "-o", exe2, c2], check=True)
        path2 = os.path.join(folder, "trace2.txt")
        with open(path2, "w") as f:
            buffered = timed([exe2, "-t", prog], f)
        assert open(path).read() == open(path2).read()
    print(f"{steps} steps")
    print(f"run:                 {plain:6.3f} s")
    print(f"traced, to nothing:  {null:6.2f} s  ({null / plain:.0f} times)")
    print(f"traced, to a file:   {to_file:6.2f} s  ({to_file / plain:.0f} times)")
    print(f"buffered, to a file: {buffered:6.2f} s  ({buffered / plain:.0f} times)")
    print(f"the trace: {size / 1e6:.0f} MB, {size / steps:.0f} bytes a step")


if __name__ == "__main__":
    main()
