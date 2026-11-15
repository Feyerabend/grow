#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# listwalk.py's times differ from run to run: python3 listwalk.py times
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cc -std=c99 -O2 -w -o "$work/vm" ../vm.c
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

run() {
    python3 ../asm.py "$1" "$work/p.vm" && "$work/vm" "$work/p.vm"
}
answer concat run concat.asm
answer points run points.asm
answer full run full.asm
answer oom python3 oom_check.py
answer stale python3 stale.py
answer listwalk python3 listwalk.py
