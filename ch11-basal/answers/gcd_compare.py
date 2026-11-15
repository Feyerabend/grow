#!/usr/bin/env python3
"""
Exercise 11.4: gcd in enkel/0 (chapter 10's samples/gcd.p) and in basal/0
(samples/gcd.bas), compiled, assembled and run on chapter 10's vm.py,
counting instructions: how many each program has, how many it runs, and of
which kinds.

    usage: python3 gcd_compare.py
"""

import collections
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CH10 = os.path.join(HERE, "..", "..", "ch10-enkel")
sys.path.insert(0, os.path.join(HERE, ".."))
import basal                                    # noqa: E402
import asm                                      # noqa: E402


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


enkel = load("enkel", os.path.join(CH10, "enkel.py"))
vm = load("vm", os.path.join(CH10, "vm.py"))


class Counting(vm.Machine):
    def __init__(self, code):
        super().__init__(code)
        self.counts = collections.Counter()
        self.out = io.BytesIO()

    def step(self):
        if 0 <= self.pc < len(self.code):
            self.counts[vm.isa.BY_CODE.get(self.code[self.pc], ("?",))[0]] += 1
        super().step()


def compile_enkel(text):
    program = enkel.Parser(enkel.scan(text)).program()
    enkel.Resolver(program).resolve()
    return enkel.Generator(text.splitlines()).program(program)


def measure(name, assembly):
    a = asm.Assembler(name)
    _, code = a.assemble(assembly)
    m = Counting(code)
    assert vm.run(m, False) == 0
    lines = [l for l in assembly.splitlines() if l.startswith("        ")]
    kinds = m.counts
    memory = kinds["LOADM"] + kinds["STOREM"]
    frame = kinds["LOAD"] + kinds["STORE"]
    print(f"{name:8} prints {m.out.getvalue().decode().strip():>3}; {len(lines):3} instructions,"
          f" {sum(kinds.values()):3} run: {memory:3} LOADM/STOREM, {frame:3} LOAD/STORE,"
          f" {kinds['PUSH']:3} PUSH, {kinds['CALL'] + kinds['RET']} CALL/RET")


measure("enkel/0", compile_enkel(open(os.path.join(CH10, "samples", "gcd.p")).read()))
measure("basal/0", basal.Translator(basal.desugar(basal.scan(
    open(os.path.join(HERE, "..", "samples", "gcd.bas")).read()))).program())
