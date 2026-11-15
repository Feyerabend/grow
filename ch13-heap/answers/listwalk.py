#!/usr/bin/env python3
"""
Exercise 13.6: a program that uses the heap, timed. A list of 1000 cells,
each a block of two fields (a value, and the next cell), walked 1000 times,
adding up the values. Chapter 10's machine has no heap, so what to compare
with is the same list kept in memory: cell i at addresses 2i and 2i + 1, and
"next" an address. Both programs are in assembly, and print the same sum.

    heap     this chapter's machine, the list in blocks
    memory   this chapter's machine, the list in memory
    int      chapter 10's machine, the list in memory: no tags at all

Best of five runs, cc -O2, as measure/tags.py does.

    usage: python3 listwalk.py
"""

import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CH13 = os.path.join(HERE, "..")
CH10 = os.path.join(HERE, "..", "..", "ch10-enkel")

CELLS, ROUNDS = 1000, 1000

HEAP = f"""
; the list in blocks: cell = [value, next], next 0 at the end
main:   PUSH 0                  ; local 0: the list
        PUSH 0                  ; local 1: i
make:   LOAD 1
        PUSH {CELLS}
        LT
        JZ made
        PUSH 2
        NEW
        DUP
        PUSH 0
        LOAD 1
        SETF                    ; value i
        DUP
        PUSH 1
        LOAD 0
        SETF                    ; next: the list so far
        STORE 0
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP make
made:   PUSH 0                  ; local 2: round
        PUSH 0                  ; local 3: sum
round:  LOAD 2
        PUSH {ROUNDS}
        LT
        JZ done
        LOAD 0                  ; local 4: the cell
walk:   LOAD 4
        PUSH 0
        EQ
        JZ step
        DROP
        LOAD 2
        PUSH 1
        ADD
        STORE 2
        JMP round
step:   LOAD 3
        LOAD 4
        PUSH 0
        GETF
        ADD
        STORE 3
        LOAD 4
        PUSH 1
        GETF
        STORE 4
        JMP walk
done:   LOAD 3
        PRINT
        HALT
"""

MEMORY = f"""
; the same list in memory: cell i at 2i + 2 (value) and 2i + 3 (next), 0 the end
main:   PUSH 0                  ; local 0: the list
        PUSH 0                  ; local 1: i
make:   LOAD 1
        PUSH {CELLS}
        LT
        JZ made
        LOAD 1
        PUSH 2
        MUL
        PUSH 2
        ADD                     ; the new cell's address
        DUP
        LOAD 1
        STOREM                  ; value i
        DUP
        PUSH 1
        ADD
        LOAD 0
        STOREM                  ; next: the list so far
        STORE 0
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP make
made:   PUSH 0                  ; local 2: round
        PUSH 0                  ; local 3: sum
round:  LOAD 2
        PUSH {ROUNDS}
        LT
        JZ done
        LOAD 0                  ; local 4: the cell
walk:   LOAD 4
        PUSH 0
        EQ
        JZ step
        DROP
        LOAD 2
        PUSH 1
        ADD
        STORE 2
        JMP round
step:   LOAD 3
        LOAD 4
        LOADM
        ADD
        STORE 3
        LOAD 4
        PUSH 1
        ADD
        LOADM
        STORE 4
        JMP walk
done:   LOAD 3
        PRINT
        HALT
"""


def best(command):
    times = []
    for _ in range(5):
        start = time.perf_counter()
        r = subprocess.run(command, capture_output=True, text=True, check=True)
        times.append(time.perf_counter() - start)
    return min(times) * 1000, r.stdout.strip()


def main():
    with tempfile.TemporaryDirectory() as work:
        files = {}
        for name, text in (("heap", HEAP), ("memory", MEMORY)):
            src, vm = os.path.join(work, name + ".asm"), os.path.join(work, name + ".vm")
            open(src, "w").write(text)
            subprocess.run([sys.executable, os.path.join(CH13, "asm.py"), src, vm], check=True)
            files[name] = vm
        exes = {}
        for name, folder in (("ch13", CH13), ("ch10", CH10)):
            exes[name] = os.path.join(work, name)
            subprocess.run(["cc", "-std=c99", "-O2", "-w", "-o", exes[name], os.path.join(folder, "vm.c")],
                           check=True)
        runs = [("heap", exes["ch13"], files["heap"]), ("memory", exes["ch13"], files["memory"]),
                ("int", exes["ch10"], files["memory"])]
        timing = "times" in sys.argv[1:]
        print(f"{CELLS} cells, walked {ROUNDS} times")
        for name, exe, vm in runs:
            ms, out = best([exe, vm])
            print(f"  {name:7} prints {out}" + (f", best of 5 {ms:5.0f} ms" if timing else ""))


if __name__ == "__main__":
    main()
