#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# The times are not checked: python3 choose.py times and python3 rules.py
# times print them. A few minutes: choose.py runs the suite on four builds.
set -e
cd "$(dirname "$0")"
(cd .. && make -s all benchmarks)
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

answer counts python3 counts.py
answer choose python3 choose.py check
answer rules python3 rules.py
