"""
The test suite of WebAssembly 1.0 writes two of its assertions in a form
the test format has since replaced, and WABT no longer reads:

    (assert_return_canonical_nan (invoke "f" ...))
    (assert_return_arithmetic_nan (invoke "f" ...))

are now written

    (assert_return (invoke "f" ...) (f32.const nan:canonical))

with the type of f's result. This rewrites them.

    python3 nan.py < suite/f32.wast > build/suite/f32.wast f32

The type is the one the function's name begins with (f64.promote_f32),
or the one given, which is the file's: f32.wast and f64.wast test their
own type, and float_exprs.wast's no_fold_promote_demote returns an f32.
"""

import re
import sys

OLD = re.compile(r"\(assert_return_(canonical|arithmetic)_nan\s")


def rewrite(text, default):
    out = []
    i = 0
    for m in OLD.finditer(text):
        if m.start() < i:
            continue
        # the action: from after the keyword to the bracket that closes
        # the whole assertion
        j = m.end()
        depth = 1
        k = j
        while depth:
            c = text[k]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            elif c == '"':
                k = text.index('"', k + 1)
            k += 1
        action = text[j:k - 1].strip()
        field = re.match(r'\(invoke\s+(?:\$\S+\s+)?"([^"]*)"', action).group(1)
        kind = field[:3] if field[:4] in ("f32.", "f64.") else default
        out.append(text[i:m.start()])
        out.append(f"(assert_return {action} ({kind}.const nan:{m.group(1)}))")
        i = k
    out.append(text[i:])
    return "".join(out)


if __name__ == "__main__":
    sys.stdout.write(rewrite(sys.stdin.read(), sys.argv[1]))
