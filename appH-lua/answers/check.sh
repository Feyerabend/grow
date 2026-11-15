#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# three.asm and loop.asm run on chapter 19's machines, from ../../ch19-registers;
# the Lua programs need lua and luac 5.5 on the PATH. The byte counts
# in tables.out are those of Lua 5.5.1 on a 64-bit computer.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
ch19=../../ch19-registers
cc -std=c99 -O2 -w -o "$work/vm" $ch19/vm.c
cc -std=c99 -O2 -w -o "$work/rvm" $ch19/rvm.c
python3 $ch19/asm.py three.asm "$work/three.vm"
python3 $ch19/asm.py loop.asm "$work/loop.vm"
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

stack() {
    python3 $ch19/asm.py -l three.asm "$work/p.vm" | sed -n '/ f:/,$p'
}

registers() {
    python3 $ch19/translate.py -l "$work/three.vm" "$work/three.rvm" | sed -n '/^S18:/,$p'
}

luac_list() {   # without the addresses, which change from run to run
    luac -l -l -p "$1" | sed 's/ at 0x[0-9a-f]*//; s/ for 0x[0-9a-f]*//; s/; 0x[0-9a-f]*//'
}

answer three-stack stack
answer three-registers registers
answer three-run sh -c "'$work/vm' '$work/three.vm' && '$work/rvm' '$work/three.rvm'"
answer loop-registers sh -c "python3 $ch19/translate.py -l '$work/loop.vm' '$work/loop.rvm' && '$work/rvm' '$work/loop.rvm'"
answer shared lua shared.lua
answer shared-listing luac_list shared.lua
answer while lua while.lua
answer while-listing luac_list while.lua
answer tables lua tables.lua
