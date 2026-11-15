"""
Compare two outputs that may differ in the last figure of a real.

    python3 lastdigit.py expected actual

Free Pascal, and so pint, writes a real with digits of its own making,
which are not always correctly rounded (see write_real in p4.c). This
machine's are, nearly always, so the two can differ by one in the last
figure. Everything else must be the same: the words between the
numbers, the spaces, the form of each real, its exponent.
"""

import re
import sys

REAL = re.compile(r"-?\d\.\d+e[+-]\d{3}")


def same(expected, actual):
    a, b = REAL.split(expected), REAL.split(actual)
    if a != b:
        return False
    for x, y in zip(REAL.findall(expected), REAL.findall(actual)):
        if x == y:
            continue
        mx, ex = x.split("e")
        my, ey = y.split("e")
        if ex != ey or len(mx) != len(my):
            return False
        # the figures as whole numbers: a float cannot hold seventeen
        if abs(int(mx.replace(".", "")) - int(my.replace(".", ""))) > 1:
            return False
    return True


if __name__ == "__main__":
    expected = open(sys.argv[1]).read()
    actual = open(sys.argv[2]).read()
    if not same(expected, actual):
        print(f"{sys.argv[2]}: not within one in the last figure of {sys.argv[1]}")
        sys.exit(1)
