#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# The times are not checked: python3 times.py, python3 jit.py times and
# python3 wasm.py times print them. About ten minutes.
set -e
cd "$(dirname "$0")"
(cd .. && make -s vm benchmarks)
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

# 22.1 and 22.2: the suite, compiled each way; then random programs.
answer suite sh -c 'cd .. && for m in "-cache" "-calls" "-cache -calls"; do
    echo "vm2c_more.py $m"
    VM2C_MORE="$m" python3 conform.py answers/vmc-more | tail -1
    VM2C_MORE="$m" python3 conform.py answers/vmc-more -g copy -S | tail -1
    done'
answer compare python3 compare.py
answer jit python3 jit.py
answer wasm sh -c 'python3 wasm.py && cd .. && python3 conform.py answers/wasm/vmw | tail -1 &&
    python3 conform.py answers/wasm/vmw -g copy -S | tail -1'
answer lean sh -c 'for b in loop fib sieve; do echo "$b:"; python3 lean.py $b; done'
