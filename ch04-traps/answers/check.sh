#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# The runs without a change (add, div) show what the M1 does with C's
# undefined overflow, built with -O1; another computer may differ.
set -e
cd "$(dirname "$0")"
while read -r name command; do
    [ -n "$name" ] || continue
    if [ "$1" = expect ]; then
        python3 $command > "$name.out"
    else
        python3 $command | diff -u "$name.out" -
    fi
done <<'EOF'
add run.py add.txt
add-overflow run.py add.txt overflow
div run.py div.txt
div-divide run.py div.txt divide
steps steps.py
EOF
