#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# four.py's times differ from run to run and are left out here: python3 four.py times
set -e
cd "$(dirname "$0")"
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

answer pow python3 pow_check.py
answer cond python3 cond_check.py
answer label python3 label_check.py
answer four python3 four.py
answer late python3 late.py
