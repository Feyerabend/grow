#!/usr/bin/env python3
"""
Exercise 15.1: both machines with TAILCALLI n, code 32.

    TAILCALLI n   n = operand; pop t, a number; if t is not an address in
                  the code, trap: jump out of program; if there are no
                  frames, trap: tail call without call; if n < 0, or the
                  current call has fewer than n locals, trap: not enough
                  arguments. Then the top n values become locals 0 to n - 1
                  of the current frame, in order, everything else of the
                  current call is removed, and pc = t. The frame itself, its
                  return address and saved fp, is kept: the called code
                  returns straight to the caller's caller.

    usage: python3 build.py c > vm_more.c
           python3 build.py py > vm_more.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CH15 = os.path.join(HERE, "..")


def change(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new)


def c():
    s = open(os.path.join(CH15, "vm.c")).read()
    s = change(s, "    CALLI,\n    NOPS", "    CALLI,\n    TAILCALLI,\n    NOPS")
    s = change(s, '    "CALLI"\n};', '    "CALLI", "TAILCALLI"\n};')
    s = change(s, "    [CALLI] = 1\n};", "    [CALLI] = 1, [TAILCALLI] = 1\n};")
    s = change(s, "    case RET:\n", """    case TAILCALLI: {
        int addr, nargs, i;
        nargs = operand();
        addr = number(pop());
        if (addr < 0 || addr >= code_len)
            trap("jump out of program");
        if (fsp == 0)
            trap("tail call without call");
        if (nargs < 0 || nargs > sp - fp)
            trap("not enough arguments");
        for (i = 0; i < nargs; i++)
            stack[fp + i] = stack[sp - nargs + i];
        sp = fp + nargs;
        pc = addr;
        break;
    }
    case RET:
""")
    return s


def py():
    s = open(os.path.join(CH15, "vm.py")).read()
    s = change(s, "import isa\n", "import isa\n\nisa.INSTRUCTIONS.append((32, \"TAILCALLI\", (\"n\",)))\n"
               "isa.BY_NAME[\"TAILCALLI\"] = (32, (\"n\",))\nisa.BY_CODE[32] = (\"TAILCALLI\", (\"n\",))\n")
    s = change(s, '        elif name == "RET":\n', '''        elif name == "TAILCALLI":
            nargs = self.operand()
            addr = self.number(self.pop())
            if not 0 <= addr < len(self.code):
                raise Trap("jump out of program")
            if not self.frames:
                raise Trap("tail call without call")
            if nargs < 0 or nargs > len(self.stack) - self.fp:
                raise Trap("not enough arguments")
            arguments = self.stack[len(self.stack) - nargs:]
            del self.stack[self.fp:]
            self.stack.extend(arguments)
            self.pc = addr
        elif name == "RET":
''')
    return s


sys.stdout.write(c() if sys.argv[1:] == ["c"] else py())
