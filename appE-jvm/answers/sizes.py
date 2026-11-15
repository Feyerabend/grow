#!/usr/bin/env python3
"""What the StackMapTables cost in bytes: for javac's classes, and for
enkelj's, the bytes of the class files, of their code, and of their stack
maps, attribute and all, with the number of frames.

    usage: sizes.py folder...
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from classfile import ClassFile        # noqa: E402

for folder in sys.argv[1:]:
    files = sorted(f for f in os.listdir(folder) if f.endswith(".class"))
    total = code = maps = frames = 0
    for name in files:
        with open(os.path.join(folder, name), "rb") as f:
            c = ClassFile(f.read())
        total += len(c.data)
        for m in c.methods.values():
            code += getattr(m, "code_length", 0)
            if m.stackmap is not None:
                maps += 6 + m.stackmap_length
                frames += c.u2(m.stackmap)
    print(f"{os.path.basename(folder.rstrip('/'))}: {len(files)} classes, {total} bytes; code {code}, "
          f"stack maps {maps} ({100 * maps / total:.1f}% of the files, "
          f"{100 * maps / code:.1f}% of the code), {frames} frames")
