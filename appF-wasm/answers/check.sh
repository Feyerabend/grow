#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# The answers that change the machine are patches, applied here to a copy:
#   predecode.patch    each function decoded once, after validation (1)
#   signext.patch      the five sign-extension instructions (4)
# modules/ holds the binaries made from the .wat and .wast files by WABT
# (wat2wasm --no-check twobranches.wat; wast2json --disable-sign-extension
# seventh.wast; wast2json signext.wast), so that no WABT is needed here.
# If the specification's tests have been made (make suite), each
# changed machine runs them too.
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

build() {       # build name [patch [sed]]: the machine, changed or not
    mkdir "$work/$1"
    cp ../wasm.c ../wasm.h ../spec.c ../spec.h ../main.c ../program.c "$work/$1"
    [ -z "$2" ] || (cd "$work/$1" && patch -s < "$OLDPWD/$2")
    [ -z "$3" ] || sed -i.orig "$3" "$work/$1/wasm.c"
    (cd "$work/$1" && $CC -std=c99 -O2 -w -D_POSIX_C_SOURCE=200809L -o wasm \
        wasm.c spec.c main.c program.c -lm)
}
build plain
build predecode predecode.patch
build signext signext.patch
build seventh "" 's/case 0x6A: return BIN32(A32 + B32);/case 0x6A: return BIN32(A32 + B32 + (A32 == 0x12345678));/'

spec() {        # the specification's tests, if made, on machine $1
    if ls ../build/suite/*.json > /dev/null 2>&1; then
        "$work/$1/wasm" -s ../build/suite/*.json > "$work/spec" 2>&1 || true
        grep -q " 0 failed" "$work/spec" || { cat "$work/spec"; exit 1; }
        echo "answers: $1 passes the specification's tests"
    fi
}

# 1. Decoded once: the programs print the same, and chapter 23's suite
#    passes with the machine running it.
predecode() {
    for p in ../programs/*.wasm; do
        n=$(basename "$p" .wasm)
        [ -f "../programs/$n.out" ] || continue
        { "$work/predecode/wasm" "$p"; echo "status $?"; } > "$work/$n.out" 2>&1
        cmp "../programs/$n.out" "$work/$n.out" || return 1
    done
    echo "the programs print the same"
    (cd ../../ch23-wasm && python3 conform.py "$work/predecode/wasm" -m ../appF-wasm/programs/vm.wasm) |
        sed 's|^.*/wasm -m|wasm -m|'
}

# 2. Two branches to one block, carrying an i32 and an i64.
twobranches() {
    "$work/plain/wasm" modules/twobranches.wasm 2>&1 | sed 's|^.*/twobranches|twobranches|'
}

# 3. The seventh breakage, and a test that catches it.
seventh() {
    printf 'as it is:  '; "$work/plain/wasm" -s modules/seventh.json 2>&1 | tail -1
    printf 'broken:    '; "$work/seventh/wasm" -s modules/seventh.json 2>&1 | tail -1
}

# 4. Sign extension: the five instructions, on the machine with them and
#    on the machine as it is, which must refuse them.
signext() {
    printf 'with them:  '; "$work/signext/wasm" -s modules/signext.json 2>&1 | tail -1
    printf 'without:    '; "$work/plain/wasm" -s modules/signext.json 2>&1 | tail -1
}

answer predecode predecode
answer twobranches twobranches
answer seventh seventh
answer signext signext
spec predecode
spec signext
spec seventh
