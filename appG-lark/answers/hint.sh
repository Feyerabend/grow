#!/bin/sh
# Exercise G.5: the machine with and without __builtin_expect on the
# test between steps, and two builds between, each timed on the loop
# benchmark (the fastest of five) with the size of its main loop's
# function, in instructions. Not run by make check: times vary. Run it
# after make check, which writes build/loop.tree.
#   hint      as it is
#   plain     the hint taken out
#   noinline  the hint taken out, collect kept out of line
#   nomerge   as it is, but clang told not to merge the globals
set -e
cd "$(dirname "$0")/.."
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
CC=${CC:-cc}
F="-std=c11 -O2 -Wno-unused-parameter"
sed 's/if (__builtin_expect(_half_full, 0)) {/if (_half_full) {/' cek.c > "$work/plain.c"
sed 's/^static void collect(void) {/__attribute__((noinline)) static void collect(void) {/' \
    "$work/plain.c" > "$work/noinline.c"
cp cek.c "$work/hint.c"
cp cek.c "$work/nomerge.c"
for v in hint plain noinline nomerge; do
    x=""; [ $v = nomerge ] && x="-mllvm -enable-global-merge=false"
    $CC $F $x -I. -o "$work/$v" "$work/$v.c" tree.c main.c
    $CC $F $x -I. -S -o "$work/$v.s" "$work/$v.c"
    n=$(awk '/^_?cek_run_until:/{f=1} f&&/^\t[a-z]/{n++} f&&/\.cfi_endproc/{print n; exit}' "$work/$v.s")
    best=$(python3 -c '
import subprocess, sys, time
best = 99
for i in range(5):
    t = time.perf_counter()
    subprocess.run([sys.argv[1], "build/loop.tree"], stdout=subprocess.DEVNULL)
    best = min(best, time.perf_counter() - t)
print(f"{best:.3f}")' "$work/$v")
    echo "$v: ${best} s, cek_run_until $n instructions"
done
