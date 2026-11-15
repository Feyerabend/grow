/*
 * Verification by type checking, JVMS 4.10.1.
 *
 * The compiler has written down, in each method's StackMapTable, the types
 * of the locals and of the operand stack at every place where paths of the
 * code meet: each branch target, and each instruction after an unconditional
 * branch. The verifier goes through the code once, in order, keeping the
 * current types. At an instruction with a frame of the table, the types that
 * flow into it must be assignable to the frame's, and the frame's become the
 * current ones. A branch is checked against the frame at its target. So no
 * instruction is looked at twice, and nothing is merged: the frames say it
 * all, and the verifier only checks that they are true.
 *
 * The rules are the specification's Prolog clauses, written in C, for the
 * part of the machine this one runs. What it cannot check, it refuses:
 * long, float, double, objects, exception handlers, and any assignment
 * between classes whose relation it would have to load a class to know.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "jvm.h"

int verify_trace;

const char *const opname[202] = {
    "nop", "aconst_null", "iconst_m1", "iconst_0", "iconst_1", "iconst_2",
    "iconst_3", "iconst_4", "iconst_5", "lconst_0", "lconst_1", "fconst_0",
    "fconst_1", "fconst_2", "dconst_0", "dconst_1", "bipush", "sipush", "ldc",
    "ldc_w", "ldc2_w", "iload", "lload", "fload", "dload", "aload", "iload_0",
    "iload_1", "iload_2", "iload_3", "lload_0", "lload_1", "lload_2",
    "lload_3", "fload_0", "fload_1", "fload_2", "fload_3", "dload_0",
    "dload_1", "dload_2", "dload_3", "aload_0", "aload_1", "aload_2",
    "aload_3", "iaload", "laload", "faload", "daload", "aaload", "baload",
    "caload", "saload", "istore", "lstore", "fstore", "dstore", "astore",
    "istore_0", "istore_1", "istore_2", "istore_3", "lstore_0", "lstore_1",
    "lstore_2", "lstore_3", "fstore_0", "fstore_1", "fstore_2", "fstore_3",
    "dstore_0", "dstore_1", "dstore_2", "dstore_3", "astore_0", "astore_1",
    "astore_2", "astore_3", "iastore", "lastore", "fastore", "dastore",
    "aastore", "bastore", "castore", "sastore", "pop", "pop2", "dup",
    "dup_x1", "dup_x2", "dup2", "dup2_x1", "dup2_x2", "swap", "iadd", "ladd",
    "fadd", "dadd", "isub", "lsub", "fsub", "dsub", "imul", "lmul", "fmul",
    "dmul", "idiv", "ldiv", "fdiv", "ddiv", "irem", "lrem", "frem", "drem",
    "ineg", "lneg", "fneg", "dneg", "ishl", "lshl", "ishr", "lshr", "iushr",
    "lushr", "iand", "land", "ior", "lor", "ixor", "lxor", "iinc", "i2l",
    "i2f", "i2d", "l2i", "l2f", "l2d", "f2i", "f2l", "f2d", "d2i", "d2l",
    "d2f", "i2b", "i2c", "i2s", "lcmp", "fcmpl", "fcmpg", "dcmpl", "dcmpg",
    "ifeq", "ifne", "iflt", "ifge", "ifgt", "ifle", "if_icmpeq", "if_icmpne",
    "if_icmplt", "if_icmpge", "if_icmpgt", "if_icmple", "if_acmpeq",
    "if_acmpne", "goto", "jsr", "ret", "tableswitch", "lookupswitch",
    "ireturn", "lreturn", "freturn", "dreturn", "areturn", "return",
    "getstatic", "putstatic", "getfield", "putfield", "invokevirtual",
    "invokespecial", "invokestatic", "invokeinterface", "invokedynamic",
    "new", "newarray", "anewarray", "arraylength", "athrow", "checkcast",
    "instanceof", "monitorenter", "monitorexit", "wide", "multianewarray",
    "ifnull", "ifnonnull", "goto_w", "jsr_w"
};

/* The length of the instruction at pc, or 0 if it does not fit in the code
 * or is not an instruction (4.9.1). */
int instruction_length(const uint8_t *code, uint32_t length, uint32_t pc) {
    unsigned op = code[pc];
    int n;
    if (op > 201)
        return 0;
    switch (op) {
    case 16: case 18: case 21: case 22: case 23: case 24: case 25:
    case 54: case 55: case 56: case 57: case 58: case 169: case 188:
        n = 2; break;
    case 17: case 19: case 20: case 132: case 178: case 179: case 180:
    case 181: case 182: case 183: case 184: case 187: case 189: case 192:
    case 193: case 198: case 199:
        n = 3; break;
    case 197: n = 4; break;
    case 185: case 186: case 200: case 201: n = 5; break;
    case 196:
        if (pc + 1 >= length)
            return 0;
        n = code[pc + 1] == 132 ? 6 : 4;
        break;
    case 170: case 171: {
        uint32_t p = (pc + 4) & ~3u;            /* past the padding */
        if (p + 12 > length)
            return 0;
        int32_t a = (int32_t)((uint32_t)code[p + 4] << 24 | (uint32_t)code[p + 5] << 16 |
                              (uint32_t)code[p + 6] << 8 | code[p + 7]);
        int32_t b = (int32_t)((uint32_t)code[p + 8] << 24 | (uint32_t)code[p + 9] << 16 |
                              (uint32_t)code[p + 10] << 8 | code[p + 11]);
        int64_t entries = op == 170 ? (int64_t)b - a + 1 : a;
        if (entries < 0 || entries > 65536)
            return 0;
        n = (int)(p - pc + 12 + (op == 170 ? 4 : 8) * entries - (op == 170 ? 0 : 4));
        break;
    }
    default:
        if (op >= 153 && op <= 168)
            n = 3;
        else
            n = 1;
    }
    return pc + n <= length ? n : 0;
}

/* Verification types, 4.10.1.2. A type is a number: a tag in the low four
 * bits, and for a class or array type the index of its name above them. */
typedef uint32_t Type;
enum { TOP, INT, FLOAT, DOUBLE, LONG, NUL, UTHIS, REF, UNINIT, REFERENCE };
#define TAG(t) ((t) & 15)
#define REFTYPE(i) (REF | (Type)(i) << 4)
#define NAME(t) (names[(t) >> 4])

static const char **names;  /* class names, and array descriptors */
static int nnames;

static Type ref(const char *name, size_t len) {
    for (int i = 0; i < nnames; i++)
        if (strlen(names[i]) == len && !strncmp(names[i], name, len))
            return REFTYPE(i);
    names = realloc(names, (nnames + 1) * sizeof *names);
    names[nnames] = strndup(name, len);
    return REFTYPE(nnames++);
}

/* What the verifier knows of classes without loading any: the class being
 * checked and its superclass, and a few of the platform's. */
static Class *current;
static const char *const supers[][2] = {
    { "java/lang/String", "java/lang/Object" },
    { "java/io/PrintStream", "java/io/FilterOutputStream" },
    { "java/io/FilterOutputStream", "java/io/OutputStream" },
    { "java/io/OutputStream", "java/lang/Object" },
};
static const char *const interfaces[] = {
    "java/lang/Cloneable", "java/io/Serializable", "java/lang/CharSequence",
    "java/lang/Comparable", "java/lang/Runnable", "java/lang/AutoCloseable",
    "java/io/Closeable", "java/io/Flushable", "java/lang/Appendable",
};

static const char *superclass(const char *name) {
    if (!strcmp(name, current->name))
        return current->super;
    for (size_t i = 0; i < sizeof supers / sizeof *supers; i++)
        if (!strcmp(name, supers[i][0]))
            return supers[i][1];
    return NULL;
}

static int is_interface(const char *name) {
    for (size_t i = 0; i < sizeof interfaces / sizeof *interfaces; i++)
        if (!strcmp(name, interfaces[i]))
            return 1;
    return 0;
}

static char unknown_class[200];

/* isJavaAssignable for class and array names: 1, 0, or -1 if the answer
 * would need a class loaded. */
static int name_assignable(const char *x, const char *y) {
    if (!strcmp(x, y) || !strcmp(y, "java/lang/Object"))
        return 1;
    if (x[0] == '[') {
        if (!strcmp(y, "java/lang/Cloneable") || !strcmp(y, "java/io/Serializable"))
            return 1;
        if (y[0] != '[')
            return 0;
        x++, y++;
        /* arrays of primitives: identity; of references: covariant */
        if ((x[0] == 'L' || x[0] == '[') && (y[0] == 'L' || y[0] == '[')) {
            char a[256], b[256];
            snprintf(a, sizeof a, "%.*s", (int)(x[0] == 'L' ? strlen(x) - 2 : strlen(x)), x + (x[0] == 'L'));
            snprintf(b, sizeof b, "%.*s", (int)(y[0] == 'L' ? strlen(y) - 2 : strlen(y)), y + (y[0] == 'L'));
            return name_assignable(a, b);
        }
        return 0;
    }
    if (y[0] == '[')
        return 0;
    if (is_interface(y))        /* "interfaces are treated like Object" */
        return 1;
    for (const char *s = superclass(x); s; s = superclass(s))
        if (!strcmp(s, y))
            return 1;
    for (const char *s = x; s; s = superclass(s))
        if (!strcmp(s, "java/lang/Object"))
            return 0;           /* the whole chain is known, and y is not on it */
    snprintf(unknown_class, sizeof unknown_class, "%s", x);
    return -1;
}

/* isAssignable(From, To), 4.10.1.2 */
static int assignable(Type from, Type to) {
    if (from == to || to == TOP)
        return 1;
    if (to == REFERENCE)
        return TAG(from) == REF || from == NUL || from == UTHIS || TAG(from) == UNINIT;
    if (TAG(to) == REF) {
        if (from == NUL)
            return 1;
        if (TAG(from) == REF)
            return name_assignable(NAME(from), NAME(to));
    }
    return 0;
}

typedef struct {
    Type *locals, *stack;
    int sp;
    int uninit;     /* flagThisUninit */
} Frame;

/* The method being checked, for the messages. */
static Method *method;
static uint32_t at;

static int refuse(const char *fmt, const char *detail) {
    char what[200];
    snprintf(what, sizeof what, fmt, detail);
    snprintf(jvm_error, sizeof jvm_error,
             "java.lang.VerifyError: %s, in %s.%s%s at %u",
             what, current->name, method->name, method->descriptor, at);
    return 0;
}

static int unsupported(const char *fmt, const char *detail) {
    char what[200];
    snprintf(what, sizeof what, fmt, detail);
    snprintf(jvm_error, sizeof jvm_error,
             "cannot check: %s, in %s.%s%s at %u",
             what, current->name, method->name, method->descriptor, at);
    return 0;
}

static int assign_or_refuse(Type from, Type to) {
    int a = assignable(from, to);
    if (a < 0)
        return unsupported("would load class %s", unknown_class);
    return a;
}

static void show_types(const Type *t, int n) {
    static const char *const tag[] = { "top", "int", "float", "double",
        "long", "null", "uninitializedThis" };
    for (int i = 0; i < n; i++)
        printf("%s%s", i ? ", " : "", TAG(t[i]) == REF ? NAME(t[i]) : tag[TAG(t[i])]);
}

/* For -f: a frame, as the verifier holds it, without the tops at the end
 * of the locals. */
static void show(const Frame *f) {
    int n = method->max_locals;
    while (n > 0 && f->locals[n - 1] == TOP)
        n--;
    printf("  %4u  locals [", at);
    show_types(f->locals, n);
    printf("]  stack [");
    show_types(f->stack, f->sp);
    printf("]%s\n", f->uninit ? "  this uninitialised" : "");
}

/* A field descriptor as a verification type: booleans, bytes, chars and
 * shorts are ints to the verifier. 0 if it cannot be checked here. */
static int field_type(const char *d, const char **end, Type *t) {
    const char *s = d;
    while (*s == '[')
        s++;
    if (*s == 'L') {
        const char *semi = strchr(s, ';');
        if (!semi)
            return 0;
        *end = semi + 1;
        *t = d[0] == '[' ? ref(d, *end - d) : ref(d + 1, semi - d - 1);
        return 1;
    }
    if (!strchr("BCDFIJSZ", *s) || !*s)
        return 0;
    *end = s + 1;
    if (d[0] == '[') {
        *t = ref(d, *end - d);
        return 1;
    }
    if (strchr("BCISZ", *s)) {
        *t = INT;
        return 1;
    }
    return 0;           /* long, float, double */
}

static Frame new_frame(const Method *m) {
    Frame f = { calloc(m->max_locals + 1, sizeof(Type)),
                calloc(m->max_stack + 1, sizeof(Type)), 0, 0 };
    return f;
}

static void copy_frame(Frame *to, const Frame *from) {
    memcpy(to->locals, from->locals, method->max_locals * sizeof(Type));
    memcpy(to->stack, from->stack, from->sp * sizeof(Type));
    to->sp = from->sp;
    to->uninit = from->uninit;
}

/* frameIsAssignable, 4.10.1.4 */
static int frame_assignable(const Frame *a, const Frame *b) {
    if (a->sp != b->sp)
        return refuse("stack of %s values, where the frame has another number",
                      a->sp == 0 ? "no" : "some");
    for (int i = 0; i < method->max_locals; i++) {
        int ok = assign_or_refuse(a->locals[i], b->locals[i]);
        if (ok <= 0)
            return ok == 0 ? refuse("a local does not match the frame", NULL) : 0;
    }
    for (int i = 0; i < a->sp; i++) {
        int ok = assign_or_refuse(a->stack[i], b->stack[i]);
        if (ok <= 0)
            return ok == 0 ? refuse("the stack does not match the frame", NULL) : 0;
    }
    if (a->uninit && !b->uninit)
        return refuse("this is not yet initialised, as the frame says it is", NULL);
    return 1;
}

/* The frames of the method's StackMapTable, 4.7.4. */
typedef struct {
    uint32_t offset;
    Frame frame;
} MapFrame;

static int read_type(const uint8_t **p, const uint8_t *end, Type *t) {
    if (*p >= end)
        return refuse("StackMapTable is truncated", NULL);
    unsigned tag = *(*p)++;
    switch (tag) {
    case 0: *t = TOP; return 1;
    case 1: *t = INT; return 1;
    case 5: *t = NUL; return 1;
    case 6: *t = UTHIS; return 1;
    case 7: {
        if (*p + 2 > end)
            return refuse("StackMapTable is truncated", NULL);
        unsigned i = (*p)[0] << 8 | (*p)[1];
        *p += 2;
        const char *name = cp_class_name(current, i);
        if (!name)
            return refuse("bad constant pool index in StackMapTable", NULL);
        *t = ref(name, strlen(name));
        return 1;
    }
    case 2: case 3: case 4:
        return unsupported("%s in a stack map frame",
                           tag == 2 ? "float" : tag == 3 ? "double" : "long");
    case 8:
        return unsupported("an uninitialised object in a stack map frame", NULL);
    default:
        return refuse("bad verification type in StackMapTable", NULL);
    }
}

static int read_frames(const Frame *initial, int nargs, MapFrame **out, int *count) {
    const Method *m = method;
    const uint8_t *p = m->stackmap, *end = p + m->stackmap_length;
    MapFrame *frames = calloc(m->frames + 1, sizeof *frames);
    const Frame *prev = initial;
    int nlocals = nargs;                /* locals the previous frame declares */
    int64_t offset = -1;
    for (int i = 0; i < m->frames; i++) {
        if (p >= end)
            return refuse("StackMapTable is truncated", NULL);
        unsigned type = *p++, delta;
        Frame f = new_frame(m);
        copy_frame(&f, prev);
        f.sp = 0;
        if (type < 64) {
            delta = type;
        } else if (type < 128) {
            delta = type - 64;
            if (!read_type(&p, end, &f.stack[0]))
                return 0;
            f.sp = 1;
        } else if (type < 247) {
            return refuse("reserved frame type in StackMapTable", NULL);
        } else {
            if (p + 2 > end)
                return refuse("StackMapTable is truncated", NULL);
            delta = p[0] << 8 | p[1];
            p += 2;
            if (type == 247) {
                if (!read_type(&p, end, &f.stack[0]))
                    return 0;
                f.sp = 1;
            } else if (type <= 250) {           /* chop */
                int k = 251 - type;
                if (k > nlocals)
                    return refuse("chop frame removes more locals than there are", NULL);
                nlocals -= k;
                for (int j = nlocals; j < m->max_locals; j++)
                    f.locals[j] = TOP;
            } else if (type == 251) {
            } else if (type <= 254) {           /* append */
                int k = type - 251;
                if (nlocals + k > m->max_locals)
                    return refuse("more locals in a frame than max_locals", NULL);
                for (int j = 0; j < k; j++)
                    if (!read_type(&p, end, &f.locals[nlocals++]))
                        return 0;
            } else {                            /* full_frame */
                if (p + 2 > end)
                    return refuse("StackMapTable is truncated", NULL);
                unsigned n = p[0] << 8 | p[1];
                p += 2;
                if (n > m->max_locals)
                    return refuse("more locals in a frame than max_locals", NULL);
                for (int j = 0; j < m->max_locals; j++)
                    f.locals[j] = TOP;
                for (unsigned j = 0; j < n; j++)
                    if (!read_type(&p, end, &f.locals[j]))
                        return 0;
                nlocals = n;
                if (p + 2 > end)
                    return refuse("StackMapTable is truncated", NULL);
                n = p[0] << 8 | p[1];
                p += 2;
                if (n > m->max_stack)
                    return refuse("more stack in a frame than max_stack", NULL);
                for (unsigned j = 0; j < n; j++)
                    if (!read_type(&p, end, &f.stack[j]))
                        return 0;
                f.sp = n;
            }
        }
        if (f.sp > m->max_stack)
            return refuse("more stack in a frame than max_stack", NULL);
        f.uninit = 0;
        for (int j = 0; j < m->max_locals; j++)
            if (f.locals[j] == UTHIS)
                f.uninit = 1;
        offset = offset < 0 ? delta : offset + delta + 1;
        frames[i].offset = (uint32_t)offset;
        frames[i].frame = f;
        prev = &frames[i].frame;
    }
    if (p != end)
        return refuse("bytes left over in StackMapTable", NULL);
    *out = frames;
    *count = m->frames;
    return 1;
}

/* The checks on the operand stack: popMatchingType and pushOperandStack. */
static Frame cur;

static int pop(Type expected, Type *actual) {
    if (cur.sp == 0)
        return refuse("operand stack underflow", NULL);
    Type t = cur.stack[--cur.sp];
    int ok = assign_or_refuse(t, expected);
    if (ok < 0)
        return 0;
    if (!ok)
        return refuse("bad type on operand stack", NULL);
    if (actual)
        *actual = t;
    return 1;
}

static int pop1(Type *t) {         /* popCategory1: any type but top */
    if (cur.sp == 0)
        return refuse("operand stack underflow", NULL);
    *t = cur.stack[--cur.sp];
    if (*t == TOP)
        return refuse("bad type on operand stack", NULL);
    return 1;
}

static int push(Type t) {
    if (cur.sp >= method->max_stack)
        return refuse("operand stack overflow", NULL);
    cur.stack[cur.sp++] = t;
    return 1;
}

static int pushes(int n, const Type *t) {
    for (int i = 0; i < n; i++)
        if (!push(t[i]))
            return 0;
    return 1;
}

static const char *return_descriptor(const char *d) {
    return strchr(d, ')') + 1;
}

/* Pop a method's arguments, last first, as its descriptor says. */
static int pop_arguments(const char *d) {
    Type args[256];
    int n = 0;
    for (d++; *d != ')'; ) {
        const char *end;
        if (!field_type(d, &end, &args[n]))
            return unsupported("an argument of type %s", d);
        if (++n == 256)
            return refuse("too many arguments", NULL);
        d = end;
    }
    while (n > 0)
        if (!pop(args[--n], NULL))
            return 0;
    return 1;
}

static int push_result(const char *d) {
    const char *r = return_descriptor(d), *end;
    Type t;
    if (*r == 'V')
        return 1;
    if (!field_type(r, &end, &t))
        return unsupported("a result of type %s", r);
    return push(t);
}

static MapFrame *frames;
static int nframes;
static int *frame_at;           /* per offset: the index of its frame, or -1 */

/* targetIsTypeSafe: the target has a frame, and the types now are
 * assignable to it. */
static int target(int64_t to) {
    if (to < 0 || to >= method->code_length || frame_at[to] == -2)
        return refuse("branch to the middle of an instruction or out of the code", NULL);
    if (frame_at[to] < 0)
        return refuse("expecting a stack map frame at the branch target", NULL);
    return frame_assignable(&cur, &frames[frame_at[to]].frame);
}

static int load(int index, Type expected) {
    if (index >= method->max_locals)
        return refuse("local variable index is not below max_locals", NULL);
    Type t = cur.locals[index];
    int ok = assign_or_refuse(t, expected);
    if (ok <= 0)
        return ok == 0 ? refuse("bad local variable type", NULL) : 0;
    return push(t);
}

static int store(int index, Type expected) {
    Type t;
    if (index >= method->max_locals)
        return refuse("local variable index is not below max_locals", NULL);
    if (!pop(expected, &t))
        return 0;
    cur.locals[index] = t;
    return 1;
}

static int32_t s4(const uint8_t *p) {
    return (int32_t)((uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 | (uint32_t)p[2] << 8 | p[3]);
}

/* One instruction: instructionIsTypeSafe. Sets *goes_on to 0 for an
 * unconditional branch, after which a frame must follow. */
static int instruction(const uint8_t *code, uint32_t pc, int *goes_on) {
    unsigned op = code[pc];
    /* instruction_length has made sure that the operands are there */
    int u2 = pc + 2 < method->code_length ? code[pc + 1] << 8 | code[pc + 2] : 0;
    int16_t s2 = (int16_t)u2;
    Type a, b, c, d;
    const char *cls, *name, *desc, *end;
    *goes_on = 1;
    Type int_array = ref("[I", 2);
    switch (op) {
    case 0:                                             /* nop */
        return 1;
    case 1:                                             /* aconst_null */
        return push(NUL);
    case 2: case 3: case 4: case 5: case 6: case 7: case 8:
    case 16: case 17:                                   /* iconst, bipush, sipush */
        return push(INT);
    case 18: case 19: {                                 /* ldc, ldc_w */
        int i = op == 18 ? code[pc + 1] : u2;
        if (i < 1 || i >= current->count)
            return refuse("bad constant pool index", NULL);
        int tag = current->pool[i].tag;
        if (tag == CP_INTEGER)
            return push(INT);
        if (tag == CP_STRING)
            return push(ref("java/lang/String", 16));
        if (tag == CP_FLOAT || tag == CP_CLASS || tag == CP_METHOD_TYPE ||
            tag == CP_METHOD_HANDLE || tag == CP_DYNAMIC)
            return unsupported("ldc of a constant of this kind", NULL);
        return refuse("ldc of a constant that cannot be loaded", NULL);
    }
    case 21: return load(code[pc + 1], INT);            /* iload */
    case 25: return load(code[pc + 1], REFERENCE);      /* aload */
    case 26: case 27: case 28: case 29: return load(op - 26, INT);
    case 42: case 43: case 44: case 45: return load(op - 42, REFERENCE);
    case 46:                                            /* iaload */
        return pop(INT, NULL) && pop(int_array, NULL) && push(INT);
    case 54: return store(code[pc + 1], INT);           /* istore */
    case 58: return store(code[pc + 1], REFERENCE);     /* astore */
    case 59: case 60: case 61: case 62: return store(op - 59, INT);
    case 75: case 76: case 77: case 78: return store(op - 75, REFERENCE);
    case 79:                                            /* iastore */
        return pop(INT, NULL) && pop(INT, NULL) && pop(int_array, NULL);
    case 87: return pop1(&a);                           /* pop */
    case 88: return pop1(&a) && pop1(&b);               /* pop2, form 1 */
    case 89: return pop1(&a) && push(a) && push(a);     /* dup */
    case 90:                                            /* dup_x1 */
        return pop1(&a) && pop1(&b) && pushes(3, (Type[]){ a, b, a });
    case 91:                                            /* dup_x2, form 1 */
        return pop1(&a) && pop1(&b) && pop1(&c) && pushes(4, (Type[]){ a, c, b, a });
    case 92:                                            /* dup2, form 1 */
        return pop1(&a) && pop1(&b) && pushes(4, (Type[]){ b, a, b, a });
    case 93:                                            /* dup2_x1, form 1 */
        return pop1(&a) && pop1(&b) && pop1(&c) && pushes(5, (Type[]){ b, a, c, b, a });
    case 94:                                            /* dup2_x2, form 1 */
        return pop1(&a) && pop1(&b) && pop1(&c) && pop1(&d) &&
               pushes(6, (Type[]){ b, a, d, c, b, a });
    case 95: return pop1(&a) && pop1(&b) && push(a) && push(b);   /* swap */
    case 96: case 100: case 104: case 108: case 112: case 120: case 122:
    case 124: case 126: case 128: case 130:             /* iadd ... ixor */
        return pop(INT, NULL) && pop(INT, NULL) && push(INT);
    case 116: case 145: case 146: case 147:             /* ineg, i2b, i2c, i2s */
        return pop(INT, NULL) && push(INT);
    case 132:                                           /* iinc */
        if (code[pc + 1] >= method->max_locals || cur.locals[code[pc + 1]] != INT)
            return refuse("iinc of a local that is not an int", NULL);
        return 1;
    case 153: case 154: case 155: case 156: case 157: case 158:   /* if<cond> */
        return pop(INT, NULL) && target((int64_t)pc + s2);
    case 159: case 160: case 161: case 162: case 163: case 164:   /* if_icmp<cond> */
        return pop(INT, NULL) && pop(INT, NULL) && target((int64_t)pc + s2);
    case 165: case 166:                                 /* if_acmp<cond> */
        return pop(REFERENCE, NULL) && pop(REFERENCE, NULL) && target((int64_t)pc + s2);
    case 198: case 199:                                 /* ifnull, ifnonnull */
        return pop(REFERENCE, NULL) && target((int64_t)pc + s2);
    case 167:                                           /* goto */
        *goes_on = 0;
        return target((int64_t)pc + s2);
    case 200:                                           /* goto_w */
        *goes_on = 0;
        return target((int64_t)pc + s4(code + pc + 1));
    case 170: case 171: {                               /* tableswitch, lookupswitch */
        uint32_t p = (pc + 4) & ~3u;
        *goes_on = 0;
        if (!pop(INT, NULL) || !target((int64_t)pc + s4(code + p)))
            return 0;
        if (op == 170) {
            int32_t low = s4(code + p + 4), high = s4(code + p + 8);
            if (low > high)
                return refuse("tableswitch with low above high", NULL);
            for (int64_t k = 0; k <= (int64_t)high - low; k++)
                if (!target((int64_t)pc + s4(code + p + 12 + 4 * k)))
                    return 0;
        } else {
            int32_t n = s4(code + p + 4);
            for (int32_t k = 0; k < n; k++) {
                if (k > 0 && s4(code + p + 8 + 8 * k) <= s4(code + p + 8 + 8 * (k - 1)))
                    return refuse("lookupswitch keys not sorted", NULL);
                if (!target((int64_t)pc + s4(code + p + 12 + 8 * k)))
                    return 0;
            }
        }
        return 1;
    }
    case 172:                                           /* ireturn */
        *goes_on = 0;
        if (method->returns == 'V' || method->returns == 'L' ||
            strchr("JFD", method->returns))
            return refuse("ireturn in a method that does not return an int", NULL);
        return pop(INT, NULL);
    case 176: {                                         /* areturn */
        *goes_on = 0;
        if (method->returns != 'L')
            return refuse("areturn in a method that does not return a reference", NULL);
        Type t;
        if (!field_type(return_descriptor(method->descriptor), &end, &t))
            return refuse("bad return type", NULL);
        return pop(t, NULL);
    }
    case 177:                                           /* return */
        *goes_on = 0;
        if (method->returns != 'V')
            return refuse("return in a method that must return a value", NULL);
        if (cur.uninit)
            return refuse("constructor must call super() or this() before return", NULL);
        return 1;
    case 178: case 179: {                               /* getstatic, putstatic */
        Type t;
        if (!cp_member(current, u2, CP_FIELDREF, &cls, &name, &desc))
            return refuse("getstatic or putstatic of an entry that is not a field", NULL);
        if (!field_type(desc, &end, &t) || *end)
            return unsupported("a field of type %s", desc);
        return op == 178 ? push(t) : pop(t, NULL);
    }
    case 182: case 183: case 184: {                     /* invokevirtual, special, static */
        if (!cp_member(current, u2, CP_METHODREF, &cls, &name, &desc) &&
            !(op != 182 && cp_member(current, u2, CP_INTERFACE_METHODREF, &cls, &name, &desc)))
            return refuse("invoke of an entry that is not a method", NULL);
        if (desc[0] != '(')
            return refuse("bad method descriptor", NULL);
        int init = !strcmp(name, "<init>");
        if (!strcmp(name, "<clinit>") || (init && op != 183))
            return refuse("invoke of an initialisation method", NULL);
        if (!pop_arguments(desc))
            return 0;
        if (op == 184)
            return push_result(desc);
        if (op == 182)
            return pop(ref(cls, strlen(cls)), NULL) && push_result(desc);
        if (!init)
            return unsupported("invokespecial of a method other than <init>", NULL);
        if (*return_descriptor(desc) != 'V')
            return refuse("<init> that returns a value", NULL);
        /* An <init> on uninitializedThis: a constructor of this class or of
         * its direct superclass. Every uninitializedThis becomes this class,
         * and the flag goes. */
        if (!pop1(&a))
            return 0;
        if (TAG(a) == UNINIT)
            return unsupported("objects made by new", NULL);
        if (a != UTHIS)
            return refuse("bad type on operand stack: <init> of an initialised object", NULL);
        if (strcmp(cls, current->name) && (!current->super || strcmp(cls, current->super)))
            return refuse("call to the wrong initialization method", NULL);
        Type this = ref(current->name, strlen(current->name));
        for (int i = 0; i < method->max_locals; i++)
            if (cur.locals[i] == UTHIS)
                cur.locals[i] = this;
        for (int i = 0; i < cur.sp; i++)
            if (cur.stack[i] == UTHIS)
                cur.stack[i] = this;
        cur.uninit = 0;
        return 1;
    }
    case 188:                                           /* newarray */
        if (code[pc + 1] < 4 || code[pc + 1] > 11)
            return refuse("bad array type in newarray", NULL);
        if (code[pc + 1] != 10)
            return unsupported("arrays of other elements than int", NULL);
        return pop(INT, NULL) && push(int_array);
    case 190: {                                         /* arraylength */
        Type t;
        if (!pop(REFERENCE, &t))
            return 0;
        if (t != NUL && !(TAG(t) == REF && NAME(t)[0] == '['))
            return refuse("arraylength of something that is not an array", NULL);
        return push(INT);
    }
    case 196: {                                         /* wide */
        unsigned w = code[pc + 1], index = code[pc + 2] << 8 | code[pc + 3];
        switch (w) {
        case 21: return load(index, INT);
        case 25: return load(index, REFERENCE);
        case 54: return store(index, INT);
        case 58: return store(index, REFERENCE);
        case 132:
            if (index >= method->max_locals || cur.locals[index] != INT)
                return refuse("iinc of a local that is not an int", NULL);
            return 1;
        case 22: case 23: case 24: case 55: case 56: case 57: case 169:
            return unsupported("wide %s", opname[w]);
        default:
            return refuse("bad instruction after wide", NULL);
        }
    }
    default:
        if (op > 201)
            return refuse("unknown instruction", NULL);
        if (op == 168 || op == 169 || op == 201)
            return refuse("jsr and ret are not allowed in class files of version 51 and above", NULL);
        return unsupported("instruction %s", opname[op]);
    }
}

static int verify_method(Method *m) {
    method = m;
    at = 0;
    if (!m->code)                       /* native or abstract */
        return 1;
    if (m->exceptions)
        return unsupported("exception handlers", NULL);
    const uint8_t *code = m->code;
    uint32_t n = m->code_length;

    /* Where the instructions start: -2 marks the middle of one. */
    frame_at = malloc(n * sizeof *frame_at);
    for (uint32_t i = 0; i < n; i++)
        frame_at[i] = -2;
    for (uint32_t pc = 0; pc < n; ) {
        int len = instruction_length(code, n, pc);
        at = pc;
        if (!len)
            return refuse("instruction runs past the end of the code, or is unknown", NULL);
        frame_at[pc] = -1;
        pc += len;
    }

    /* The initial frame, from the descriptor: methodInitialStackFrame. */
    Frame initial = new_frame(m);
    int k = 0;
    if (!(m->access & 0x0008)) {
        if (!strcmp(m->name, "<init>") && strcmp(current->name, "java/lang/Object")) {
            initial.locals[k++] = UTHIS;
            initial.uninit = 1;
        } else
            initial.locals[k++] = ref(current->name, strlen(current->name));
    }
    for (const char *d = m->descriptor + 1, *end; *d != ')'; d = end) {
        if (!field_type(d, &end, &initial.locals[k]))
            return unsupported("an argument of type %s", d);
        if (++k > m->max_locals)
            return refuse("arguments do not fit in max_locals", NULL);
    }
    if (!read_frames(&initial, k, &frames, &nframes))
        return 0;
    for (int i = 0; i < nframes; i++) {
        at = frames[i].offset;
        if (frames[i].offset >= n || frame_at[frames[i].offset] != -1)
            return refuse("stack map frame not at the start of an instruction", NULL);
        frame_at[frames[i].offset] = i;
    }

    /* One pass over the code: mergedCodeIsTypeSafe. */
    cur = new_frame(m);
    copy_frame(&cur, &initial);
    int goes_on = 1;
    if (verify_trace)
        printf("%s.%s%s\n", current->name, m->name, m->descriptor);
    for (uint32_t pc = 0; pc < n; pc += instruction_length(code, n, pc)) {
        at = pc;
        if (frame_at[pc] >= 0) {
            const Frame *f = &frames[frame_at[pc]].frame;
            if (goes_on && !frame_assignable(&cur, f))
                return 0;
            copy_frame(&cur, f);
            if (verify_trace)
                show(&cur);
        } else if (!goes_on)
            return refuse("expecting a stack map frame after an "
                          "unconditional branch", NULL);
        if (!instruction(code, pc, &goes_on))
            return 0;
    }
    at = n;
    if (goes_on)
        return refuse("falling off the end of the code", NULL);
    return 1;
}

int verify_class(Class *c) {
    current = c;
    for (int i = 0; i < c->nmethods; i++)
        if (!verify_method(&c->methods[i]))
            return 0;
    return 1;
}
