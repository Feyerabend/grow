"""Reading and writing class files, for break.py and enkelj.py.

Only what those two need: the constant pool, the methods and where each
one's code and stack map are in the file's bytes; and, for writing, a
constant pool that gives each constant one entry.
"""

import struct

# The lengths of the instructions that have operands; the rest take one byte.
LENGTHS = {16: 2, 18: 2, 21: 2, 22: 2, 23: 2, 24: 2, 25: 2, 54: 2, 55: 2,
           56: 2, 57: 2, 58: 2, 169: 2, 188: 2, 17: 3, 19: 3, 20: 3, 132: 3,
           178: 3, 179: 3, 180: 3, 181: 3, 182: 3, 183: 3, 184: 3, 187: 3,
           189: 3, 192: 3, 193: 3, 198: 3, 199: 3, 197: 4, 185: 5, 186: 5,
           200: 5, 201: 5}
LENGTHS.update({op: 3 for op in range(153, 169)})


def instruction_length(code, pc):
    op = code[pc]
    if op == 196:
        return 6 if code[pc + 1] == 132 else 4
    if op in (170, 171):
        p = (pc + 4) & ~3
        a, b = struct.unpack(">ii", code[p + 4:p + 12])
        return p - pc + 12 + (4 * (b - a + 1) if op == 170 else 8 * a - 4)
    return LENGTHS.get(op, 1)


def instructions(code):
    """The offset and opcode of each instruction."""
    pc = 0
    while pc < len(code):
        yield pc, code[pc]
        pc += instruction_length(code, pc)


class Method:
    pass


class ClassFile:
    """A class file read: its bytes, its pool, and its methods' places."""

    def __init__(self, data):
        self.data = bytearray(data)
        self.pool = [None]
        p = 10
        count = struct.unpack(">H", data[8:10])[0]
        i = 1
        while i < count:
            tag = data[p]
            if tag == 1:
                n = struct.unpack(">H", data[p + 1:p + 3])[0]
                self.pool.append(("Utf8", data[p + 3:p + 3 + n].decode("utf-8", "replace"), p))
                p += 3 + n
            elif tag in (3, 4):
                self.pool.append(("Integer" if tag == 3 else "Float",
                                  struct.unpack(">i", data[p + 1:p + 5])[0], p))
                p += 5
            elif tag in (5, 6):
                self.pool += [("Long", 0, p), None]
                p += 9
                i += 1
            elif tag in (7, 8, 16, 19, 20):
                self.pool.append(({7: "Class", 8: "String"}.get(tag, "other"),
                                  struct.unpack(">H", data[p + 1:p + 3])[0], p))
                p += 3
            elif tag == 15:
                self.pool.append(("other", 0, p))
                p += 4
            else:
                a, b = struct.unpack(">HH", data[p + 1:p + 5])
                self.pool.append(({9: "Fieldref", 10: "Methodref", 11: "InterfaceMethodref",
                                   12: "NameAndType"}.get(tag, "other"), (a, b), p))
                p += 5
            i += 1
        self.pool_end = p
        p += 6
        interfaces = struct.unpack(">H", data[p:p + 2])[0]
        p += 2 + 2 * interfaces
        p = self.members(p, None)
        self.methods = {}
        self.members(p, self.methods)

    def u2(self, p):
        return struct.unpack(">H", self.data[p:p + 2])[0]

    def utf8(self, i):
        return self.pool[i][1]

    def find(self, kind, text):
        """The index of the constant of this kind whose text is text:
        for a member, Class.name:descriptor."""
        for i, k in enumerate(self.pool):
            if k and k[0] == kind and self.describe(i) == text:
                return i
        raise KeyError(f"{kind} {text}")

    def describe(self, i):
        kind, value, _ = self.pool[i]
        if kind == "Utf8":
            return value
        if kind in ("Class", "String"):
            return self.utf8(value)
        if kind == "NameAndType":
            return self.utf8(value[0]) + ":" + self.utf8(value[1])
        if kind in ("Fieldref", "Methodref", "InterfaceMethodref"):
            return self.describe(value[0]) + "." + self.describe(value[1])
        return str(value)

    def members(self, p, into):
        count = self.u2(p)
        p += 2
        for _ in range(count):
            name, descriptor = self.utf8(self.u2(p + 2)), self.utf8(self.u2(p + 4))
            attributes = self.u2(p + 6)
            p += 8
            m = Method()
            m.name, m.descriptor, m.stackmap = name, descriptor, None
            for _ in range(attributes):
                aname = self.utf8(self.u2(p))
                length = struct.unpack(">I", self.data[p + 2:p + 6])[0]
                if aname == "Code":
                    m.attribute = p                     # the Code attribute
                    m.max_stack, m.max_locals = p + 6, p + 8
                    code_length = struct.unpack(">I", self.data[p + 10:p + 14])[0]
                    m.code = p + 14
                    m.code_length = code_length
                    q = m.code + code_length
                    q += 2 + 8 * self.u2(q)
                    m.code_attributes = q               # their count
                    for _ in range(self.u2(q)):
                        sub = self.utf8(self.u2(q + 2))
                        sub_length = struct.unpack(">I", self.data[q + 4:q + 8])[0]
                        if sub == "StackMapTable":
                            m.stackmap_name = q + 2
                            m.stackmap = q + 8          # number_of_entries
                            m.stackmap_length = sub_length
                        q += 6 + sub_length
                p += 6 + length
            if into is not None:
                into[name + descriptor] = m
        return p

    def without_stack_maps(self):
        """The class file with every StackMapTable taken out."""
        data = bytearray(self.data)
        for m in sorted(self.methods.values(), key=lambda m: -m.attribute):
            if m.stackmap is None:
                continue
            start, size = m.stackmap_name, 6 + m.stackmap_length
            del data[start:start + size]
            struct.pack_into(">H", data, m.code_attributes,
                             struct.unpack(">H", data[m.code_attributes:m.code_attributes + 2])[0] - 1)
            struct.pack_into(">I", data, m.attribute + 2,
                             struct.unpack(">I", data[m.attribute + 2:m.attribute + 6])[0] - size)
        return data

    def code(self, method):
        m = self.methods[method]
        return self.data[m.code:m.code + m.code_length]

    def at(self, method, opcode, n=0):
        """The file offset of the n-th instruction with this opcode in a
        method's code."""
        m = self.methods[method]
        found = [pc for pc, op in instructions(self.code(method)) if op == opcode]
        return m.code + found[n]


class Pool:
    """A constant pool being written: each constant gets one entry."""

    def __init__(self):
        self.entries = []
        self.index = {}

    def add(self, key, data):
        if key not in self.index:
            self.entries.append(data)
            self.index[key] = len(self.entries)
        return self.index[key]

    def utf8(self, s):
        b = s.encode("utf-8")
        return self.add(("Utf8", s), b"\x01" + struct.pack(">H", len(b)) + b)

    def integer(self, n):
        return self.add(("Integer", n), b"\x03" + struct.pack(">i", n))

    def klass(self, name):
        return self.add(("Class", name), b"\x07" + struct.pack(">H", self.utf8(name)))

    def string(self, s):
        return self.add(("String", s), b"\x08" + struct.pack(">H", self.utf8(s)))

    def name_and_type(self, name, descriptor):
        return self.add(("NameAndType", name, descriptor),
                        b"\x0c" + struct.pack(">HH", self.utf8(name), self.utf8(descriptor)))

    def member(self, tag, owner, name, descriptor):
        return self.add((tag, owner, name, descriptor),
                        bytes([tag]) + struct.pack(">HH", self.klass(owner),
                                                   self.name_and_type(name, descriptor)))

    def field(self, owner, name, descriptor):
        return self.member(9, owner, name, descriptor)

    def method(self, owner, name, descriptor):
        return self.member(10, owner, name, descriptor)

    def bytes(self):
        return struct.pack(">H", len(self.entries) + 1) + b"".join(self.entries)
