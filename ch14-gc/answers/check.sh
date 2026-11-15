#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# Times differ from run to run, and are measured apart: python3 times.py
# About two minutes: the suite runs eight times.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
python3 build.py > "$work/vm_more.c"
cc -std=c99 -O2 -Wall -Wextra -o "$work/vm" "$work/vm_more.c"
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

counts() {          # a program under the four collectors, without the times
    python3 ../asm.py "$1" "$work/p.vm"
    for g in mark next copy compact; do
        echo "-g $g"
        "$work/vm" -g $g -s "$work/p.vm" 2>&1 | grep -v "seconds"
    done
}
answer suite sh -c "cd .. && for g in mark next copy compact; do
    python3 conform.py '$work/vm' -g \$g | tail -1 | sed 's|.*/vm |vm |'
    python3 conform.py '$work/vm' -g \$g -S | tail -1 | sed 's|.*/vm |vm |'; done"
answer trees counts ../samples/trees.asm
answer frag counts frag.asm
answer fit counts fit.asm
