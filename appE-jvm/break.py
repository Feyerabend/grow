#!/usr/bin/env python3
"""Class files broken on purpose, each in one way, for the verifiers.

Each case takes a class file that javac made, from classes/, changes a few
of its bytes, and writes it as build/broken/<case>/<Class>.class. Every one
must be refused, by this machine and by Java, before any of it runs; except
the cases in DIFFER, where the two are known to disagree, for the reason
given.

    usage: break.py [classes folder] [output folder]
"""

import os
import struct
import sys

from classfile import ClassFile

CASES = []


def case(name, cls, why):
    def register(f):
        CASES.append((name, cls, why, f))
        return f
    return register


FIB = "fib(I)I"
MAIN = "main([Ljava/lang/String;)V"


@case("load-int-as-reference", "Fib", "aload_0 where fib's n is an int")
def _(c):
    c.data[c.at(FIB, 0x1a)] = 0x2a


@case("int-as-array", "Sieve", "iload_1, an int, where iaload wants the array")
def _(c):
    c.data[c.at(MAIN, 0x2c)] = 0x1b          # the first aload_2 becomes iload_1


@case("store-int-as-reference", "Sieve", "astore_1 of the int 100")
def _(c):
    c.data[c.at(MAIN, 0x3c)] = 0x4c


@case("underflow", "Fib", "iconst_2 removed: if_icmpge finds one value")
def _(c):
    c.data[c.at(FIB, 0x05)] = 0x00


@case("max-stack", "Fib", "max_stack one less than fib needs")
def _(c):
    m = c.methods[FIB]
    c.data[m.max_stack + 1] -= 1


@case("max-locals", "Sieve", "max_locals one less than main's locals")
def _(c):
    m = c.methods[MAIN]
    c.data[m.max_locals + 1] -= 1


@case("no-stackmap", "Sieve", "the StackMapTable renamed, so not there")
def _(c):
    m = c.methods[MAIN]
    struct.pack_into(">H", c.data, m.stackmap_name, c.find("Utf8", "SourceFile"))


@case("frame-says-top", "Sieve", "the first frame says p is top, not int")
def _(c):
    m = c.methods[MAIN]
    p = m.stackmap + 2                         # frame_type 254, an append
    assert c.data[p] == 254 and c.data[p + 3:p + 8] == bytes([1, 7, 0, c.data[p + 6], 1])
    c.data[p + 7] = 0


@case("frame-says-null", "Bits", "abs's frame says null where an int is")
def _(c):
    m = c.methods["abs(I)I"]
    p = m.stackmap + 2
    p += 1                                     # past the first, same_frame
    assert 64 <= c.data[p] < 128 and c.data[p + 1] == 1
    c.data[p + 1] = 5


@case("branch-without-frame", "Fib", "if_icmpge to 8, which has no frame")
def _(c):
    p = c.at(FIB, 0xa2)
    struct.pack_into(">h", c.data, p + 1, struct.unpack(">h", c.data[p + 1:p + 3])[0] + 1)


@case("branch-into-instruction", "Sieve", "goto into the middle of istore 4")
def _(c):
    p = c.at(MAIN, 0xa7)                       # goto 29, at 46
    struct.pack_into(">h", c.data, p + 1, struct.unpack(">h", c.data[p + 1:p + 3])[0] - 1)


@case("return-without-value", "Fib", "return where fib must return an int")
def _(c):
    c.data[c.at(FIB, 0xac)] = 0xb1


@case("falls-off-the-end", "Fib", "the last ireturn made a nop")
def _(c):
    c.data[c.at(FIB, 0xac, 1)] = 0x00


@case("code-after-return", "Fib", "iadd made ireturn: then an instruction with no frame")
def _(c):
    c.data[c.at(FIB, 0x60)] = 0xac


@case("constructor-without-super", "Fib", "<init> returns before calling Object's")
def _(c):
    m = c.methods["<init>()V"]
    for i in range(4):
        c.data[m.code + i] = 0x00


@case("wrong-field", "Queens", "putstatic of an int into column, an int[]")
def _(c):
    p = c.at("place(I)V", 0xb3)
    struct.pack_into(">H", c.data, p + 1, c.find("Fieldref", "Queens.column:[I"))


@case("wrong-argument", "Divide", "println(String) given share's int")
def _(c):
    p = c.at(MAIN, 0xb6, 1)
    struct.pack_into(">H", c.data, p + 1,
                     c.find("Methodref", "java/io/PrintStream.println:(Ljava/lang/String;)V"))


@case("call-a-field", "Fib", "invokestatic of a Fieldref")
def _(c):
    p = c.at(MAIN, 0xb8)
    struct.pack_into(">H", c.data, p + 1, c.find("Fieldref", "java/lang/System.out:Ljava/io/PrintStream;"))


@case("unsorted-keys", "Switch", "roman's lookupswitch with two keys swapped")
def _(c):
    p = c.at("roman(I)C", 0xab)
    q = (p - c.methods["roman(I)C"].code + 4 & ~3) + c.methods["roman(I)C"].code
    a, b = c.data[q + 8:q + 16], c.data[q + 16:q + 24]
    c.data[q + 8:q + 16], c.data[q + 16:q + 24] = b, a


@case("bad-magic", "Fib", "CAFEBABE made CAFEBABF")
def _(c):
    c.data[3] = 0xBF


@case("truncated", "Fib", "the last ten bytes cut off")
def _(c):
    del c.data[-10:]


# Changes on which the two disagree: which one accepts it, and why.
DIFFER = {}


@case("version-49", "Fib", "made version 49, of Java 5, with its StackMapTables still in it")
def _(c):
    struct.pack_into(">HH", c.data, 4, 0, 49)


DIFFER["version-49"] = ("Java", "Java verifies a class file of version 49 by type inference, "
                        "and ignores its StackMapTable; this machine has only type checking")


@case("illegal-name", "Fib", "the method fib renamed f;b, a name the format forbids")
def _(c):
    p = c.pool[c.find("Utf8", "fib")][2]
    c.data[p + 4] = ord(";")


DIFFER["illegal-name"] = ("this machine", "Java checks names, as the format asks (4.2.2); "
                          "this machine does not")


def main():
    source = sys.argv[1] if len(sys.argv) > 1 else "classes"
    out = sys.argv[2] if len(sys.argv) > 2 else "build/broken"
    for name, cls, why, change in CASES:
        with open(os.path.join(source, cls + ".class"), "rb") as f:
            c = ClassFile(f.read())
        change(c)
        os.makedirs(os.path.join(out, name), exist_ok=True)
        with open(os.path.join(out, name, cls + ".class"), "wb") as f:
            f.write(c.data)
    with open(os.path.join(out, "cases.txt"), "w") as f:
        for name, cls, why, _ in CASES:
            who, reason = DIFFER.get(name, ("", ""))
            f.write(f"{name}\t{cls}\t{why}\t{who}\t{reason}\n")


if __name__ == "__main__":
    main()
