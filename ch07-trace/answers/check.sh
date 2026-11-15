#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
python3 build.py > "$work/vm_more.c"
cc -std=c99 -O2 -Wall -Wextra -o "$work/vm" "$work/vm_more.c"
python3 asm_sym.py ../samples/primes.asm "$work/primes.vm"
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

answer symbols cat "$work/primes.sym"
answer debug-label sh -c "'$work/vm' -d '$work/primes.vm' < debug-label.txt"
answer debug-watch sh -c "'$work/vm' -d '$work/primes.vm' < debug-watch.txt"
answer profile sh -c "'$work/vm' -p '$work/primes.vm' 2>&1 >/dev/null"
answer tracetime python3 tracetime.py
