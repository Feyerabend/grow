#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# Times differ from run to run, and are measured apart: python3 table.py times
# About two minutes: the suite runs three times, and the table twice.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
python3 build.py > "$work/vm_keep.c"
cc -std=c99 -O2 -Wall -Wextra -o "$work/vm" "$work/vm_keep.c"
(cd .. && make -s vm)
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

answer keep-suite sh -c "cd .. && for o in 'mark' 'copy -S' 'mark -S'; do
    python3 conform.py '$work/vm' -g \$o | tail -1 | sed 's|.*/vm|vm_keep|'; done"
answer table python3 table.py
answer roundrobin sh -c "python3 ../asm.py roundrobin.asm '$work/rr.vm' && ../vm '$work/rr.vm' &&
    ../vm -g copy -S '$work/rr.vm'"
answer conway sh -c "for p in conway-function conway-coroutine; do echo \$p
    python3 ../lambda.py \$p.lam > '$work/p.asm' && python3 ../asm.py '$work/p.asm' '$work/p.vm' &&
    ../vm -s '$work/p.vm' 2>&1 | grep -v seconds; done"
answer generators python3 generators.py
