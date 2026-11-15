#!/usr/bin/env python3
"""
Make the machine of exercises 21.1 and 21.2, in a folder of its own:

    python3 build.py folder

  folder/vm.c, folder/loop.h   built with -DKINDS, -DROOM, or both

-DKINDS (exercise 1): after the verifier accepts a program, kinds() works
out, for every value in every frame at every instruction, whether it is
certainly a number, certainly a reference, or either. Where ADD, SUB,
MUL, AND, OR, XOR or LT is certain to be given two numbers, the verified
run loop's threaded code gets the label of a copy of it that reads the
numbers without looking at their tags. -K prints how many were found.

-DROOM (exercise 2): the verified run loop's push no longer checks for
overflow. Instead, every CALL checks that the stack has room for the
deepest the called function's frame can get, which the verifier knows.

Both are only for the verified run loop; a program that does not verify
runs with every check, as before.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)


def patch(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


KINDS = r"""
#if defined KINDS || defined ROOM
static int *vdepth, *vowner;        /* kept from the verifier */
#endif

#ifdef KINDS
/*
 * Kinds: 1 a number, 2 a reference, 3 either; 0 nothing yet. Joining
 * two is or-ing them. For every instruction reached, the kind of each
 * value in the frame, joined over every path there; a function's
 * arguments are joined over every call, and what a CALL leaves is what
 * the function's RETs return, joined. Repeated until nothing changes.
 */
static unsigned char *fast;
static int kinds_fast = 0, kinds_arith = 0;

static int arith(int op) {
    return op == ADD || op == SUB || op == MUL || op == AND || op == OR || op == XOR ||
           op == LT;
}

static int join_into(unsigned char *state, char *reached, int b, const unsigned char *s,
                     int d) {
    unsigned char *to = state + (size_t) b * STACK_SIZE;
    int k, changed = !reached[b];

    reached[b] = 1;
    for (k = 0; k < d; k++) {
        unsigned char j = to[k] | s[k];
        if (j != to[k]) {
            to[k] = j;
            changed = 1;
        }
    }
    return changed;
}

static void kinds(void) {
    unsigned char *state = calloc((size_t) (code_len + 1) * STACK_SIZE, 1);
    unsigned char *ret = calloc(code_len + 1, 1);
    char *reached = calloc(code_len + 1, 1);
    unsigned char s[STACK_SIZE + 3];
    int a, changed = 1;

    fast = calloc(code_len + 1, 1);
    if (!state || !ret || !reached || !fast) {
        fprintf(stderr, "out of memory for the verifier\n");
        exit(2);
    }
    reached[0] = 1;
    while (changed) {
        changed = 0;
        for (a = 0; a < code_len; a++) {
            int op = code[a], d = vdepth[a], next, t, n;
            unsigned char x;

            if (!reached[a])
                continue;
            memcpy(s, state + (size_t) a * STACK_SIZE, d);
            next = a + 1 + noperands[op];
            switch (op) {
            case HALT:
                continue;
            case PUSH:
                s[d++] = 1;
                break;
            case ADD: case SUB: case MUL: case DIV: case MOD: case AND: case OR:
            case XOR: case LT: case EQ:
                d -= 2;
                s[d++] = 1;
                break;
            case LEN:
                s[d - 1] = 1;
                break;
            case NEW:
                s[d - 1] = 2;
                break;
            case LOADM:
                s[d - 1] = 3;
                break;
            case GETF:
                d -= 2;
                s[d++] = 3;
                break;
            case SETF:
                d -= 3;
                break;
            case STOREM:
                d -= 2;
                break;
            case PRINT: case EMIT: case DROP: case JZ:
                d -= 1;
                break;
            case DUP:
                s[d] = s[d - 1];
                d++;
                break;
            case SWAP:
                x = s[d - 1]; s[d - 1] = s[d - 2]; s[d - 2] = x;
                break;
            case OVER:
                s[d] = s[d - 2];
                d++;
                break;
            case ROT:
                x = s[d - 3]; s[d - 3] = s[d - 2]; s[d - 2] = s[d - 1]; s[d - 1] = x;
                break;
            case LOAD:
                s[d] = s[code[a + 1]];
                d++;
                break;
            case STORE:
                s[code[a + 1]] = s[d - 1];
                d--;
                break;
            case CALL:
                t = code[a + 1];
                n = code[a + 2];
                changed |= join_into(state, reached, t, s + d - n, n);
                if (ret[t] == 0)
                    continue;           /* nothing known of what it returns yet */
                d -= n;
                s[d++] = ret[t];
                break;
            case RET:
                x = ret[vowner[a]] | s[d - 1];
                if (x != ret[vowner[a]]) {
                    ret[vowner[a]] = x;
                    changed = 1;
                }
                continue;
            case JMP:
                changed |= join_into(state, reached, code[a + 1], s, d);
                continue;
            }
            if (op == JZ)
                changed |= join_into(state, reached, code[a + 1], s, d);
            changed |= join_into(state, reached, next, s, d);
        }
    }
    for (a = 0; a < code_len; a++)
        if (reached[a] && arith(code[a])) {
            const unsigned char *in = state + (size_t) a * STACK_SIZE;
            int d = vdepth[a];
            kinds_arith++;
            if (in[d - 1] == 1 && in[d - 2] == 1) {
                fast[a] = 1;
                kinds_fast++;
            }
        }
    free(state);
    free(ret);
    free(reached);
}
#endif

#ifdef ROOM
/* For each function, by its entry: the deepest its frame can get. */
static int *room;

static void rooms(void) {
    int a;
    room = calloc(code_len + 1, sizeof (int));
    if (room == NULL) {
        fprintf(stderr, "out of memory for the verifier\n");
        exit(2);
    }
    for (a = 0; a < code_len; a++)
        if (vdepth[a] >= 0 && vdepth[a] > room[vowner[a]])
            room[vowner[a]] = vdepth[a];
}
#endif
"""

FAST = r"""
#ifdef FAST_PATHS
/* Exercise 1: two values known to be numbers, so no tag is looked at. */
L_ADD_N: { struct value w = pop(), v = pop(); push_int(wrap_add(v.n, w.n)); NEXT; }
L_SUB_N: { struct value w = pop(), v = pop(); push_int(wrap_sub(v.n, w.n)); NEXT; }
L_MUL_N: { struct value w = pop(), v = pop(); push_int(wrap_mul(v.n, w.n)); NEXT; }
L_AND_N: { struct value w = pop(), v = pop(); push_int(v.n & w.n); NEXT; }
L_OR_N:  { struct value w = pop(), v = pop(); push_int(v.n | w.n); NEXT; }
L_XOR_N: { struct value w = pop(), v = pop(); push_int(v.n ^ w.n); NEXT; }
L_LT_N:  { struct value w = pop(), v = pop(); push_int(v.n < w.n); NEXT; }
#endif
#ifdef ROOM_PATHS
/* Exercise 2: room for the whole frame of the function called. */
L_CALL_ROOM: {
    int t = code[pc], n = code[pc + 1];
    if (sp - n + room[t] > STACK_SIZE)
        trap("stack overflow");
    goto L_CALL;
}
#endif
"""

SWAP_IN = r"""
#ifdef FAST_PATHS
    for (a = 0; a < code_len; a++)
        if (fast[a]) {
            switch (code[a]) {
            case ADD: thread[a] = &&L_ADD_N; break;
            case SUB: thread[a] = &&L_SUB_N; break;
            case MUL: thread[a] = &&L_MUL_N; break;
            case AND: thread[a] = &&L_AND_N; break;
            case OR:  thread[a] = &&L_OR_N; break;
            case XOR: thread[a] = &&L_XOR_N; break;
            case LT:  thread[a] = &&L_LT_N; break;
            }
        }
#endif
#ifdef ROOM_PATHS
    for (a = 0; a < code_len; a++)
        if (vdepth[a] >= 0 && code[a] == CALL)
            thread[a] = &&L_CALL_ROOM;
#endif
"""


def main():
    folder = sys.argv[1]
    loop = open(os.path.join(CHAPTER, "loop.h")).read()
    loop = patch(loop, "    thread[code_len] = &&L_RUNOFF;\n",
                 "    thread[code_len] = &&L_RUNOFF;\n" + SWAP_IN)
    loop = patch(loop, '#include "ops.h"\n', '#include "ops.h"\n' + FAST)
    open(os.path.join(folder, "loop.h"), "w").write(loop)
    ops = os.path.join(folder, "ops.h")
    if not os.path.exists(ops):
        os.symlink(os.path.join(CHAPTER, "ops.h"), ops)

    c = open(os.path.join(CHAPTER, "vm.c")).read()
    # The two run loops are defined before the verifier; declare what
    # the second needs, and define it after.
    c = patch(c, "#define RUN run_checked\n", """#ifdef KINDS
static unsigned char *fast;
#endif
#ifdef ROOM
static int *room;
static int *vdepth;
#endif
#define RUN run_checked
""")
    c = patch(c, """#define local()     local_verified()
""", """#define local()     local_verified()
#ifdef KINDS
#define FAST_PATHS
#endif
#ifdef ROOM
/* The stack's room is checked at each CALL instead. */
static inline void push_verified(struct value v) {
    stack[sp++] = v;
}
static inline void push_int_verified(int n) {
    push_verified(integer(n));
}
#define push(v)     push_verified(v)
#define push_int(n) push_int_verified(n)
#define ROOM_PATHS
#endif
""")
    c = patch(c, """#undef pop
#undef operand""", """#undef FAST_PATHS
#undef ROOM_PATHS
#ifdef ROOM
#undef push
#undef push_int
#endif
#undef pop
#undef operand""")
    kinds = KINDS.replace("static unsigned char *fast;\n", "") \
                 .replace("static int *room;\n", "") \
                 .replace("static int *vdepth, *vowner;", "static int *vowner;")
    kinds = kinds.replace("#if defined KINDS || defined ROOM\nstatic int *vowner;",
                          "#if defined KINDS || defined ROOM\n#ifndef ROOM\nstatic int *vdepth;\n#endif\nstatic int *vowner;")
    c = patch(c, "static char why[200];\n", "static char why[200];\n" + kinds)
    c = patch(c, """    free(begins);
    free(depth);
    free(owner);""", """    free(begins);
#if defined KINDS || defined ROOM
    vdepth = depth;
    vowner = owner;
#else
    free(depth);
    free(owner);
#endif""")
    c = patch(c, """    verified = !checked && verify();
""", """    verified = !checked && verify();
    (void) show_kinds;
#ifdef KINDS
    if (verified)
        kinds();
    if (show_kinds)
        fprintf(stderr, "kinds: %d of %d arithmetic instructions given two numbers\\n",
                verified ? kinds_fast : 0, verified ? kinds_arith : 0);
#endif
#ifdef ROOM
    if (verified)
        rooms();
#endif
""")
    c = patch(c, "    int i, strict = 0, verbose = 0, checked = 0, verified;\n",
              "    int i, strict = 0, verbose = 0, checked = 0, verified, show_kinds = 0;\n")
    c = patch(c, """        } else if (strcmp(argv[i], "-C") == 0) {
            checked = 1;""", """        } else if (strcmp(argv[i], "-C") == 0) {
            checked = 1;
        } else if (strcmp(argv[i], "-K") == 0) {
            show_kinds = 1;""")
    open(os.path.join(folder, "vm.c"), "w").write(c)


main()
