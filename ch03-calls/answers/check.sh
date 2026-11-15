#!/bin/sh
# Run every answer program and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
set -e
cd "$(dirname "$0")"
while read -r name program options; do
    [ -n "$name" ] || continue
    if [ "$1" = expect ]; then
        python3 run.py "$program.txt" $options > "$name.out"
    else
        python3 run.py "$program.txt" $options | diff -u "$name.out" -
    fi
done <<'EOF'
square square
gcd gcd mod
factloop factloop
fact12 fact N=12
fact13 fact N=13
fact34 fact N=34
fact100000 fact N=100000 asan
sum127 sum N=127 asan
sum128 sum N=128 asan
fib-locals fib-locals
fib-mixed fib-mixed
fib-mixed2 fib-mixed2
EOF
