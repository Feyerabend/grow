#!/bin/sh
# Exercise 5, by hand: the machine as it is, and with pc.patch, on the two
# benchmarks, each the best of five runs. Run from appE-jvm after
# make check, on mains power.
set -e
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cp jvm.h class.c verify.c run.c main.c "$work"
cc -std=c11 -O2 -o "$work/as-it-is" class.c verify.c run.c main.c
(cd "$work" && patch -s < "$OLDPWD/answers/pc.patch" && cc -std=c11 -O2 -o pc class.c verify.c run.c main.c)
python3 enkelj.py bench/fib30.p "$work"
python3 enkelj.py bench/sort4000.p "$work"
for b in Fib30 Sort4000; do
    for m in as-it-is pc; do
        python3 -c "
import subprocess, sys, time
t = []
for _ in range(5):
    s = time.perf_counter()
    subprocess.run(sys.argv[1:], stdout=subprocess.DEVNULL, check=True)
    t.append(time.perf_counter() - s)
print(f'$b $m: {min(t):.3f} s')" "$work/$m" "$work/$b.class"
    done
done
