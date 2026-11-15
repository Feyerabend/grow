#!/usr/bin/env python3
"""
Make the register machine and translator of exercise 19.2, with one more
instruction, a compare and jump, in a folder of their own:

    python3 build.py folder

  folder/rvm.c          rvm.c with JGE and JGEI
  folder/translate.py   translate.py that, given -jge, fuses LT or LTI and
                        the JZ after it into one of them
  folder/rvm-run        the two together, for conform.py, always with -jge

LT and then JZ jumps when LT gave 0, that is when the first value is not
less than the second: so the fused instruction is JGE, jump if greater or
equal, and not JLT. JGE x, y, L jumps to L if rx >= ry; JGEI x, n, L if
rx >= n. Both check that rx and ry are numbers, as LT does, and in the same
order, and carry the address of the LT, since only the LT could trap.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)


def patch(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def main():
    folder = sys.argv[1]
    c = open(os.path.join(CHAPTER, "rvm.c")).read()
    c = patch(c, "    LOADM, STOREM, NEW, GETF, SETF, LEN, TRAP,\n    NOPS",
              "    LOADM, STOREM, NEW, GETF, SETF, LEN, TRAP,\n    JGE, JGEI,\n    NOPS")
    c = patch(c, """        case JZ:
            if (!R(x).is_ref && R(x).n == 0)
                pc = y;
            break;""", """        case JZ:
            if (!R(x).is_ref && R(x).n == 0)
                pc = y;
            break;
        case JGE: {
            int a = number(R(x)), b = number(R(y));
            if (a >= b)
                pc = z;
            break;
        }
        case JGEI:
            if (number(R(x)) >= y)
                pc = z;
            break;""")
    open(os.path.join(folder, "rvm.c"), "w").write(c)

    t = open(os.path.join(CHAPTER, "translate.py")).read()
    t = patch(t, '"LOADM", "STOREM", "NEW", "GETF", "SETF", "LEN", "TRAP"]',
              '"LOADM", "STOREM", "NEW", "GETF", "SETF", "LEN", "TRAP", "JGE", "JGEI"]')
    t = patch(t, '''def assemble(out):''', '''def fuse(out):
    """LT or LTI, and straight after it a JZ on its result, become one
    JGE or JGEI. The result is a stack slot that JZ pops, so nothing
    reads it again; that is checked all the same."""
    final = []
    for item in out:
        lab, ins, org, before, after = item
        if (ins[0] == "JZ" and lab is None and final
                and final[-1][1][0] in ("LT", "LTI")):
            plab, pins, porg, pbefore, pafter = final[-1]
            if pins[1] == ins[1] and pins[1] >= after:
                op = "JGE" if pins[0] == "LT" else "JGEI"
                final[-1] = (plab, [op, pins[2], pins[3], ins[2]], porg, pbefore, after)
                continue
        final.append(item)
    return final


def assemble(out):''')
    t = patch(t, '''        elif ins[0] == "JZ":
            text += f" r{ops[0]}, {ops[1]}"''', '''        elif ins[0] == "JZ":
            text += f" r{ops[0]}, {ops[1]}"
        elif ins[0] == "JGE":
            text += f" r{ops[0]}, r{ops[1]}, {ops[2]}"
        elif ins[0] == "JGEI":
            text += f" r{ops[0]}, {ops[1]}, {ops[2]}"''')
    t = patch(t, '''    plain = "-naive" in args
    args = [a for a in args if a not in ("-l", "-naive")]''', '''    plain = "-naive" in args
    jge = "-jge" in args
    args = [a for a in args if a not in ("-l", "-naive", "-jge")]''')
    t = patch(t, '''        out = strip(out) if plain else improve(out)
''', '''        out = strip(out) if plain else improve(out)
        if jge:
            out = fuse(out)
''')
    open(os.path.join(folder, "translate.py"), "w").write(t)
    for f in ["isa.py", "vmfile.py"]:
        shutil.copy(os.path.join(CHAPTER, f), folder)
    run = os.path.join(folder, "rvm-run")
    open(run, "w").write(open(os.path.join(CHAPTER, "rvm-run")).read().replace(
        'translate.py" "$1"', 'translate.py" -jge "$1"'))
    os.chmod(run, 0o755)


main()
