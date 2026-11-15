#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cc -std=c99 -O1 -w -o "$work/vm" ../vm.c
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

run() {             # compile with the given compiler, assemble, run
    python3 "$1" "$2" > "$work/p.asm" && python3 ../asm.py "$work/p.asm" "$work/p.vm" &&
        "$work/vm" "$work/p.vm"
}
answer calls run enkel_calls.py calls.p
answer for run enkel_for.py for.p
answer bounds sh -c "python3 bounds.py 2>/dev/null"
answer measure python3 measure_more.py
