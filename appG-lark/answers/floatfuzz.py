"""
Exercise G.6: Lark's generator with floats added, run on Lark's own CEK
machine in Python and on this one, which round every float to 32 bits.

    python3 floatfuzz.py [N] [show]

Lark's generator (lark/tests/gen_prog.py) leaves floats out, because
Lark's intermediate machine computes them in 64 bits. Here a Float goal
is added: literals, arithmetic, negation, int_to_float, float_abs,
float_sqrt, float_floor and float_ceil; and the other goals reach it
through show, comparisons and float_to_int. Hypothesis shrinks the first
program on which the machines differ, and it is printed with both
outputs. Differences already explained are in EXPLAINED; with
KNOWN=all, a program that shows only those is passed over, so that the
run looks for another.
"""

import contextlib
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.dirname(HERE)
sys.path.insert(0, TOP)
sys.path.insert(0, os.path.join(TOP, "lark", "src"))
sys.path.insert(0, os.path.join(TOP, "lark", "tests"))

from hypothesis import HealthCheck, given, settings   # noqa: E402
from hypothesis import strategies as st               # noqa: E402

import cek as lark_cek                                 # noqa: E402
import emit                                            # noqa: E402
import gen_prog                                        # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
MACHINE = os.environ.get("LARK_MACHINE", os.path.join(TOP, "build", "lark"))
WORK = tempfile.mkdtemp(prefix="lark-float-")
# Ways of differing already explained, each a way of making Lark's
# output into this machine's; KNOWN=all passes over every one of them.
import re                                              # noqa: E402


def nan_inf(out):
    """show writes nan and inf with .0 after them."""
    return re.sub(r"(nan|inf)\.0", r"\1", out)


def too_large(out):
    """_f32 packs with struct, which refuses a number too large for 32
    bits, where C rounds it to infinity: Lark's machine stops."""
    return None if "OverflowError: float too large to pack" in out else out


def floor_int(out):
    """float_floor and float_ceil go through Python's math.floor and
    math.ceil, which give an integer, and a NaN or an infinity has none:
    Lark's machine stops."""
    stops = ("cannot convert float NaN to integer",
             "cannot convert float infinity to integer")
    return None if any(m in out for m in stops) else out


EXPLAINED = [nan_inf, too_large, floor_int]
KNOWN = EXPLAINED if os.environ.get("KNOWN") == "all" else []
# float_to_int of a number outside 32 bits: Lark's machine wraps it, and
# in C the cast is undefined; on this computer it saturates. Programs that
# use float_to_int are passed over whole, with KNOWN=all.


def explained(expected, got, source=""):
    if KNOWN and "float_to_int" in source:
        return True
    if any(f(expected) is None for f in KNOWN):
        return True
    for k in range(1, len(KNOWN) + 1):
        out = expected
        for f in KNOWN[:k]:
            out = f(out)
        if out == got:
            return True
    return False

LITERALS = ["0.0", "1.0", "0.5", "2.5", "0.1", "3.14159", "1000.0",
            "16777217.0", "123456789.0", "340282350000000000000000000000000000000.0"]


class FloatGen(gen_prog._Gen):
    def expr(self, goal, ctx, fuel):
        if goal == "Float":
            rules = [(3, "flit")]
            if fuel > 0:
                rules += [(3, "farith"), (1, "fneg"), (1, "int_to_float"),
                          (2, "fbuiltin"), (1, "if_"), (1, "let_")]
            return getattr(self, "r_" + self.pick(rules))(goal, ctx, fuel)
        if fuel > 0 and self.draw(st.integers(0, 3)) == 0:
            if goal == "String":
                return self.r_show_float(goal, ctx, fuel)
            if goal == "Bool":
                return self.r_fcmp(goal, ctx, fuel)
            if goal == "Int":
                return self.r_float_to_int(goal, ctx, fuel)
        return super().expr(goal, ctx, fuel)

    def r_flit(self, goal, ctx, fuel):
        text = self.draw(st.one_of(
            st.sampled_from(LITERALS),
            st.builds(lambda a, b: f"{a}.{b}", st.integers(0, 10**9), st.integers(0, 999))))
        if self.draw(st.booleans()):
            text = f"(0.0 - {text})"
        return text, False

    def r_farith(self, goal, ctx, fuel):
        op = self.draw(st.sampled_from(["+", "-", "*", "/"]))
        l, _ = self.expr("Float", ctx, fuel - 1)
        if op == "/" and self.draw(st.booleans()):
            r = "0.0"
        else:
            r, _ = self.expr("Float", ctx, fuel - 1)
        return f"({l} {op} {r})", False

    def r_fneg(self, goal, ctx, fuel):
        return f"(- {self.expr('Float', ctx, fuel - 1)[0]})", False

    def r_int_to_float(self, goal, ctx, fuel):
        return f"int_to_float({self.expr('Int', ctx, fuel - 1)[0]})", False

    def r_fbuiltin(self, goal, ctx, fuel):
        f = self.draw(st.sampled_from(["float_abs", "float_sqrt", "float_floor", "float_ceil"]))
        return f"{f}({self.expr('Float', ctx, fuel - 1)[0]})", False

    def r_show_float(self, goal, ctx, fuel):
        return f"show({self.expr('Float', ctx, fuel - 1)[0]})", False

    def r_fcmp(self, goal, ctx, fuel):
        op = self.draw(st.sampled_from(["==", "!=", "<", "<=", ">", ">="]))
        l, _ = self.expr("Float", ctx, fuel - 1)
        r, _ = self.expr("Float", ctx, fuel - 1)
        return f"({l} {op} {r})", False

    def r_float_to_int(self, goal, ctx, fuel):
        return f"float_to_int({self.expr('Float', ctx, fuel - 1)[0]})", False


@st.composite
def float_programs(draw):
    return FloatGen(draw).program()


def run_both(source):
    path = os.path.join(WORK, "p.lark")
    tree = os.path.join(WORK, "p.tree")
    with open(path, "w") as f:
        f.write(source)
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            lark_cek.run_file(path)
        expected = out.getvalue()
    except Exception as e:                 # Lark's machine stopped with an error
        expected = out.getvalue() + f"<error: {type(e).__name__}: {e}>"
    with open(tree, "w") as f:
        f.write(emit.emit(path))
    got = subprocess.run([MACHINE, tree], capture_output=True, text=True)
    return expected, got.stdout + (f"<status {got.returncode}>" if got.returncode else "")


count = 0
found = []


@settings(max_examples=N, deadline=None, database=None, derandomize=True,
          suppress_health_check=list(HealthCheck))
@given(float_programs())
def agree(source):
    global count
    count += 1
    expected, got = run_both(source)
    if expected != got and not explained(expected, got, source):
        found.append((source, expected, got))
        raise AssertionError("the machines differ")


if __name__ == "__main__":
    try:
        agree()
        print(f"{count} programs: the two machines agree")
    except AssertionError:
        source, expected, got = found[-1]
        print(source)
        print("Lark's machine: " + expected)
        print("this machine:   " + got)
