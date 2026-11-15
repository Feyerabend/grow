#!/usr/bin/env python3
"""
Exercise 11.5, measured: measure/onepass.py's program of 20000 assignments,
compiled by basal.py, which holds every token, and by basal_stream.py, which
reads the file a line at a time and writes as it goes. For each, the peak of
what Python allocates while compiling (tracemalloc); for the stream, also
what it keeps to the end.

    usage: python3 stream_memory.py [lines]
"""

import os
import sys
import tempfile
import tracemalloc

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "measure"))
os.chdir(os.path.join(HERE, ".."))              # onepass.py finds enkel.py from there
import basal                                    # noqa: E402
import basal_stream                             # noqa: E402
import onepass                                  # noqa: E402


class Discard:
    def write(self, text):
        pass


lines = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
text, _ = onepass.programs(lines)
with tempfile.TemporaryDirectory() as folder:
    path = os.path.join(folder, "p.bas")
    open(path, "w").write(text)

    tracemalloc.start()
    with open(path) as f:
        basal.Translator(basal.desugar(basal.scan(f.read()))).program()
    whole = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    tracemalloc.start()
    with open(path) as f:
        t = basal_stream.Translator(basal_stream.desugar_stream(basal_stream.scan_lines(f)), Discard())
        t.program()
    stream = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

print(f"{lines} assignments, then 26 prints")
print(f"  basal.py, every token held:     peak {whole / 1e6:7.1f} MB")
print(f"  basal_stream.py, line by line:  peak {stream / 1e3:7.1f} KB")
print(f"  what the stream keeps to the end: {len(t.variables)} variables, "
      f"{len(t.labels_defined)} labels, {len(t.labels_used)} uses of labels")
