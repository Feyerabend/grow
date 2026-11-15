#!/usr/bin/env python3
"""
Exercise 21.5: fuzz.py, made to call a function, sometimes in two ways.

    python3 fuzz_more.py seed count directory

fuzz.py's programs never call. These are fuzz.py's, made from its source
with three changes: half of them get a function f, of 1 to 3 arguments,
which loads its last argument and returns it; the main program calls it,
now and then, where the stack holds enough; and in three in ten of those
programs, a call after the first may pass fewer. This is a cheat of its
own, apart from fuzz.py's, so that nothing else in the program is refused. The verifier follows the first call
it meets, which passes the right number, so f is then called with two
numbers of arguments, and, with fewer, its LOAD reads past its frame.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
sys.path.insert(0, CHAPTER)


def patch(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


source = open(os.path.join(CHAPTER, "fuzz.py")).read()
source = patch(source, "    cheat = rng.random() < 0.3\n", """    cheat = rng.random() < 0.3
    calls, K, fixups = rng.random() < 0.5, rng.randint(1, 3), []
    odd = rng.random() < 0.3                # calls that pass too few
""")
source = patch(source, """        else:
            name = rng.choice(list(POPS))""", """        elif calls and r < 0.56:
            k = rng.randint(0, K - 1) if odd and fixups and rng.random() < 0.5 else K
            if k <= d:
                fixups.append(len(code) + 1)
                code += [isa.BY_NAME["CALL"][0], 0, k]
                d = d - k + 1
        else:
            name = rng.choice(list(POPS))""")
source = patch(source, """        code = code[:-1]                    # run off the end
    return code""", """        code = code[:-1]                    # run off the end
    if fixups:
        for at in fixups:
            code[at] = len(code)
        code += [isa.BY_NAME["LOAD"][0], K - 1, isa.BY_NAME["RET"][0]]
    return code""")
exec(compile(source, "fuzz.py, with calls", "exec"))
