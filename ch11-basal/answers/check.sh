#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# About a minute: stream_memory.py compiles 20000 lines twice.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
python3 build_vm.py > "$work/vm_read.c"
cc -std=c99 -O1 -Wall -Wextra -o "$work/vm" "$work/vm_read.c"
cc -std=c99 -O1 -w -o "$work/vm_plain" ../vm.c
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

answer input python3 run.py input.bas "$work/vm" '1 2\n30 -4\n'
answer input-bad python3 run.py input.bas "$work/vm" '1 x\n'
answer forlimit python3 run.py forlimit.bas "$work/vm"
answer forlimit-old sh -c "python3 ../basal.py forlimit.bas > '$work/o.asm' &&
    python3 ../asm.py '$work/o.asm' '$work/o.vm' && '$work/vm_plain' '$work/o.vm'"
answer leave python3 basal_more.py leave.bas
answer samples sh -c "for s in ../samples/*.bas; do
    python3 basal_more.py \$s > /dev/null && echo \$(basename \$s): accepted
    python3 basal_stream.py \$s | cmp -s - \$(python3 ../basal.py \$s > '$work/a.asm'; echo '$work/a.asm') &&
        echo \$(basename \$s): the stream writes the same; done"
answer gcd python3 gcd_compare.py
answer stream python3 stream_memory.py
