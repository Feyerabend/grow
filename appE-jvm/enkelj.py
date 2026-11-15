#!/usr/bin/env python3
"""enkel/0 to class files: chapter 10's language on the JVM.

The scanner, parser and resolver are chapter 10's own, from
../ch10-enkel/enkel.py; only the last stage is new. Where chapter 10
generated assembly for the book's machine, this writes a class file:

    a global variable, and rval      a static int field
    an array                         a static int[] field, made in <clinit>
    a procedure                      a static method, (II...)V
    the main program                 main(String[])
    print e                          System.out.println(int)
    emit e                           System.out.print(char)

It writes the bytecode, works out max_stack and max_locals, and writes the
StackMapTable itself. That is easy for enkel/0, and the reason is worth
seeing: a statement leaves nothing on the operand stack, so at every place
where paths meet the stack is empty, and every local is an int, set to 0
when the procedure begins. So every frame is the same one.

    usage: enkelj.py program.p [folder]     writes folder/Program.class
           enkelj.py -name program          prints Program, the class's name
"""

import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ch10-enkel"))
sys.path.insert(0, HERE)

import enkel                                    # noqa: E402
from enkel import (Assign, Binary, Block, Call, Compare, DoWhile, Element,  # noqa: E402
                   Emit, Empty, If, Name, Negate, Number, Print, Return, While)
from classfile import Pool                      # noqa: E402

OUT = ("java/lang/System", "out", "Ljava/io/PrintStream;")
ARITHMETIC = {"+": 0x60, "-": 0x64, "*": 0x68, "/": 0x6c, "%": 0x70,
              "and": 0x7e, "or": 0x80, "xor": 0x82}
# if_icmp<cond> for each comparison, and the one for its opposite.
JUMP_IF = {"=": 0x9f, "#": 0xa0, "<": 0xa1, ">=": 0xa2, ">": 0xa3, "<=": 0xa4}
OPPOSITE = {"=": "#", "#": "=", "<": ">=", ">=": "<", ">": "<=", "<=": ">"}
GOTO, IFEQ, IFNE = 0xa7, 0x99, 0x9a
RETURN, GETSTATIC, PUTSTATIC = 0xb1, 0xb2, 0xb3
INVOKEVIRTUAL, INVOKESTATIC = 0xb6, 0xb8
ILOAD, ISTORE, IALOAD, IASTORE = 0x15, 0x36, 0x2e, 0x4f


class Code:
    """The code of one method being written: its bytes, the depth of its
    operand stack, its labels and the frames they need."""

    def __init__(self, pool, cls, nlocals):
        self.pool, self.cls = pool, cls
        self.bytes = bytearray()
        self.depth = self.max_depth = 0
        self.labels, self.fixups = {}, []
        self.frames = set()          # offsets where a stack map frame goes
        self.after_jump = False      # the last instruction does not go on
        self.lines = []
        self.nlocals = nlocals

    def op(self, *data, stack=0):
        if self.after_jump:          # code that follows a return or goto
            self.frames.add(len(self.bytes))
            self.after_jump = False
        self.bytes += bytes(data)
        self.depth += stack
        self.max_depth = max(self.max_depth, self.depth)

    def u2(self, op, index, stack):
        self.op(op, index >> 8, index & 255, stack=stack)

    def label(self):
        return object()

    def place(self, label):
        self.labels[label] = len(self.bytes)
        self.frames.add(len(self.bytes))
        self.after_jump = False

    def jump(self, op, label, stack):
        self.fixups.append((len(self.bytes), label))
        self.op(op, 0, 0, stack=stack)
        if op == GOTO:
            self.after_jump = True

    def finish(self):
        for at, label in self.fixups:
            offset = self.labels[label] - at
            if not -32768 <= offset <= 32767:
                raise SystemExit("enkelj: a procedure too long for a 16-bit branch")
            struct.pack_into(">h", self.bytes, at + 1, offset)

    def push(self, n):
        if -1 <= n <= 5:
            self.op(0x03 + n, stack=1)                  # iconst_<n>
        elif -128 <= n <= 127:
            self.op(0x10, n & 255, stack=1)             # bipush
        elif -32768 <= n <= 32767:
            self.op(0x11, (n >> 8) & 255, n & 255, stack=1)   # sipush
        else:
            i = self.pool.integer(n)
            if i < 256:
                self.op(0x12, i, stack=1)               # ldc
            else:
                self.u2(0x13, i, 1)                     # ldc_w

    def local(self, op, k, stack):
        if k <= 3:
            self.op((0x1a if op == ILOAD else 0x3b) + k, stack=stack)
        elif k <= 255:
            self.op(op, k, stack=stack)
        else:
            self.op(0xc4, op, k >> 8, k & 255, stack=stack)   # wide

    def field(self, op, name, descriptor):
        self.u2(op, self.pool.field(self.cls, name, descriptor), 1 if op == GETSTATIC else -1)

    def stack_map(self):
        """The StackMapTable: every frame is the method's first, with
        each local an int and the stack empty, once they are set."""
        offsets = sorted(o for o in self.frames if o < len(self.bytes))
        out, last = bytearray(), -1
        for i, offset in enumerate(offsets):
            delta = offset if last < 0 else offset - last - 1
            last = offset
            k = self.nlocals
            if i == 0 and k <= 3 and k:         # the locals appear
                out += struct.pack(">BH", 251 + k, delta) + b"\x01" * k
            elif i == 0 and k:                  # full_frame: all of them
                n = self.nparams + k
                out += struct.pack(">BHH", 255, delta, n)
                out += b"\x01" * n + b"\x00\x00"
            elif delta < 64:
                out += bytes([delta])           # same_frame
            else:                               # same_frame_extended
                out += struct.pack(">BH", 251, delta)
        return len(offsets), bytes(out)


class Compiler:

    def __init__(self, program, cls, source):
        self.program, self.cls, self.source = program, cls, source
        self.pool = Pool()

    def method(self, name, descriptor, body, nparams, nlocals, access=0x0008):
        code = Code(self.pool, self.cls, nlocals)
        code.nparams = nparams
        self.code = code
        for k in range(nparams, nparams + nlocals):     # every local starts as 0
            code.push(0)
            code.local(ISTORE, k, -1)
        body(code)
        if not code.after_jump:
            code.op(RETURN)
        code.finish()
        attributes = []
        count, table = code.stack_map()
        if count:
            attributes.append(struct.pack(">HIH", self.pool.utf8("StackMapTable"),
                                          2 + len(table), count) + table)
        if code.lines:
            lines = b"".join(struct.pack(">HH", pc, line) for pc, line in code.lines)
            attributes.append(struct.pack(">HIH", self.pool.utf8("LineNumberTable"),
                                          2 + len(lines), len(code.lines)) + lines)
        max_locals = max(nparams + nlocals, 1 if name == "main" and descriptor.startswith("([") else 0)
        body_bytes = (struct.pack(">HHI", code.max_depth, max_locals, len(code.bytes)) +
                      bytes(code.bytes) + struct.pack(">HH", 0, len(attributes)) +
                      b"".join(attributes))
        return (struct.pack(">HHHH", access, self.pool.utf8(name), self.pool.utf8(descriptor), 1) +
                struct.pack(">HI", self.pool.utf8("Code"), len(body_bytes)) + body_bytes)

    def class_file(self):
        p = self.program
        fields = [("rval", "I")] + [(t.text, "I") for t in p.globals] + \
                 [(t.text, "[I") for t, _ in p.arrays]
        methods = []
        if p.arrays:
            def clinit(code):
                for name, size in p.arrays:
                    code.push(size)
                    code.op(0xbc, 10)                   # newarray int
                    code.field(PUTSTATIC, name.text, "[I")
            methods.append(self.method("<clinit>", "()V", clinit, 0, 0))
        methods.append(self.method("main", "([Ljava/lang/String;)V",
                                   lambda code: self.statement(p.body), 1, 0, 0x0009))
        for proc in p.procedures:
            methods.append(self.method(proc.name.text, "(" + "I" * len(proc.params) + ")V",
                                       lambda code, proc=proc: self.statement(proc.body),
                                       len(proc.params), len(proc.locals)))
        this, super_ = self.pool.klass(self.cls), self.pool.klass("java/lang/Object")
        source = struct.pack(">HIH", self.pool.utf8("SourceFile"), 2, self.pool.utf8(self.source))
        field_bytes = b"".join(struct.pack(">HHHH", 0x0008, self.pool.utf8(n), self.pool.utf8(d), 0)
                               for n, d in fields)
        return (struct.pack(">IHH", 0xCAFEBABE, 0, 65) + self.pool.bytes() +
                struct.pack(">HHHH", 0x0021, this, super_, 0) +
                struct.pack(">H", len(fields)) + field_bytes +
                struct.pack(">H", len(methods)) + b"".join(methods) +
                struct.pack(">H", 1) + source)

    # Statements: each leaves the operand stack as it found it, empty.

    def statement(self, node):
        c = self.code
        kind = type(node)
        if kind not in (Block, Empty):
            if not c.lines or c.lines[-1][1] != node.token.line:
                c.lines.append((len(c.bytes), node.token.line))
        if kind is Assign:
            t = node.target
            if t.meaning[0] == "local":
                self.value(node.value)
                c.local(ISTORE, t.meaning[1], -1)
            elif t.meaning[0] == "global":
                self.value(node.value)
                c.field(PUTSTATIC, t.name, "I")
            else:
                c.field(GETSTATIC, t.name, "[I")
                self.value(t.index)
                self.value(node.value)
                c.op(IASTORE, stack=-3)
        elif kind is Call:
            for arg in node.args:
                self.value(arg)
            n = len(node.args)
            c.u2(INVOKESTATIC, self.pool.method(self.cls, node.name.text, "(" + "I" * n + ")V"), -n)
        elif kind is Block:
            for s in node.statements:
                self.statement(s)
        elif kind is If:
            otherwise, done = c.label(), c.label()
            self.branch_unless(node.condition, otherwise)
            self.statement(node.then)
            if node.otherwise:
                c.jump(GOTO, done, 0)
                c.place(otherwise)
                self.statement(node.otherwise)
                c.place(done)
            else:
                c.place(otherwise)
        elif kind is While:
            top, done = c.label(), c.label()
            c.place(top)
            self.branch_unless(node.condition, done)
            self.statement(node.body)
            c.jump(GOTO, top, 0)
            c.place(done)
        elif kind is DoWhile:
            top = c.label()
            c.place(top)
            self.statement(node.body)
            self.branch_if(node.condition, top)
        elif kind is Return:
            if node.value:                  # only a return with a value sets rval
                self.value(node.value)
                c.field(PUTSTATIC, "rval", "I")
            c.op(RETURN)
            c.after_jump = True
        elif kind in (Print, Emit):
            c.u2(GETSTATIC, self.pool.field(*OUT), 1)
            self.value(node.value)
            if kind is Print:
                c.u2(INVOKEVIRTUAL, self.pool.method("java/io/PrintStream", "println", "(I)V"), -2)
            else:
                c.op(0x92)                  # i2c
                c.u2(INVOKEVIRTUAL, self.pool.method("java/io/PrintStream", "print", "(C)V"), -2)

    def branch_unless(self, condition, label):
        if type(condition) is Compare:
            self.value(condition.left)
            self.value(condition.right)
            self.code.jump(JUMP_IF[OPPOSITE[condition.op]], label, -2)
        else:
            self.value(condition)
            self.code.jump(IFEQ, label, -1)

    def branch_if(self, condition, label):
        if type(condition) is Compare:
            self.value(condition.left)
            self.value(condition.right)
            self.code.jump(JUMP_IF[condition.op], label, -2)
        else:
            self.value(condition)
            self.code.jump(IFNE, label, -1)

    # Expressions: each leaves one int on the stack.

    def value(self, node):
        c = self.code
        kind = type(node)
        if kind is Number:
            c.push(node.value)
        elif kind is Name:
            what = node.meaning[0]
            if what == "const":
                c.push(node.meaning[1])
            elif what == "local":
                c.local(ILOAD, node.meaning[1], 1)
            else:
                c.field(GETSTATIC, node.name, "I")
        elif kind is Element:
            c.field(GETSTATIC, node.name, "[I")
            self.value(node.index)
            c.op(IALOAD, stack=-1)
        elif kind is Negate:
            self.value(node.operand)
            c.op(0x74)                      # ineg
        elif kind is Binary:
            self.value(node.left)
            self.value(node.right)
            c.op(ARITHMETIC[node.op], stack=-1)
        elif kind is Compare:               # the grammar puts these only in conditions
            raise SystemExit("enkelj: a comparison used as a value")


def class_name(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    return "".join(part[:1].upper() + part[1:] for part in stem.replace("_", "-").split("-"))


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "-name":
        print(class_name(sys.argv[2]))
        return
    if len(sys.argv) not in (2, 3):
        sys.exit("usage: enkelj.py program.p [folder]")
    path = sys.argv[1]
    folder = sys.argv[2] if len(sys.argv) == 3 else "."
    with open(path) as f:
        text = f.read()
    try:
        program = enkel.Parser(enkel.scan(text)).program()
        enkel.Resolver(program).resolve()
    except enkel.CompileError as error:
        enkel.report(path, text, error)
        sys.exit(1)
    cls = class_name(path)
    data = Compiler(program, cls, os.path.basename(path)).class_file()
    with open(os.path.join(folder, cls + ".class"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
