#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# About a minute: onebyone.py compiles and runs fuzz.py's 500 expressions
# under six wrong parsers.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
(cd .. && make vm > /dev/null)
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

run() {             # compile with expr_more.py, assemble, run
    python3 expr_more.py "$1" > "$work/p.asm" && python3 ../asm.py "$work/p.asm" "$work/p.vm" &&
        ../vm "$work/p.vm"
}
answer semicolon-old python3 ../expr.py semicolon.expr
answer semicolon-new python3 expr_more.py semicolon.expr
answer power run power.expr
answer nested python3 expr_more.py nested.expr
answer minus python3 expr_more.py minus.expr
answer minus255 run minus255.expr
answer twonumbers sh -c "python3 ../expr.py -tokens twonumbers.expr; python3 ../expr.py twonumbers.expr"
answer shortest python3 shortest.py
answer onebyone python3 onebyone.py
