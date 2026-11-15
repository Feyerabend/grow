#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# copy.asm runs on chapter 13's machine, from ../../ch13-heap.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
ch13=../../ch13-heap
cc -std=c99 -O2 -w -o "$work/vm" $ch13/vm.c
mode=$1

answer() {
    name=$1
    shift
    if [ "$mode" = expect ]; then
        "$@" > "$name.out" 2>&1 || true
    else
        "$@" 2>&1 | diff -u "$name.out" - || exit 1
    fi
}

bytes() {
    python3 -c 'import sys; sys.path.insert(0, ".."); from sweet16 import assemble
print(assemble(open(sys.argv[1]).read()).hex(" ").upper())' "$1"
}

listing() {
    python3 $ch13/asm.py -l copy.asm "$work/p.vm" | sed -n '/^ *[0-9]* .*copy:/,$p'
}

answer zero-bytes bytes zero.s16
answer zero-run python3 ../sweet16.py -m A030:A03F zero-run.s16
answer copy6502 python3 copy6502.py
answer prior-sub python3 ../sweet16.py -t prior-sub.s16
answer prior-cpr python3 ../sweet16.py -t prior-cpr.s16
answer copy-listing listing
answer copy "$work/vm" "$work/p.vm"
