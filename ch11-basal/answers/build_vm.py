#!/usr/bin/env python3
"""
Exercise 11.1: chapter 11's vm.c with READ, code 27: skip white space on
standard input, read a decimal number, with a '-' before it if negative,
and push it. At the end of the input it traps, "end of input"; on anything
else that is not a number, or one that does not fit in 32 bits, "not a
number".

    usage: python3 build_vm.py > vm_read.c
"""

import os

s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vm.c")).read()


def change(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)


change("    AND, OR, XOR, LOADM, STOREM, EMIT,\n    NOPS",
       "    AND, OR, XOR, LOADM, STOREM, EMIT,\n    READ,\n    NOPS")
change('"AND", "OR", "XOR", "LOADM", "STOREM", "EMIT"\n};',
       '"AND", "OR", "XOR", "LOADM", "STOREM", "EMIT", "READ"\n};')
change("""        default:
            trap("unknown instruction");""", """        case READ: {
            int c, negative = 0;
            long long n = 0;

            do
                c = getchar();
            while (c == ' ' || c == '\\t' || c == '\\n' || c == '\\r');
            if (c == EOF)
                trap("end of input");
            if (c == '-') {
                negative = 1;
                c = getchar();
            }
            if (c < '0' || c > '9')
                trap("not a number");
            while (c >= '0' && c <= '9') {
                n = n * 10 + (c - '0');
                if (n > 2147483648LL)
                    trap("not a number");
                c = getchar();
            }
            if (c != EOF && c != ' ' && c != '\\t' && c != '\\n' && c != '\\r')
                trap("not a number");
            n = negative ? -n : n;
            if (n > 2147483647LL)
                trap("not a number");
            push((int) n);
            break;
        }
        default:
            trap("unknown instruction");""")
print(s, end="")
