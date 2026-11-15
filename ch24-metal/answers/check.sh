#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# Several minutes: the suite runs in simulation on five variants.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
(cd .. && make -s sim)
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

# The tests of versions 3 and 4, as the chapter's Makefile finds them; with
# the heap of exercise 1, only CALLI's and garbage, which needs a collector.
later=$(cd .. && grep -l -E '^\s*[A-Za-z_]*:?\s*(NEW|GETF|SETF|LEN|CALLI)\b|\.word (2[7-9]|3[01])' \
    suite/*.asm | xargs -n1 basename | sed 's/\.asm$//' | paste -sd, -)
calli=$(cd .. && grep -l -E '^\s*[A-Za-z_]*:?\s*CALLI\b|\.word 31' \
    suite/*.asm | xargs -n1 basename | sed 's/\.asm$//' | paste -sd, -),garbage
for v in heap pipe div trace pair; do python3 build.py $v "$work/$v"; done
answer suite sh -c "cd .. && for v in heap pipe div trace pair; do
    if [ \$v = heap ]; then known='$calli'; else known='$later'; fi
    echo \"\$v: \$(python3 conform.py --known \$known python3 answers/vrun_more.py '$work/'\$v |
        grep passed | sed 's/.*: //')\"
    done"
answer cycles python3 cycles.py
answer compare python3 compare.py
# Exercise 3's sizes, if Yosys is installed: the dividers beside an adder
# and a multiplier (size.py cpu, the whole CPU, takes minutes and is not run).
if command -v yosys > /dev/null; then
    answer size python3 size.py units
else
    echo "answers: size not checked: Yosys is not installed"
fi
