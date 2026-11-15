#!/usr/bin/env python3
"""
Compile a basal/0 program with basal_more.py, assemble it with READ known to
the assembler, and run it on the machine that build_vm.py makes, with the
given text as standard input.

    usage: run.py program.bas vm_read [input text]
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import isa                                      # noqa: E402

isa.INSTRUCTIONS.append((27, "READ", ()))
isa.BY_NAME["READ"] = (27, ())
isa.BY_CODE[27] = ("READ", ())
import asm                                      # noqa: E402
import vmfile                                   # noqa: E402

program, machine = sys.argv[1:3]
stdin = sys.argv[3].replace("\\n", "\n") if len(sys.argv) > 3 else ""
r = subprocess.run([sys.executable, os.path.join(HERE, "basal_more.py"), program],
                   capture_output=True, text=True)
if r.returncode:
    sys.stdout.write(r.stderr)
    sys.exit(0)
a = asm.Assembler(program)
_, code = a.assemble(r.stdout)
with tempfile.TemporaryDirectory() as folder:
    path = os.path.join(folder, "p.vm")
    vmfile.write(path, code)
    r = subprocess.run([machine, path], input=stdin, capture_output=True, text=True)
sys.stdout.write(r.stdout + r.stderr + f"status {r.returncode}\n")
