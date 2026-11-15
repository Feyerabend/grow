#!/usr/bin/env python3
"""
What do the machine's missing instructions, rval, and unchecked arrays cost?

Every sample is compiled by enkel.py and run on vm.py, counting how many times
each instruction is executed. Some instructions are tagged as they are generated:

    compare     the extra instructions that build >, #, <= and >= from LT and EQ,
                and the PUSH 0, EQ that turns do ... while's condition round
    unused      the value every RET carries and every call DROPs: enkel/0 does
                not use it, since results go through rval
    rval        storing a result in rval and reading it back: PUSH 0, STOREM
                in return, PUSH 0, LOADM where rval is read

Then the same samples with every computed array index checked before it is
used, as exercise 1 asks: the index must be at least 0 and less than the size.
The check is ten instructions, since the machine has only LT and EQ:

    DUP  PUSH size  LT  JZ bad                  index < size, or go to bad
    DUP  PUSH 0  LT  PUSH 0  EQ  JZ bad         not (index < 0), or go to bad

and bad: is PUSH -1, LOADM, which traps. Each sample must still print what
it printed before.

    usage: python3 measure/cost.py      (run in code/ch10-enkel)
"""

import collections
import glob
import io
import os
import sys

sys.path.insert(0, os.getcwd())
import enkel                                     # noqa: E402
import isa                                       # noqa: E402
import vm                                        # noqa: E402
import asm as assembler                          # noqa: E402,F401


class Tagging(enkel.Generator):

    def __init__(self, lines, checked=False):
        super().__init__(lines)
        self.tags = {}
        self.checked = checked
        self.bad_used = False

    def tagged(self, tag, instruction):
        self.tags[len(self.out)] = tag
        self.emit(instruction)

    def statement(self, node):
        kind = type(node)
        if kind is enkel.Call:
            self.note(node.token)
            for arg in node.args:
                self.value(arg)
            self.emit(f"CALL p_{node.procedure.name.text} {len(node.args)}")
            self.tagged("unused", "DROP")
        elif kind is enkel.DoWhile:
            self.note(node.token)
            top = self.new_label()
            self.label(top)
            self.statement(node.body)
            self.value(node.condition)
            self.tagged("compare", "PUSH 0")
            self.tagged("compare", "EQ")
            self.emit(f"JZ {top}")
        elif kind is enkel.Return:
            self.note(node.token)
            if node.value:
                self.tagged("rval", f"PUSH {enkel.RVAL}")
                self.value(node.value)
                self.tagged("rval", "STOREM")
            if node.in_procedure:
                self.tagged("unused", "PUSH 0")
                self.emit("RET")
            else:
                self.emit("HALT")
        else:
            super().statement(node)

    def program(self, p):
        text = super().program(p)
        # The PUSH 0 before each procedure's last RET is the unused value too.
        for i, line in enumerate(self.out):
            if line.strip() == "RET" and self.out[i - 1].strip() == "PUSH 0":
                self.tags.setdefault(i - 1, "unused")
        if self.bad_used:
            self.out += ["", "bad:", "        PUSH -1", "        LOADM"]
            text = "\n".join(self.out) + "\n"
        return text

    def value(self, node):
        kind = type(node)
        if kind is enkel.Compare:
            self.value(node.left)
            self.value(node.right)
            steps = enkel.COMPARISONS[node.op]
            essential = steps.index("LT") if "LT" in steps else 0
            for k, instruction in enumerate(steps):
                if k == essential:
                    self.emit(instruction)
                else:
                    self.tagged("compare", instruction)
        elif kind is enkel.Name and node.meaning == ("global", enkel.RVAL):
            self.tagged("rval", f"PUSH {enkel.RVAL}")
            self.tagged("rval", "LOADM")
        else:
            super().value(node)

    def address(self, element):
        if not self.checked or type(element.index) is enkel.Number:
            return super().address(element)
        base, size = element.meaning[1], element.meaning[2]
        self.emit(f"PUSH {base}")
        self.value(element.index)
        self.bad_used = True
        for instruction in ["DUP", f"PUSH {size}", "LT", "JZ bad",
                            "DUP", "PUSH 0", "LT", "PUSH 0", "EQ", "JZ bad"]:
            self.tagged("check", instruction)
        self.emit("ADD")


def addresses(lines):
    """The program address of each instruction line, as asm.py lays them out."""
    at, where = 0, {}
    for i, line in enumerate(lines):
        if not line.startswith("        "):
            continue
        name = line.split()[0]
        where[i] = at
        at += 1 + len(isa.BY_NAME[name][1])
    return where


class Counting(vm.Machine):

    def __init__(self, code):
        super().__init__(code)
        self.counts = collections.Counter()
        self.out = io.BytesIO()

    def step(self):
        self.counts[self.pc] += 1
        super().step()


def run(path, checked):
    text = open(path).read()
    program = enkel.Parser(enkel.scan(text)).program()
    enkel.Resolver(program).resolve()
    g = Tagging(text.splitlines(), checked)
    source = g.program(program)
    tmp_asm, tmp_vm = "_cost.asm", "_cost.vm"
    with open(tmp_asm, "w") as f:
        f.write(source)
    os.system(f"{sys.executable} asm.py {tmp_asm} {tmp_vm}")
    code = vm.vmfile.read(tmp_vm)
    os.remove(tmp_asm)
    os.remove(tmp_vm)
    where = addresses(g.out)
    assert max(where.values()) < len(code)
    m = Counting(code)
    assert vm.run(m, False) == 0, path
    by_tag = collections.Counter()
    for i, tag in g.tags.items():
        by_tag[tag] += m.counts[where[i]]
    static = len(where)
    return sum(m.counts.values()), by_tag, m.out.getvalue(), static


def main():
    rows, totals = [], collections.Counter()
    print(f"{'sample':22} {'executed':>9} {'compare':>8} {'unused':>7} {'rval':>6}"
          f" {'checked':>9} {'more':>6}")
    for path in sorted(glob.glob("samples/*.p")):
        n, tags, out, _ = run(path, False)
        n2, tags2, out2, _ = run(path, True)
        assert out == out2, path
        assert open(path[:-2] + ".out", "rb").read() == out, path
        name = os.path.basename(path)[:-2]
        print(f"{name:22} {n:9} {tags['compare']:8} {tags['unused']:7} {tags['rval']:6}"
              f" {n2:9} {100 * (n2 - n) / n:5.1f}%")
        totals.update(executed=n, compare=tags["compare"], unused=tags["unused"],
                      rval=tags["rval"], checked=n2)
    t = totals
    print(f"{'all':22} {t['executed']:9} {t['compare']:8} {t['unused']:7} {t['rval']:6}"
          f" {t['checked']:9} {100 * (t['checked'] - t['executed']) / t['executed']:5.1f}%")
    for k in ("compare", "unused", "rval"):
        print(f"  {k}: {100 * t[k] / t['executed']:.1f}% of all executed instructions")


if __name__ == "__main__":
    main()
