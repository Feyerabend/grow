#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# About a minute: the race runs for many turns, traced.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cc -std=c99 -O2 -w -o "$work/vm" ../vm.c
(cd .. && make -s vm)                   # race_model.py runs the chapter's own ./vm
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

answer inc python3 inc.py
answer race-model python3 race_model.py
answer queue sh -c "for t in 1 2 3 5 7 11 50 0; do
    python3 -c \"import sys; s = open('queue.asm').read().replace('        PUSH 3\\n        SLICE', '        PUSH \$t\\n        SLICE', 1); open('$work/q.asm', 'w').write(s)\"
    python3 ../asm.py '$work/q.asm' '$work/q.vm'
    printf 'turn %s: ' \$t; '$work/vm' '$work/q.vm' | tr '\n' ' '; echo; done"
answer embrace python3 embrace.py
answer scheduler sh -c "python3 ../lambda.py scheduler.lam > '$work/s.asm' &&
    python3 ../asm.py '$work/s.asm' '$work/s.vm' && '$work/vm' '$work/s.vm'"
