#!/bin/sh
# Run every answer program and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
set -e
cd "$(dirname "$0")"
for run in count times fib-jnz:jnz gt fib-less fib-less-jnz:jnz fib:relative fib-moved:relative; do
    program=${run%%:*}
    option=$(echo "$run" | sed -n 's/.*://p')
    expected="$program$option.out"
    if [ "$1" = expect ]; then
        python3 run.py "$program.txt" $option > "$expected"
    else
        python3 run.py "$program.txt" $option | diff -u "$expected" -
    fi
done
