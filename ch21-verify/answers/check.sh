#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# The times are not checked: python3 kinds.py times prints them.
# About ten minutes: most of it is fuzzing, 1800 programs at a time.
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

answer kinds python3 kinds.py fuzz
answer room python3 room.py
answer shrink python3 shrink.py
answer holes python3 holes.py
