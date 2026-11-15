#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# The times are not checked: python3 times.py [-O0] prints them.
# The counts of machine instructions and jumps are for arm64 and Apple clang.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
python3 build.py > "$work/vm_more.c"
for d in subroutine spread indirect; do
    D=$(echo $d | tr a-z A-Z)
    cc -std=gnu99 -O2 -Wall -Wextra -I.. -DDISPATCH=$D -o "$work/vm-$d" "$work/vm_more.c"
done
(cd .. && make -s benchmarks)
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

# Every new build passes the suite and gets the benchmarks right.
answer builds sh -c "cd .. && for d in subroutine spread indirect; do
    python3 conform.py '$work/vm-'\$d -g mark | sed 's|.*/vm-|vm-|'
    python3 conform.py '$work/vm-'\$d -g copy -S | sed 's|.*/vm-|vm-|'
    for b in fib loop sieve closures; do
        '$work/vm-'\$d bench/\$b.vm | diff -q bench/\$b.out - && echo \"vm-\$d \$b: right\"
    done; done"
answer pairs python3 pairs.py
answer addcount python3 addcount.py
answer jumps python3 jumps.py
