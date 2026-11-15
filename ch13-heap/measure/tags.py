#!/usr/bin/env python3
"""
What do the tags cost a program that never uses the heap?

Two programs in enkel/0, compiled by chapter 10's enkel.py and assembled
once, run on two machines built with cc -O2: chapter 10's vm.c, where a value
is an int, and this chapter's, where a value is a tag and an int, and every
arithmetic instruction checks the tag. A third machine is this chapter's with
the checks taken out of number() and block(), to see what the checks alone
cost. The two chapters' instruction loops are also written differently: this
chapter's shares one case among the nine arithmetic instructions. The best of five runs of each, as the
time the shell's clock gives, and the size of the machine's arrays.

    sieve      the primes below 4000, found 400 times over
    fib        fib(24) by plain recursion, 20 times over

    usage: python3 measure/tags.py      (run in code/ch13-heap)
"""

import os
import subprocess
import sys
import tempfile
import time

HERE = os.getcwd()
ENKEL = os.path.join(HERE, "..", "ch10-enkel")

SIEVE = """
const size = 4000;
array marked:4000;
var round, p, m, count;
begin
    round is 0;
    while round < 400 do
    begin
        p is 0;
        while p < size do begin marked.p is 0; p is p + 1 end;
        p is 2;
        while p * p < size do
        begin
            if marked.p = 0 then
            begin
                m is p * p;
                while m < size do begin marked.m is 1; m is m + p end
            end;
            p is p + 1
        end;
        count is 0;
        p is 2;
        while p < size do
        begin
            if marked.p = 0 then count is count + 1;
            p is p + 1
        end;
        round is round + 1
    end;
    print count
end.
"""

FIB = """
var round;
procedure fib[n];
  var a, b, k;
  begin
    if n < 2 then return n;
    k is n - 1;
    call fib[k];
    a is rval;
    k is n - 2;
    call fib[k];
    b is rval;
    rval is a + b
  end;
begin
  round is 0;
  while round < 20 do begin call fib[24]; round is round + 1 end;
  print rval
end.
"""


def best(command, runs=5):
    times, out = [], None
    for _ in range(runs):
        t = time.perf_counter()
        r = subprocess.run(command, capture_output=True, check=True)
        times.append(time.perf_counter() - t)
        out = r.stdout
    return min(times), out


def main():
    with tempfile.TemporaryDirectory() as tmp:
        machines = {}
        unchecked = open("vm.c").read()
        for check in ('if (v.is_ref)\n        trap("not a number");',
                      'if (!v.is_ref)\n        trap("not a reference");'):
            assert unchecked.count(check) == 1
            unchecked = unchecked.replace(check, "")
        with open(os.path.join(tmp, "unchecked.c"), "w") as f:
            f.write(unchecked)
        for name, source in (("int", os.path.join(ENKEL, "vm.c")),
                             ("tagged", "vm.c"),
                             ("unchecked", os.path.join(tmp, "unchecked.c"))):
            binary = os.path.join(tmp, f"vm-{name}")
            subprocess.run(["cc", "-std=c99", "-O2", "-o", binary, source], check=True)
            machines[name] = binary
        print(f"{'program':8} {'int':>9} {'tagged':>9} {'unchecked':>10}")
        for name, text in (("sieve", SIEVE), ("fib", FIB)):
            p = os.path.join(tmp, f"{name}.p")
            with open(p, "w") as f:
                f.write(text)
            asm = os.path.join(tmp, f"{name}.asm")
            vm = os.path.join(tmp, f"{name}.vm")
            with open(asm, "w") as f:
                subprocess.run([sys.executable, os.path.join(ENKEL, "enkel.py"), p],
                               stdout=f, check=True)
            subprocess.run([sys.executable, "asm.py", asm, vm], check=True)
            t1, out1 = best([machines["int"], vm])
            t2, out2 = best([machines["tagged"], vm])
            t3, out3 = best([machines["unchecked"], vm])
            assert out1 == out2 == out3, name
            print(f"{name:8} {1000 * t1:6.0f} ms {1000 * t2:6.0f} ms {1000 * t3:7.0f} ms"
                  f"   prints {out1.decode().split()[-1]}")
    for name, size in (("int", 4), ("tagged", 8)):
        print(f"{name}: a value is {size} bytes; stack and memory"
              f" {(256 + 4096) * size} bytes")
    print("tagged: the heap, 65536 values, another", 65536 * 8, "bytes")


if __name__ == "__main__":
    main()
