#!/bin/sh
# Run every answer and compare its output with the .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# About a minute: the suite runs on both machines, and the programs are traced.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
python3 build.py c > "$work/vm_more.c"
cc -std=c99 -O2 -Wall -Wextra -o "$work/vm" "$work/vm_more.c"
python3 build.py py > "$work/vm_more.py"
cp ../isa.py ../vmfile.py "$work/"
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

answer suite sh -c "cd .. && python3 conform.py '$work/vm' | tail -1 | sed 's|.*/vm:|vm_more.c:|'
    python3 conform.py python3 '$work/vm_more.py' | tail -1 | sed 's|.*/vm_more.py|vm_more.py|'"
answer count sh -c "for flags in '' -tail; do echo \"lambda_more.py \$flags\"
    python3 lambda_more.py \$flags count.lam > '$work/c.asm'
    python3 -c \"
import sys; sys.path.insert(0, '..')
import isa
isa.INSTRUCTIONS.append((32, 'TAILCALLI', ('n',))); isa.BY_NAME['TAILCALLI'] = (32, ('n',)); isa.BY_CODE[32] = ('TAILCALLI', ('n',))
import asm, vmfile
a = asm.Assembler('c'); _, code = a.assemble(open('$work/c.asm').read()); vmfile.write('$work/c.vm', code)\"
    '$work/vm' '$work/c.vm' || true; done"
answer measure python3 measure_more.py
