#!/bin/sh
# The page's machine, chip8.js, held to chip8.py: run by node, through
# run.js, it must print each sample's and answer's .out file, as
# chip8.py does; and on random programs both must print the same. And
# samples.js must be made from the .hex files as they are now.
set -e
cd "$(dirname "$0")"
python3 samples.py | cmp -s - samples.js || { echo "web/samples.js is out of date: python3 samples.py > samples.js"; exit 1; }
J="node run.js"
$J ../samples/answer.hex | diff -u ../samples/answer.out -
$J ../samples/collide.hex | diff -u ../samples/collide.out -
$J -m vip ../samples/quirks.hex | diff -u ../samples/quirks-vip.out -
$J -m chip48 ../samples/quirks.hex | diff -u ../samples/quirks-chip48.out -
$J -k 7 ../answers/keydigit.hex | diff -u ../answers/keydigit.out -
$J ../answers/keydigit.hex | diff -u ../answers/keydigit-nokey.out -
$J ../answers/overlap.hex | diff -u ../answers/overlap.out -
$J ../answers/multiply.hex | diff -u ../answers/multiply.out -
$J -n 31 ../answers/multiply.hex | diff -u ../answers/multiply-steps.out -
$J -m vip ../answers/shift.hex | diff -u ../answers/shift-vip.out -
$J -m chip48 ../answers/shift.hex | diff -u ../answers/shift-chip48.out -
out=$(python3 fuzz.py 200 1) || { echo "$out"; exit 1; }
echo "$out" | head -1
