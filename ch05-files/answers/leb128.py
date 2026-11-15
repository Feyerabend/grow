#!/usr/bin/env python3
"""
Exercise 5.6: the samples' code words in signed LEB128, seven bits a byte, the
high bit set on every byte but the last, against four bytes a word. Each file
is encoded, decoded again and checked against the words it came from.

    usage: python3 leb128.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import tobin                                    # noqa: E402


def encode(n):
    out = bytearray()
    while True:
        byte = n & 0x7f
        n >>= 7                                 # Python's >> keeps the sign
        if (n == 0 and not byte & 0x40) or (n == -1 and byte & 0x40):
            out.append(byte)
            return bytes(out)
        out.append(byte | 0x80)


def decode(data, i):
    """The number that starts at data[i], and where the next one starts."""
    result, shift = 0, 0
    while True:
        byte = data[i]
        i += 1
        result |= (byte & 0x7f) << shift
        shift += 7
        if not byte & 0x80:
            if byte & 0x40:
                result -= 1 << shift
            return result, i


total_old = total_new = 0
for name in ("gcd", "fib", "primes", "fact"):
    with open(os.path.join(HERE, "..", "samples", name + ".txt")) as f:
        code = tobin.translate(f.read(), name)
    data = b"".join(encode(w) for w in code)
    back, i = [], 0
    while i < len(data):
        n, i = decode(data, i)
        back.append(n)
    assert back == code, name
    old, new = 8 + 4 * len(code), 8 + len(data)
    total_old, total_new = total_old + old, total_new + new
    print(f"{name:<7} {len(code):>3} words: {old:>4} bytes, in LEB128 {new:>4}, "
          f"{100 * new / old:.0f}%")
print(f"all four: {total_old} bytes, in LEB128 {total_new}, {100 * total_new / total_old:.0f}%")
for n in (0, 1, 63, 64, -1, -64, -65, 1071, 2**31 - 1, -2**31):
    print(f"{n:>11}: {encode(n).hex(' ')}")
