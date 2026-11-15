#!/usr/bin/env python3
"""
Make vm_more.c: chapter 18's vm.c with three more ways of dispatching, for
exercises 18.4 to 18.6, chosen like the others with -DDISPATCH=...

  SUBROUTINE   18.4: every instruction a C function, and the program a list
               of calls: thread[a] is the function for word a, and the loop
               calls one after another.
  SPREAD       18.5: the goto build, with each NEXT made different by an
               empty asm statement naming its line, so that the compiler
               cannot merge them into one shared jump.
  INDIRECT     18.6: Dewar's indirect threading: thread[a] is the address of
               a place that holds the label, so NEXT loads twice.

    usage: python3 build.py > vm_more.c

  and compile it with -I.. so that it finds ../ops.h.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "..", "vm.c")).read()
ops = open(os.path.join(HERE, "..", "ops.h")).read()


def change(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)


change("#define THREADED 3", "#define THREADED 3\n#define SUBROUTINE 4\n#define SPREAD 5\n#define INDIRECT 6")

# Subroutine threading: ops.h as functions. HALT must also say so to the loop.
halt = "OP(HALT) {\n    return;\n}"
assert ops.count(halt) == 1
functions = ops.replace(halt, "OP(HALT) {\n    halted_now = 1;\n    return;\n}")
change("""#else

#define OP(x)       L_##x:""", """#elif DISPATCH == SUBROUTINE

#define OP(x)       static void f_##x(void)
#define NEXT        return
#define UNKNOWN     static void f_UNKNOWN(void)

static int halted_now = 0;

""" + functions + """

static void f_RUNOFF(void) {
    trap("ran off the end of the program");
}

static void run(void) {
    static void (*table[NOPS])(void) = {
        f_HALT, f_PUSH, f_ADD, f_SUB, f_MUL, f_PRINT,
        f_JMP, f_JZ, f_DUP, f_DROP, f_SWAP, f_OVER, f_ROT, f_LT, f_EQ,
        f_LOAD, f_STORE, f_CALL, f_RET,
        f_DIV, f_MOD,
        f_AND, f_OR, f_XOR, f_LOADM, f_STOREM, f_EMIT,
        f_NEW, f_GETF, f_SETF, f_LEN,
        f_CALLI
    };
    void (**thread)(void) = malloc((code_len + 1) * sizeof *thread);
    int a;

    if (thread == NULL) {
        fprintf(stderr, "out of memory for threaded code\\n");
        exit(2);
    }
    for (a = 0; a < code_len; a++)
        thread[a] = code[a] >= 0 && code[a] < NOPS ? table[code[a]] : f_UNKNOWN;
    thread[code_len] = f_RUNOFF;
    while (!halted_now) {
        start = pc;
        thread[pc++]();
    }
}

#else

#define OP(x)       L_##x:""")

# SPREAD: the goto NEXT, made different at every use.
change("""#if DISPATCH == GOTO
#define NEXT \\""", """#if DISPATCH == GOTO || DISPATCH == SPREAD
#if DISPATCH == SPREAD
#define DIFFERENT __asm__ volatile("// next %0" :: "i"(__LINE__))
#else
#define DIFFERENT
#endif
#define NEXT \\""")
change("""        if (op < 0 || op >= NOPS) \\
            goto L_UNKNOWN; \\
        goto *table[op]; \\""", """        if (op < 0 || op >= NOPS) \\
            goto L_UNKNOWN; \\
        DIFFERENT; \\
        goto *table[op]; \\""")

# INDIRECT: one more load.
change("""#else
#define NEXT \\
    do { \\
        start = pc; \\
        goto *thread[pc++]; \\
    } while (0)
#endif""", """#elif DISPATCH == INDIRECT
#define NEXT \\
    do { \\
        start = pc; \\
        goto **thread[pc++]; \\
    } while (0)
#else
#define NEXT \\
    do { \\
        start = pc; \\
        goto *thread[pc++]; \\
    } while (0)
#endif""")
change("""#if DISPATCH == THREADED
    /*""", """#if DISPATCH == INDIRECT
    /* Dewar: each word points at the place in table that holds its label. */
    static void *unknown = &&L_UNKNOWN, *runoff = &&L_RUNOFF;
    void ***thread = malloc((code_len + 1) * sizeof (void **));
    int a;

    if (thread == NULL) {
        fprintf(stderr, "out of memory for threaded code\\n");
        exit(2);
    }
    for (a = 0; a < code_len; a++)
        thread[a] = code[a] >= 0 && code[a] < NOPS ? &table[code[a]] : &unknown;
    thread[code_len] = &runoff;
    (void) op;
#endif
#if DISPATCH == THREADED
    /*""")
change("""#if DISPATCH == THREADED
L_RUNOFF:""", """#if DISPATCH == THREADED || DISPATCH == INDIRECT
L_RUNOFF:""")
print(s, end="")
