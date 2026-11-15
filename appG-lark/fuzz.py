"""
Random well-typed programs, run on Lark's own CEK machine in Python and
on this one, which must print the same.

    python3 fuzz.py [N]

The programs come from Lark's generator (lark/tests/gen_prog.py), which
builds them by inverting the typing rules, so every one is well typed
and ends. Hypothesis drives it, and a program on which the two machines
differ is shrunk to a small one before it is reported.
"""

import contextlib
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lark", "src"))
sys.path.insert(0, os.path.join(HERE, "lark", "tests"))

from hypothesis import HealthCheck, given, settings   # noqa: E402

import cek as lark_cek                                 # noqa: E402
import emit                                            # noqa: E402
from gen_prog import lark_programs                     # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
# The machine to run: build/lark, or another build of it, such as the one
# that checks every variable's depth (LARK_MACHINE=build/lark-checked).
MACHINE = os.environ.get("LARK_MACHINE", os.path.join(HERE, "build", "lark"))
WORK = tempfile.mkdtemp(prefix="lark-fuzz-")
count = 0


def oracle(path):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        lark_cek.run_file(path)
    return out.getvalue()


@settings(max_examples=N, deadline=None, database=None,
          suppress_health_check=list(HealthCheck))
@given(lark_programs())
def agree(source):
    global count
    count += 1
    path = os.path.join(WORK, "p.lark")
    tree = os.path.join(WORK, "p.tree")
    with open(path, "w") as f:
        f.write(source)
    expected = oracle(path)
    with open(tree, "w") as f:
        f.write(emit.emit(path))
    got = subprocess.run([MACHINE, tree], capture_output=True, text=True)
    assert got.returncode == 0, f"machine failed: {got.stderr}\n{source}"
    assert got.stdout == expected, f"outputs differ\n{source}"


if __name__ == "__main__":
    agree()
    print(f"{count} generated programs: the two machines agree")
