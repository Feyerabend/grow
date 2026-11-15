#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# The answers that change the machine are patches, applied here to a copy
# of emit.py, cek.h, tree.c and cek.c:
#   flat.patch     a closure keeps only the cells its body uses (2)
#   frames.patch   each call's variables in an array, a frame (4)
# Each copy, built to check every variable and to collect before every
# step, runs all of Lark's tests and samples, which must print what Lark's
# own machine printed; then the benchmarks, with LARK_STATS. floatfuzz.py
# (6) runs if Hypothesis is installed (make venv). hint.sh (5) times, and
# is run by hand.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
CC=${CC:-cc}
PYTHON=${PYTHON:-python3}
F="-std=c11 -O2 -w"
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

build() {       # build name patch: emit.py and the machine, changed
    d="$work/$1"
    mkdir "$d"
    cp ../emit.py ../cek.h ../tree.c ../tree.h ../cek.c ../main.c "$d"
    ln -s "$(cd .. && pwd)/lark" "$d/lark"
    (cd "$d" && patch -s < "$OLDPWD/$2")
    (cd "$d" && $CC $F -o machine cek.c tree.c main.c &&
        $CC $F -DLARK_CHECK_DEPTH -DLARK_COLLECT_ALWAYS -o lark-checked cek.c tree.c main.c)
}

# All of Lark's programs, as make check runs them, then the benchmarks.
run() {
    d="$work/$1"
    n=0
    for f in ../lark/tests/[0-9][0-9]_*.lark ../lark/tests/09_modules/main.lark \
             ../lark/tests/errors/*.lark ../lark/samples/*.lark; do
        name=$(echo "$f" | sed 's|^\.\./lark/||; s|\.lark$||; s|/|_|g')
        { $PYTHON "$d/emit.py" "$f" > "$d/p.tree" && "$d/lark-checked" "$d/p.tree"; echo "status $?"; } \
            > "$d/p.out" 2>&1
        cmp -s "../expected/$name.out" "$d/p.out" || { echo "differs: $name"; cat "$d/p.out"; return 1; }
        n=$((n + 1))
    done
    echo "$n programs print what Lark's machine printed"
    for b in fib loop sort; do
        $PYTHON "$d/emit.py" "../bench/$b.lark" > "$d/$b.tree"
        LARK_STATS=1 "$d/machine" "$d/$b.tree" > "$d/$b.out" 2> "$d/$b.stats"
        cmp -s "../bench/$b.out" "$d/$b.out" || { echo "differs: $b"; return 1; }
        echo "$b: $(grep collections "$d/$b.stats")"
    done
}

build flat flat.patch
build frames frames.patch
mkdir "$work/as-it-is"
ln -s "$(cd .. && pwd)/lark" "$work/as-it-is/lark"
cp ../emit.py "$work/as-it-is"
(cd .. && $CC $F -o "$work/as-it-is/machine" cek.c tree.c main.c &&
    $CC $F -DLARK_CHECK_DEPTH -DLARK_COLLECT_ALWAYS -o "$work/as-it-is/lark-checked" cek.c tree.c main.c)

answer as-it-is run as-it-is
answer flat run flat
answer frames run frames

# 6. Floats, if Hypothesis is there: with the four differences explained
#    passed over, the machines agree.
FUZZPY=$PYTHON
[ -x ../build/venv/bin/python ] && FUZZPY=../build/venv/bin/python
if $FUZZPY -c 'import hypothesis' 2> /dev/null; then
    (cd .. && make -s build/lark > /dev/null)
    KNOWN=all $FUZZPY floatfuzz.py 200 | tail -1
fi
