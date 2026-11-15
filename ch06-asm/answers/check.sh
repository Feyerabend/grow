#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# The programs run on chapter 5's machine, which reads the same .vm files.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cc -std=c99 -O1 -w -o "$work/vm" ../../ch05-files/vm.c
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

run() {             # assemble with the given assembler, then run
    python3 "$1" "$2" "$work/p.vm" && "$work/vm" "$work/p.vm"
}
answer table run ../asm.py table.asm
answer data run ../asm.py data.asm
answer data-disasm sh -c "python3 ../asm.py data.asm $work/d.vm && python3 ../disasm.py $work/d.vm"
answer equ run asm_more.py equ.asm
answer dead run asm_more.py dead.asm
answer samples-same sh -c "for s in ../samples/*.asm; do
    python3 asm_more.py \$s $work/a.vm && python3 ../asm.py \$s $work/b.vm
    cmp $work/a.vm $work/b.vm && echo \$(basename \$s): the same, no warnings; done"
answer bad python3 onepass_checked.py bad.asm
answer onepass-samples sh -c "for s in ../samples/*.asm table.asm; do
    python3 onepass_checked.py \$s | tail -1; done"
