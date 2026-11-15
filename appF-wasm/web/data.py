#!/usr/bin/env python3
"""
Write web/data.js: what the page runs, as base64, so that the page needs
no server and opens straight from disk. Two modules, appendix F's machine
compiled to WebAssembly (build/appf.wasm) and chapter 23's machine in
WebAssembly 1.0 (programs/vm.wasm); and the five examples of chapter
23's playground, assembled, a trap among them.

    usage: python3 web/data.py build/appf.wasm > web/data.js
"""

import base64
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH23 = os.path.join(HERE, "..", "..", "ch23-wasm")


def b64(data):
    return base64.b64encode(data).decode()


def assemble(source):
    with tempfile.TemporaryDirectory() as work:
        asm, vm = os.path.join(work, "p.asm"), os.path.join(work, "p.vm")
        open(asm, "w").write(source)
        subprocess.run([sys.executable, os.path.join(CH23, "asm.py"), asm, vm], check=True)
        return open(vm, "rb").read()


def examples():
    """The playground's examples, from its app.js, in its order."""
    text = open(os.path.join(CH23, "web", "app.js")).read()
    block = text[text.index("const EXAMPLES = {"):]
    block = block[:block.index("\n};")]
    return re.findall(r'^    "([^"]+)": `(.*?)`', block, flags=re.M | re.S)


def main():
    appf = open(sys.argv[1], "rb").read()
    vm = open(os.path.join(HERE, "..", "programs", "vm.wasm"), "rb").read()
    programs = [(name, assemble(source)) for name, source in examples()]
    print("// Made by data.py from build/appf.wasm, programs/vm.wasm and chapter 23's")
    print("// programs. Not to be edited.")
    print(f'const APPF = "{b64(appf)}";')
    print(f'const VM = "{b64(vm)}";')
    print("const PROGRAMS = [")
    for name, data in programs:
        print(f'    ["{name}", "{b64(data)}"],')
    print("];")
    print("if (typeof module !== \"undefined\") module.exports = { APPF, VM, PROGRAMS };")


if __name__ == "__main__":
    main()
