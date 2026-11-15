#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# The times are not checked: python3 core.py times, and node slices.mjs
# program.vm, print them. The playground's breakpoints were tried by hand,
# in a browser: python3 build.py web folder, then serve the folder.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
(cd .. && make -s all)
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

answer core python3 core.py
answer web sh -c "python3 build.py web '$work/web' && node --check '$work/web/app.js' &&
    ls '$work/web' && grep -c 'breaks' '$work/web/app.js'"
