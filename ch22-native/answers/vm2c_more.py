#!/usr/bin/env python3
"""
vm2c.py with two more ways of compiling a verified program, for exercises
22.1 and 22.2.

    usage: vm2c_more.py [-cache] [-calls] program.vm > program.c
           cc -O2 -I.. program.c -o program

-cache   Every value of the current frame is a C variable, s0, s1, ...: the
         value at depth d is always s<d>, since the depth at every
         instruction is known. stack[] is written only where something else
         must read it: before a CALL, the caller's values, so that the
         function called finds its arguments and the collector its roots;
         after a RET, the caller reads its values back; and around NEW,
         which may collect, the frame's values go to stack[] and come back,
         moved if the collector moved them. A push still checks for
         overflow, as fp plus the depth, except in the main program, where
         the frame is the whole stack and the verifier has checked it.

-calls   Every function becomes a C function, and CALL a C call: its frame
         starts at the fp it is given, and RET is return. frames[] is not
         used at all; fsp still counts the calls, so that too many nested
         calls still traps. HALT inside a function ends the program with
         exit(0).

Both at once: the arguments go through stack[], and a caller keeps its own
values in its own C variables across the call, unless the program has a NEW
anywhere, in which case they go to stack[] for the collector and come back.

A program that does not verify, or uses CALLI, is compiled by vm2c.py as it
is. Traps are the same, with the same message at the same address.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
sys.path.insert(0, CHAPTER)
import flow  # noqa: E402  chapter 19's analysis, which says which function each address is in
import isa  # noqa: E402
import vm2c  # noqa: E402
import vmfile  # noqa: E402

NOPERANDS = vm2c.NOPERANDS
PUSHES = {"PUSH", "DUP", "OVER", "LOAD"}        # take the stack one higher


def analyse(code):
    try:
        depth, traps, entries, owner = flow.analyse(code)
    except flow.Refused:
        return None
    if traps:
        return None
    return depth, entries, owner


def compile_program(code, cache, calls):
    found = analyse(code)
    if found is None:
        return vm2c.compile_program(code, False)
    depth, entries, owner = found
    n = len(code)
    has_new = any(isa.BY_CODE[code[a]][0] == "NEW" for a in depth if a < n)
    top = max(list(depth.values()) + [1]) + 2
    functions = {}                      # entry: its addresses, in order
    for a in sorted(depth):
        if a < n:
            functions.setdefault(owner[a], []).append(a)
    returns = set()                     # where a RET goes back to
    for a in depth:
        if a < n and isa.BY_CODE[code[a]][0] == "CALL":
            returns.add(a + 3)

    def body(fn):
        out = []

        def emit(line):
            out.append("    " + line)

        def spill(d):
            for i in range(d):
                emit("stack[fp + %d] = s%d;" % (i, i))

        def reload(d):
            for i in range(d):
                emit("s%d = stack[fp + %d];" % (i, i))

        def overflow(d):
            if fn != 0:
                emit('if (fp + %d >= STACK_SIZE) trap("stack overflow");' % d)

        if calls and fn != 0 and cache:
            reload(entries[fn])                 # the arguments
        for a in functions.get(fn, []):
            op = code[a]
            name = isa.BY_CODE[op][0]
            ops = code[a + 1:a + 1 + NOPERANDS[op]]
            nxt = a + 1 + NOPERANDS[op]
            d = depth[a]
            out.append("A%d: start = %d;" % (a, a))
            if name == "HALT":
                emit("return;" if fn == 0 or not calls else "exit(0);")
                continue
            if name == "PUSH":
                overflow(d)
                emit("s%d = integer(%d);" % (d, ops[0]))
            elif name in vm2c.ARITHMETIC:
                emit("{ int a = number(s%d), b = number(s%d); s%d = integer(%s); }" % (
                    d - 2, d - 1, d - 2, vm2c.ARITHMETIC[name]))
            elif name in ("DIV", "MOD"):
                f = "wrap_div" if name == "DIV" else "wrap_mod"
                emit('{ int a = number(s%d), b = number(s%d); if (b == 0) trap("division by zero");'
                     " s%d = integer(%s(a, b)); }" % (d - 2, d - 1, d - 2, f))
            elif name == "EQ":
                emit("s%d = integer(same(s%d, s%d));" % (d - 2, d - 2, d - 1))
            elif name == "PRINT":
                emit('printf("%%d\\n", number(s%d));' % (d - 1))
            elif name == "DUP":
                overflow(d)
                emit("s%d = s%d;" % (d, d - 1))
            elif name == "DROP":
                pass
            elif name == "SWAP":
                emit("{ struct value t = s%d; s%d = s%d; s%d = t; }" % (d - 1, d - 1, d - 2, d - 2))
            elif name == "OVER":
                overflow(d)
                emit("s%d = s%d;" % (d, d - 2))
            elif name == "ROT":
                emit("{ struct value t = s%d; s%d = s%d; s%d = s%d; s%d = t; }" % (
                    d - 3, d - 3, d - 2, d - 2, d - 1, d - 1))
            elif name == "LOAD":
                overflow(d)
                emit("s%d = s%d;" % (d, ops[0]))
            elif name == "STORE":
                emit("s%d = s%d;" % (ops[0], d - 1))
            elif name == "LOADM":
                emit('{ int a = number(s%d); if (a < 0 || a >= MEMORY_SIZE) trap("no such memory'
                     ' address"); s%d = memory[a]; }' % (d - 1, d - 1))
            elif name == "STOREM":
                emit('{ int a = number(s%d); if (a < 0 || a >= MEMORY_SIZE) trap("no such memory'
                     ' address"); memory[a] = s%d; }' % (d - 2, d - 1))
            elif name == "EMIT":
                emit('{ int c = number(s%d); if (c < 0 || c > 255) trap("not a character");'
                     " putchar(c); }" % (d - 1))
            elif name == "NEW":
                emit("{ int k = number(s%d); struct value v;" % (d - 1))
                spill(d - 1)
                emit("  sp = fp + %d; v = allocate(k);" % (d - 1))
                reload(d - 1)
                emit("  s%d = v; }" % (d - 1))
            elif name == "GETF":
                emit("{ int b = block(s%d); s%d = heap[field(b, number(s%d))]; }" % (
                    d - 2, d - 2, d - 1))
            elif name == "SETF":
                emit("{ int b = block(s%d); heap[field(b, number(s%d))] = s%d; }" % (
                    d - 3, d - 2, d - 1))
            elif name == "LEN":
                emit("s%d = integer(heap[block(s%d)].n);" % (d - 1, d - 1))
            elif name == "JMP":
                emit("goto A%d;" % ops[0])
                continue
            elif name == "JZ":
                emit("if (!s%d.is_ref && s%d.n == 0) goto A%d;" % (d - 1, d - 1, ops[0]))
            elif name == "CALL":
                t, k = ops
                if calls:
                    if has_new:
                        spill(d)
                    else:
                        for i in range(d - k, d):
                            emit("stack[fp + %d] = s%d;" % (i, i))
                    emit('if (fsp == FRAMES) trap("too many nested calls");')
                    emit("fsp++;")
                    emit("{ struct value r = f%d(fp + %d); fsp--;" % (t, d - k))
                    if has_new:
                        reload(d - k)
                    emit('  if (fp + %d >= STACK_SIZE) trap("stack overflow");' % (d - k))
                    emit("  s%d = r; }" % (d - k))
                    emit("goto A%d;" % nxt)
                else:
                    spill(d)
                    emit("sp = fp + %d;" % d)
                    emit('if (fsp == FRAMES) trap("too many nested calls");')
                    emit("frames[fsp].ret = %d;" % nxt)
                    emit("frames[fsp].fp = fp;")
                    emit("fsp++;")
                    emit("fp = sp - %d;" % k)
                    for i in range(k):
                        emit("s%d = s%d;" % (i, d - k + i))
                    emit("goto A%d;" % t)
                continue
            elif name == "RET":
                if calls:
                    emit("return s%d;" % (d - 1))
                else:
                    emit("{ struct value v = s%d; sp = fp; fsp--; target = frames[fsp].ret;" % (d - 1))
                    emit("  fp = frames[fsp].fp; push(v); }")
                    emit("goto dispatch;")
                continue
            else:
                raise ValueError(name)
            emit("goto A%d;" % nxt)
        return out

    if not cache:
        # -calls alone: vm2c.py's code for every instruction, but each
        # function in a C function. Made by compiling with vm2c.py and
        # cutting its output at the labels.
        return calls_only(code, depth, entries, owner, functions)
    variables = "    struct value %s;" % ", ".join("s%d" % i for i in range(top))
    parts = []
    if calls:
        for fn in sorted(functions):
            if fn == 0:
                continue
            parts.append("static struct value f%d(int fp);" % fn)
        for fn in sorted(functions):
            if fn == 0:
                continue
            parts.append("static struct value f%d(int fp) {\n%s\n%s\n}" % (
                fn, variables, "\n".join(body(fn))))
        main_body = body(0) + ["A%d: start = %d;" % (n, n),
                               '    trap("ran off the end of the program");']
        run = "static void run(void) {\n    const int fp = 0;\n%s\n%s\n}" % (
            variables, "\n".join(main_body))
    else:
        lines = []
        for fn in sorted(functions):
            lines += body(fn)
        lines.append("A%d: start = %d;" % (n, n))
        lines.append('    trap("ran off the end of the program");')
        lines.append("dispatch:")
        lines.append("    switch (target) {")
        for r in sorted(returns):
            lines.append("    case %d:" % r)
            for i in range(depth[r]):
                lines.append("        s%d = stack[fp + %d];" % (i, i))
            lines.append("        goto A%d;" % r)
        lines.append("    }")
        lines.append("    return;")
        run = "static void run(void) {\n    int target = 0;\n%s\n    (void) target;\n%s\n}" % (
            variables, "\n".join(lines))
    parts.append(run)
    return HEADER % ("-cache" + (" -calls" if calls else ""), "\n\n".join(parts), n)


HEADER = '''/* Compiled by answers/vm2c_more.py %s: verified. */

#include "runtime.h"
#undef pop
#define pop() (stack[--sp])
#define local_at(k) (fp + (k))

%s

int main(int argc, char *argv[]) {
    if (!run_options(argc, argv)) {
        fprintf(stderr, "usage: %%s [-g mark | -g copy] [-S] [-s]\\n", argv[0]);
        return 2;
    }
    code_len = %d;
    heap_init();
    atexit(report);
    run();
    return 0;
}
'''


def calls_only(code, depth, entries, owner, functions):
    """vm2c.py's output, cut into one C function for each function."""
    n = len(code)
    text = vm2c.compile_program(code, False)
    head, rest = text.split("static void run(void) {\n", 1)
    body, tail = rest.split("\n}\n\nint main", 1)
    pieces, current, label = {}, [], None
    for line in body.splitlines():
        if line.startswith("A") and ": start = " in line:
            label = int(line[1:line.index(":")])
        if line.startswith("dispatch:"):
            break
        pieces.setdefault(label, []).append(line)
    out = []
    for fn in sorted(functions):
        lines = []
        for a in functions[fn]:
            name = isa.BY_CODE[code[a]][0]
            nxt = a + 1 + NOPERANDS[code[a]]
            if name == "CALL":
                t, k = code[a + 1:a + 3]
                lines += ["A%d: start = %d;" % (a, a),
                          '    if (fsp == FRAMES) trap("too many nested calls");',
                          "    fsp++;",
                          "    { struct value r = f%d(sp - %d); fsp--; push(r); }" % (t, k),
                          "    goto A%d;" % nxt]
            elif name == "RET":
                lines += ["A%d: start = %d;" % (a, a),
                          "    { struct value v = pop(); sp = fp; return v; }"]
            elif name == "HALT" and fn != 0:
                lines += ["A%d: start = %d;" % (a, a), "    exit(0);"]
            else:
                lines += pieces[a]
        if fn == 0:
            lines += pieces[n]
            out.append("static void run(void) {\n    const int fp = 0;\n%s\n}" % "\n".join(lines))
        else:
            out.append("static struct value f%d(int fp) {\n%s\n}" % (fn, "\n".join(lines)))
    protos = ["static struct value f%d(int fp);" % fn for fn in sorted(functions) if fn != 0]
    return HEADER % ("-calls", "\n".join(protos) + "\n\n" + "\n\n".join(out), n)


def main():
    args = sys.argv[1:]
    cache = "-cache" in args
    calls = "-calls" in args
    args = [a for a in args if a not in ("-cache", "-calls")]
    if len(args) != 1:
        sys.exit("usage: vm2c_more.py [-cache] [-calls] program.vm > program.c")
    path = args[0]
    try:
        code = vmfile.read(path)
    except OSError:
        print(f"{path}: cannot open", file=sys.stderr)
        sys.exit(2)
    except vmfile.FormatError as e:
        print(f"{path}: {e}", file=sys.stderr)
        sys.exit(2)
    if not cache and not calls:
        sys.stdout.write(vm2c.compile_program(code, False))
    else:
        sys.stdout.write(compile_program(code, cache, calls))


if __name__ == "__main__":
    main()
