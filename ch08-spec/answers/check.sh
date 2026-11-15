#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# Needs node for vm.js. About a minute: fuzz_forward.py runs 1000 programs.
set -e
cd "$(dirname "$0")"
here=$(pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cc -std=c99 -O1 -w -o "$work/vm" ../vm.c
mkdir "$work/dir.vm"
printf 'PUSH 1\nPRINT\nHALT\n' > "$work/one.asm"
python3 ../asm.py "$work/one.asm" "$work/one.vm"
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

answer js sh -c "cd .. && python3 conform.py node answers/vm.js | tail -1"
answer js-literal sh -c "cd .. && python3 conform.py node answers/vm_literal.js | tail -6"
answer directory sh -c "cd '$work' && for m in ./vm 'python3 $here/../vm.py' 'node $here/vm.js'; do
    \$m dir.vm; echo status \$?; done"
answer closed sh -c "cd '$work' && for m in ./vm 'python3 $here/../vm.py' 'node $here/vm.js'; do
    \$m one.vm >&-; echo status \$?; done"
answer fuzz python3 fuzz_forward.py 1000
answer coverage python3 coverage.py
