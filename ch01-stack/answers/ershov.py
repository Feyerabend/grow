"""Exercise 1.3: every way to add eight numbers, as a tree, and the stack each
needs in its best order: Ershov's number, which chapter 1's measure/depth.py
checks against the machine."""

from functools import lru_cache


@lru_cache(None)
def trees(n):
    """The Ershov numbers of all binary trees with n leaves, with how many have each."""
    if n == 1:
        return {1: 1}
    counts = {}
    for k in range(1, n):
        for a, x in trees(k).items():
            for b, y in trees(n - k).items():
                e = max(a, b) if a != b else a + 1
                counts[e] = counts.get(e, 0) + x * y
    return counts


for n in range(1, 17):
    c = trees(n)
    print(f"{n:2} leaves: {sum(c.values()):>9} trees; the most any needs: {max(c)}, "
          f"and {c[max(c)]} need it")
