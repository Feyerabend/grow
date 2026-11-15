#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
set -e
cd "$(dirname "$0")"
cc -std=c99 -O1 -w -o vm ../vm.c
work=$(mktemp -d)
trap 'rm -rf "$work" vm' EXIT

answer() {
    name=$1
    shift
    if [ "$mode" = expect ]; then
        "$@" > "$name.out" 2>&1 || true
    else
        "$@" 2>&1 | diff -u "$name.out" - || exit 1
    fi
}
mode=$1

run() {             # tobin, then run on chapter 5's machine
    python3 "$1" "$2" "$work/p.vm" && ./vm "$work/p.vm"
}
answer squares run ../tobin.py squares.txt
answer primes-dup run ../tobin.py primes-dup.txt
answer xxd sh -c "python3 ../tobin.py ../samples/gcd.txt $work/gcd.vm && xxd $work/gcd.vm | head -2"
answer bad1 python3 tobin-checked.py bad1.txt "$work/x.vm"
answer bad2 python3 tobin-checked.py bad2.txt "$work/x.vm"
answer bad3 python3 tobin-checked.py bad3.txt "$work/x.vm"
answer samples-same sh -c "for s in gcd fib primes fact; do
    python3 tobin-checked.py ../samples/\$s.txt $work/a.vm
    python3 ../tobin.py ../samples/\$s.txt $work/b.vm
    cmp $work/a.vm $work/b.vm && echo \$s: the same bytes; done"
answer checksum python3 checksum.py
answer leb128 python3 leb128.py
