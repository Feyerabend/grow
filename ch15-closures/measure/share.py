#!/usr/bin/env python3
"""
Two closures that share a variable which can change, in Python: bump
changes n, and get sees the change, since both hold the same cell.

    usage: python3 measure/share.py     prints: 2 True

The same in JavaScript, with node:

    node -e 'function make(){let n=1;return [()=>n,()=>{n+=1}]}
             const [get,bump]=make(); bump(); console.log(get())'    prints: 2
"""


def make():
    n = 1

    def get():
        return n

    def bump():
        nonlocal n
        n += 1
    return get, bump


get, bump = make()
bump()
print(get(), get.__closure__[0] is bump.__closure__[0])
