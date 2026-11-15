#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# The times are not checked: python3 jge.py times prints them.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
(cd .. && make -s test > /dev/null)     # every .vm and .rvm the answers read
python3 build.py "$work"
cc -std=c99 -O2 -o "$work/rvm" "$work/rvm.c"
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

answer copies python3 copies.py
answer jge python3 jge.py
answer jge-suite sh -c "cd .. && python3 conform.py --known garbage,calli,trap-calli-address,trap-calli-args,trap-calli-reference '$work/rvm-run' | sed 's|.*/rvm-run|rvm-run|' | grep passed"
answer jge-fib sh -c "cd .. && python3 '$work/translate.py' -l -jge bench/fib.vm /dev/null"
answer moves python3 moves.py
