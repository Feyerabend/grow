#!/usr/bin/env python3
"""
Exercise 7.2: assemble as asm.py does, and also write program.sym beside
program.vm, a line "name address" for every label: what the file format
leaves out, kept beside it.

    usage: asm_sym.py program.asm program.vm
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import asm      # noqa: E402
import vmfile   # noqa: E402

source, target = sys.argv[1:]
a = asm.Assembler(source)
_, code = a.assemble(open(source).read())
if a.errors:
    sys.exit("\n".join(m for _, m in a.errors))
vmfile.write(target, code)
with open(os.path.splitext(target)[0] + ".sym", "w") as f:
    for name, address in sorted(a.labels.items(), key=lambda x: x[1]):
        f.write(f"{name} {address}\n")
