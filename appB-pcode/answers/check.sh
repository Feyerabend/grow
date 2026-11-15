#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# Each answer that changes a machine is a patch, applied here to a copy:
#   display.patch       p4.c with a display (exercise 1)
#   eof.patch           pcom.p, mended at the end of its input (exercise 2)
#   readln-p4.patch     p4.c, and
#   readln-pint.patch   pint.p, reading readln(prd) from prd (exercise 5)
# The mended pint is built and run only if Free Pascal is installed.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
CC=${CC:-cc}
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

build() {       # build name [patch]: p4.c, patched or not, as $work/name
    cp ../p4.c "$work/$1.c"
    [ -z "$2" ] || patch -s "$work/$1.c" < "$2"
    $CC -std=c99 -O2 -w -o "$work/$1" "$work/$1.c" -lm
}
build p4
build display display.patch
build mended readln-p4.patch
python3 ../p4/adapt.py self < ../p4/pcom.p > "$work/self.p"

# 1. With a display, pcom compiles itself to the same code, and every
#    program in the suite compiles and prints the same.
display() {
    "$work/display" -s ../p4/pcom.p4 "$work/pcom.p4" < "$work/self.p" 2> "$work/counts" > /dev/null
    cmp ../p4/pcom.p4 "$work/pcom.p4" || return 1
    echo "pcom compiles itself to the same code"
    head -3 "$work/counts"
    for f in ../pascal/*.pas; do
        s=$(basename "$f" .pas)
        in=/dev/null; [ -f "../pascal/$s.in" ] && in="../pascal/$s.in"
        "$work/display" ../p4/pcom.p4 "$work/$s.p4" < "$f" > /dev/null
        cmp "../pascal/$s.p4" "$work/$s.p4" || return 1
        "$work/display" "$work/$s.p4" < "$in" > "$work/$s.out"
        if [ "$s" = reals ]; then   # pint's reals, one apart in the last figure at most
            python3 ../lastdigit.py "../pascal/$s.out" "$work/$s.out" || return 1
        else
            cmp "../pascal/$s.out" "$work/$s.out" || return 1
        fi
    done
    echo "the suite's programs compile and print the same"
}

# 2. pcom mended compiles itself, as compiled by pcom, to the same code
#    as it was compiled to; and ends on programs cut short, which made
#    it write "*** eof encountered" without end.
eof() {
    cp ../p4/pcom.p "$work/fixed.p"
    patch -s "$work/fixed.p" < eof.patch
    python3 ../p4/adapt.py self < "$work/fixed.p" > "$work/selffixed.p"
    "$work/p4" ../p4/pcom.p4 "$work/a.p4" < "$work/selffixed.p" > /dev/null
    "$work/p4" "$work/a.p4" "$work/b.p4" < "$work/selffixed.p" > /dev/null
    cmp "$work/a.p4" "$work/b.p4" || return 1
    echo "mended pcom compiles itself to the same code"
    for s in 'program p(output); begin' \
             'program p(output); var x: integer; begin x := 12' \
             "program hello(output)/
begin
    writeln('Hello, world!')
end"; do
        printf '%s' "$s" > "$work/cut.pas"     # no end of line at the end
        "$work/p4" "$work/a.p4" "$work/cut.p4" < "$work/cut.pas"
        echo "status $?"
    done
}

# 5. readprd.pas reads "ab" and "cd" from prd, which follows its code,
#    and "xy" and "zw" from input. Right is "ac x"; as P4 was, "ab z".
readln() {
    "$work/p4" ../p4/pcom.p4 "$work/r.p4" < readprd.pas > /dev/null
    printf 'ab\ncd\n' | cat "$work/r.p4" - > "$work/rd.p4"
    printf 'as it was: '; printf 'xy\nzw\n' | "$work/p4" "$work/rd.p4"
    printf 'mended:    '; printf 'xy\nzw\n' | "$work/mended" "$work/rd.p4"
}

pint() {
    FPC=${FPC:-fpc}
    cp ../p4/pint.p "$work/pint.p"
    patch -s "$work/pint.p" < readln-pint.patch
    python3 ../p4/adapt.py pint < "$work/pint.p" > "$work/pintfpc.p"
    $FPC -Miso -v0 -FE"$work" -o"$work/pint" "$work/pintfpc.p" > "$work/log" 2>&1 || { cat "$work/log"; exit 1; }
    "$work/p4" ../p4/pcom.p4 "$work/r.p4" < readprd.pas > /dev/null
    printf 'ab\ncd\n' | cat "$work/r.p4" - > "$work/rd.p4"
    printf 'pint mended: '; printf 'xy\nzw\n' | "$work/pint" "$work/rd.p4" | tr -d '\000'
}

answer display display
answer eof eof
answer readln readln
if command -v "${FPC:-fpc}" > /dev/null; then
    answer pint pint
else
    echo "answers: Free Pascal not found, the mended pint not checked"
fi
