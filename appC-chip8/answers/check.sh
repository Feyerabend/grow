#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
set -e
cd "$(dirname "$0")"
mode=$1

answer() {
    name=$1
    shift
    if [ "$mode" = expect ]; then
        "$@" > "$name.out"
    else
        "$@" | diff -u "$name.out" -
    fi
}

C="python3 ../chip8.py"
answer keydigit $C -k 7 keydigit.hex            # 1, with the key 7
answer keydigit-nokey $C keydigit.hex           # 1, with no key
answer overlap $C overlap.hex                   # 2
answer multiply $C multiply.hex                 # 3
answer multiply-steps $C -n 31 multiply.hex     # 3: the loop is done after 31
answer shift-vip $C -m vip shift.hex            # 4
answer shift-chip48 $C -m chip48 shift.hex
echo "appendix C answers: ok"
