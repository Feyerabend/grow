#!/usr/bin/env python3
"""A class file made old: version 49, of Java 5, with its StackMapTables
taken out, as javac would have written it before Java 6.

    usage: old.py in.class out.class
"""

import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from classfile import ClassFile        # noqa: E402

with open(sys.argv[1], "rb") as f:
    c = ClassFile(f.read())
data = c.without_stack_maps()
struct.pack_into(">HH", data, 4, 0, 49)
with open(sys.argv[2], "wb") as f:
    f.write(data)
print(f"{os.path.basename(sys.argv[1])}: {len(c.data)} bytes, {len(data)} without its stack maps")
