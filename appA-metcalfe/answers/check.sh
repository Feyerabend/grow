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

M="python3 ../metcalfe.py"
# 2: the wrong sentence, traced
answer wrong sh -c "echo 'THE BOY A TREE SEES' | $M -w -t ../samples/sentence.syn"
# 3: the adjective list, three ways
for g in short-first long-first loop; do
    answer adjectives-$g sh -c "$M -w adjectives-$g.syn < adjectives.in"
done
# 4: operators moved behind their operands by the editor
answer postfix sh -c "$M postfix.syn < postfix.in"
echo "appendix A answers: ok"
