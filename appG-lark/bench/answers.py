"""
What the three benchmarks must print, worked out apart from any Lark
machine, in Python, with Lark's Int: wrapping two's-complement 32-bit
integers, and division that truncates toward zero.

    python3 bench/answers.py fib|loop|sort
"""

import sys


def i32(x):
    x &= 0xFFFFFFFF
    return x - (1 << 32) if x & 0x80000000 else x


def div(a, b):          # Lark's /: toward zero (b is never 0 here)
    q = abs(a) // abs(b)
    return i32(q if (a < 0) == (b < 0) else -q)


def rem(a, b):          # the benchmark's own rem: a - (a / b) * b
    return i32(a - i32(div(a, b) * b))


def fib():
    a, b = 0, 1
    for _ in range(32):
        a, b = b, a + b
    return a


def loop():
    acc = 0
    for n in range(10000000, 0, -1):
        acc = i32(acc + n)
    return acc


def sort():
    def numbers(n, seed):
        acc = []
        while n:
            seed = rem(i32(i32(seed * 1103515245) + 12345), 1000003)
            acc.insert(0, seed)
            n -= 1
        return acc

    def check(xs):
        acc = 0
        for h in xs:
            acc = rem(i32(i32(acc * 31) + h), 1000003)
        return acc

    acc = 0
    for k in range(100, 0, -1):
        acc = rem(i32(acc + check(sorted(numbers(1000, k)))), 1000003)
    return acc


if __name__ == "__main__":
    print({"fib": fib, "loop": loop, "sort": sort}[sys.argv[1]]())
