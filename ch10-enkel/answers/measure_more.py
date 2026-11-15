#!/usr/bin/env python3
"""
Exercises 10.5 and 10.6, measured as measure/cost.py measures: every sample
compiled by enkel.py, run on vm.py, its instructions counted.

10.5: a check of a computed index in six instructions instead of ten. XOR with
-2147483648 flips the sign bit, and turns a signed comparison into an unsigned
one: 0 <= i < size, as signed numbers, is i < size as unsigned numbers. So

    DUP  PUSH -2147483648  XOR  PUSH size-2147483648  LT  JZ bad

10.6: the machine gets GT, NE, LE and GE (codes 27 to 30, in this copy only),
and the compiler uses them, so that every comparison is one instruction.

    usage: python3 measure_more.py       (run in code/ch10-enkel/answers)
"""

import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CH10 = os.path.join(HERE, "..")
sys.path.insert(0, CH10)
sys.path.insert(0, os.path.join(CH10, "measure"))
import asm                                      # noqa: E402
import cost                                     # noqa: E402
import enkel                                    # noqa: E402
import isa                                      # noqa: E402
import vm                                       # noqa: E402
import vmfile                                   # noqa: E402

NEW = {"GT": (27, lambda a, b: a > b), "NE": (28, lambda a, b: a != b),
       "LE": (29, lambda a, b: a <= b), "GE": (30, lambda a, b: a >= b)}


class Short(cost.Tagging):
    """measure/cost.py's checked generator, with the six-instruction check."""

    def address(self, element):
        if not self.checked or type(element.index) is enkel.Number:
            return enkel.Generator.address(self, element)
        base, size = element.meaning[1], element.meaning[2]
        self.emit(f"PUSH {base}")
        self.value(element.index)
        self.bad_used = True
        for instruction in ["DUP", "PUSH -2147483648", "XOR",
                            f"PUSH {size - 2147483648}", "LT", "JZ bad"]:
            self.tagged("check", instruction)
        self.emit("ADD")


class Machine(cost.Counting):
    def step(self):
        op = self.code[self.pc] if 0 <= self.pc < len(self.code) else None
        for name, (code, f) in NEW.items():
            if op == code:
                self.start = self.pc
                self.counts[self.pc] += 1
                self.pc += 1
                self.binary(lambda a, b, f=f: int(f(a, b)))
                return
        super().step()


def run(path, generator, checked=False):
    text = open(path).read()
    program = enkel.Parser(enkel.scan(text)).program()
    enkel.Resolver(program).resolve()
    g = generator(text.splitlines(), checked)
    a = asm.Assembler(path)
    _, code = a.assemble(g.program(program))
    assert not a.errors, a.errors
    m = Machine(code)
    assert vm.run(m, False) == 0, path
    return sum(m.counts.values()), m.out.getvalue()


def main():
    samples = sorted(glob.glob(os.path.join(CH10, "samples", "*.p")))
    print("10.5: computed indexes checked, instructions run")
    print(f"{'sample':22} {'unchecked':>10} {'ten':>8} {'six':>8}")
    totals = [0, 0, 0]
    for path in samples:
        name = os.path.basename(path)[:-2]
        n0, out0 = run(path, cost.Tagging)
        n10, out10 = run(path, cost.Tagging, True)
        n6, out6 = run(path, Short, True)
        assert out0 == out10 == out6 == open(path[:-2] + ".out", "rb").read(), path
        if n10 != n0:
            print(f"{name:22} {n0:10} {n10:8} {n6:8}")
        totals = [t + n for t, n in zip(totals, (n0, n10, n6))]
    print(f"{'all thirteen':22} {totals[0]:10} {totals[1]:8} {totals[2]:8}"
          f"   checks add {100 * (totals[1] - totals[0]) / totals[0]:.1f}% and "
          f"{100 * (totals[2] - totals[0]) / totals[0]:.1f}%")

    print("\n10.6: with GT, NE, LE and GE, instructions run")
    before = run_all(samples)
    for name, (code, _) in NEW.items():
        isa.INSTRUCTIONS.append((code, name, ()))
        isa.BY_NAME[name] = (code, ())
        isa.BY_CODE[code] = (name, ())
    enkel.COMPARISONS.update({"#": ["NE"], ">": ["GT"], "<=": ["LE"], ">=": ["GE"]})
    after = run_all(samples)
    print(f"{'sample':22} {'before':>8} {'after':>8} {'fewer':>7}")
    for name in before:
        if before[name] != after[name]:
            b, a = before[name], after[name]
            print(f"{name:22} {b:8} {a:8} {100 * (b - a) / b:6.1f}%")
    b, a = sum(before.values()), sum(after.values())
    print(f"{'all thirteen':22} {b:8} {a:8} {100 * (b - a) / b:6.1f}%")


def run_all(samples):
    result = {}
    for path in samples:
        n, out = run(path, cost.Tagging)
        assert out == open(path[:-2] + ".out", "rb").read(), path
        result[os.path.basename(path)[:-2]] = n
    return result


if __name__ == "__main__":
    main()
