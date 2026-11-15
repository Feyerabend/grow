/*
 * Running verified code, JVMS chapter 6.
 *
 * One stack of values holds every call's locals and, above them, its operand
 * stack; a call pushes a frame record and goes on in the same loop, so the
 * depth of Java's calls is bounded by this machine's stacks, not by C's.
 * Because the verifier has proved the types of every value at every
 * instruction, nothing here looks at a value to see what it is.
 *
 * A reference in the constant pool is resolved the first time it is used,
 * and remembered: until the program runs, nothing in a class file is an
 * address (JVMS 5.4.3).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "jvm.h"

#define STACK_VALUES (1 << 22)
#define MAX_FRAMES 100000

typedef struct {
    Method *m;
    const uint8_t *pc;
    Value *locals, *sp;
} Call;

static Class *cls;
static Value *stack;
static Call *calls;
static int depth;

/* What a constant of the pool resolves to: a method or a field of this
 * class, System.out, one of PrintStream's methods, or a string. */
enum { UNRESOLVED, METHOD, FIELD, SYSTEM_OUT, PRINT, STRING, OBJECT_INIT };
enum { PRINTLN_INT, PRINTLN_CHAR, PRINTLN_STRING, PRINTLN_BOOLEAN, PRINTLN,
       PRINT_INT, PRINT_CHAR, PRINT_STRING, PRINT_BOOLEAN, WRITE, FLUSH };
static const char *const printers[][2] = {
    { "println", "(I)V" }, { "println", "(C)V" },
    { "println", "(Ljava/lang/String;)V" }, { "println", "(Z)V" },
    { "println", "()V" }, { "print", "(I)V" }, { "print", "(C)V" },
    { "print", "(Ljava/lang/String;)V" }, { "print", "(Z)V" },
    { "write", "(I)V" }, { "flush", "()V" },
};
static uint8_t *kind;
static int *printer;
static char system_out;     /* its address is System.out */

/* An exception that ends the program, printed as Java prints one that no
 * handler catches, with the trace of the calls. */
static void throw(const char *name, const char *message) {
    fflush(stdout);
    if (depth > 0 && !strcmp(calls[0].m->name, "<clinit>")) {
        fprintf(stderr, "Exception in thread \"main\" java.lang.ExceptionInInitializerError\n");
        fprintf(stderr, "Caused by: java.lang.%s", name);
    } else
        fprintf(stderr, "Exception in thread \"main\" java.lang.%s", name);
    fprintf(stderr, message ? ": %s\n" : "\n", message);
    char cname[256];
    snprintf(cname, sizeof cname, "%s", cls->name);
    for (char *p = cname; *p; p++)
        if (*p == '/')
            *p = '.';
    /* As Java does, at most 1024 frames (MaxJavaStackTraceDepth). */
    for (int i = depth - 1; i >= 0 && i >= depth - 1024; i--) {
        Method *m = calls[i].m;
        int line = line_of(m, (int)(calls[i].pc - m->code));
        if (!cls->source)
            fprintf(stderr, "\tat %s.%s(Unknown Source)\n", cname, m->name);
        else if (line)
            fprintf(stderr, "\tat %s.%s(%s:%d)\n", cname, m->name, cls->source, line);
        else
            fprintf(stderr, "\tat %s.%s(%s)\n", cname, m->name, cls->source);
    }
    exit(1);
}

static void link_error(const char *name, const char *what, const char *member) {
    char message[300];
    snprintf(message, sizeof message, "%s.%s", what, member);
    throw(name, message);
}

/* Resolve the constant at index i, once (JVMS 5.4.3). */
static int resolve(int i) {
    if (kind[i] != UNRESOLVED)
        return kind[i];
    const Constant *k = &cls->pool[i];
    const char *owner, *name, *desc;
    if (k->tag == CP_STRING) {
        cls->resolved[i] = (void *)cp_utf8(cls, k->a);
        return kind[i] = STRING;
    }
    cp_member(cls, i, k->tag, &owner, &name, &desc);
    if (k->tag == CP_FIELDREF) {
        if (!strcmp(owner, "java/lang/System") && !strcmp(name, "out") &&
            !strcmp(desc, "Ljava/io/PrintStream;"))
            return kind[i] = SYSTEM_OUT;
        if (strcmp(owner, cls->name))
            link_error("NoClassDefFoundError", owner, name);
        Field *f = find_field(cls, name, desc);
        if (!f)
            link_error("NoSuchFieldError", owner, name);
        if (!(f->access & 0x0008))
            link_error("IncompatibleClassChangeError", owner, name);
        cls->resolved[i] = f;
        return kind[i] = FIELD;
    }
    if (!strcmp(owner, "java/io/PrintStream")) {
        for (size_t p = 0; p < sizeof printers / sizeof *printers; p++)
            if (!strcmp(name, printers[p][0]) && !strcmp(desc, printers[p][1])) {
                printer[i] = (int)p;
                return kind[i] = PRINT;
            }
        link_error("NoSuchMethodError", owner, name);
    }
    if (!strcmp(owner, "java/lang/Object") && !strcmp(name, "<init>") &&
        !strcmp(desc, "()V"))
        return kind[i] = OBJECT_INIT;
    if (strcmp(owner, cls->name))
        link_error("NoClassDefFoundError", owner, name);
    Method *m = find_method(cls, name, desc);
    if (!m)
        link_error("NoSuchMethodError", owner, name);
    if (!(m->access & 0x0008))
        link_error("IncompatibleClassChangeError", owner, name);
    cls->resolved[i] = m;
    return kind[i] = METHOD;
}

/* A char as Java writes it to a UTF-8 stream. */
static void put_char(int c) {
    if (c < 0x80)
        putchar(c);
    else if (c < 0x800) {
        putchar(0xC0 | c >> 6);
        putchar(0x80 | (c & 63));
    } else {
        putchar(0xE0 | c >> 12);
        putchar(0x80 | (c >> 6 & 63));
        putchar(0x80 | (c & 63));
    }
}

static void print(int which, Value v) {
    switch (which) {
    case PRINTLN_INT: printf("%d\n", (int32_t)v); break;
    case PRINT_INT: printf("%d", (int32_t)v); break;
    case PRINTLN_CHAR: put_char((uint16_t)v); putchar('\n'); break;
    case PRINT_CHAR: put_char((uint16_t)v); break;
    case PRINTLN_BOOLEAN: puts(v ? "true" : "false"); break;
    case PRINT_BOOLEAN: fputs(v ? "true" : "false", stdout); break;
    case PRINTLN_STRING: puts(v ? (const char *)v : "null"); break;
    case PRINT_STRING: fputs(v ? (const char *)v : "null", stdout); break;
    case PRINTLN: putchar('\n'); break;
    case WRITE: putchar((int)v & 255); break;
    case FLUSH: fflush(stdout); break;
    }
}

static int16_t s2(const uint8_t *p) { return (int16_t)(p[0] << 8 | p[1]); }
static uint16_t u2(const uint8_t *p) { return (uint16_t)(p[0] << 8 | p[1]); }
static int32_t s4(const uint8_t *p) {
    return (int32_t)((uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 | (uint32_t)p[2] << 8 | p[3]);
}

static Array *new_array(int32_t length) {
    if (length < 0) {
        char n[16];
        snprintf(n, sizeof n, "%d", length);
        throw("NegativeArraySizeException", n);
    }
    Array *a = calloc(1, sizeof *a + (size_t)length * sizeof(int32_t));
    if (!a)
        throw("OutOfMemoryError", "Java heap space");
    a->length = length;
    return a;
}

static Array *element(Value ref, int32_t index) {
    Array *a = (Array *)ref;
    if (!a)
        throw("NullPointerException", NULL);
    if (index < 0 || index >= a->length) {
        char message[80];
        snprintf(message, sizeof message, "Index %d out of bounds for length %d",
                 index, a->length);
        throw("ArrayIndexOutOfBoundsException", message);
    }
    return a;
}

/* Run a static method with its arguments already on the stack at sp. */
static void execute(Method *entry, Value *sp) {
    Method *m = entry;
    const uint8_t *pc = m->code;
    Value *locals = sp, a, b;
    sp = locals + m->max_locals;
    int base = depth;
    calls[depth++] = (Call){ m, pc, locals, sp };

#define PUSH(v) (*sp++ = (Value)(v))
#define POP() (*--sp)
#define I(v) ((int32_t)(v))
#define BRANCH(cond) do { if (cond) { pc += s2(pc + 1); goto next; } pc += 3; goto next; } while (0)
    for (;;) {
    next:
        calls[depth - 1].pc = pc;       /* for a trace, if this throws */
        switch (*pc) {
        case 0: pc++; break;                                    /* nop */
        case 1: PUSH(0); pc++; break;                           /* aconst_null */
        case 2: case 3: case 4: case 5: case 6: case 7: case 8: /* iconst */
            PUSH(*pc - 3); pc++; break;
        case 16: PUSH((int8_t)pc[1]); pc += 2; break;           /* bipush */
        case 17: PUSH(s2(pc + 1)); pc += 3; break;              /* sipush */
        case 18: case 19: {                                     /* ldc, ldc_w */
            int i = *pc == 18 ? pc[1] : u2(pc + 1);
            if (cls->pool[i].tag == CP_INTEGER)
                PUSH(cls->pool[i].value);
            else {
                resolve(i);
                PUSH(cls->resolved[i]);
            }
            pc += *pc == 18 ? 2 : 3;
            break;
        }
        case 21: case 25: PUSH(locals[pc[1]]); pc += 2; break;  /* iload, aload */
        case 26: case 27: case 28: case 29: PUSH(locals[*pc - 26]); pc++; break;
        case 42: case 43: case 44: case 45: PUSH(locals[*pc - 42]); pc++; break;
        case 46:                                                /* iaload */
            b = POP(); a = POP();
            PUSH(element(a, I(b))->data[I(b)]);
            pc++;
            break;
        case 54: case 58: locals[pc[1]] = POP(); pc += 2; break;  /* istore, astore */
        case 59: case 60: case 61: case 62: locals[*pc - 59] = POP(); pc++; break;
        case 75: case 76: case 77: case 78: locals[*pc - 75] = POP(); pc++; break;
        case 79: {                                              /* iastore */
            Value v = POP();
            b = POP(); a = POP();
            element(a, I(b))->data[I(b)] = I(v);
            pc++;
            break;
        }
        case 87: sp--; pc++; break;                             /* pop */
        case 88: sp -= 2; pc++; break;                          /* pop2 */
        case 89: sp[0] = sp[-1]; sp++; pc++; break;             /* dup */
        case 90:                                                /* dup_x1 */
            a = sp[-1]; b = sp[-2];
            sp[-2] = a; sp[-1] = b; sp[0] = a; sp++; pc++; break;
        case 91: {                                              /* dup_x2 */
            Value c;
            a = sp[-1]; b = sp[-2]; c = sp[-3];
            sp[-3] = a; sp[-2] = c; sp[-1] = b; sp[0] = a; sp++; pc++; break;
        }
        case 92:                                                /* dup2 */
            sp[0] = sp[-2]; sp[1] = sp[-1]; sp += 2; pc++; break;
        case 93: {                                              /* dup2_x1 */
            Value c;
            a = sp[-1]; b = sp[-2]; c = sp[-3];
            sp[-3] = b; sp[-2] = a; sp[-1] = c; sp[0] = b; sp[1] = a; sp += 2; pc++; break;
        }
        case 94: {                                              /* dup2_x2 */
            Value c, d;
            a = sp[-1]; b = sp[-2]; c = sp[-3]; d = sp[-4];
            sp[-4] = b; sp[-3] = a; sp[-2] = d; sp[-1] = c; sp[0] = b; sp[1] = a;
            sp += 2; pc++; break;
        }
        case 95: a = sp[-1]; sp[-1] = sp[-2]; sp[-2] = a; pc++; break;  /* swap */
        /* Integer arithmetic wraps, in two's complement (JVMS 2.11.3):
         * done in unsigned, where C defines it. */
        case 96: b = POP(); a = POP(); PUSH((int32_t)((uint32_t)a + (uint32_t)b)); pc++; break;
        case 100: b = POP(); a = POP(); PUSH((int32_t)((uint32_t)a - (uint32_t)b)); pc++; break;
        case 104: b = POP(); a = POP(); PUSH((int32_t)((uint32_t)a * (uint32_t)b)); pc++; break;
        case 108: case 112:                         /* idiv, irem */
            b = POP(); a = POP();
            if (I(b) == 0)
                throw("ArithmeticException", "/ by zero");
            /* the one overflow: MIN_VALUE / -1 is MIN_VALUE */
            if (I(b) == -1)
                PUSH(*pc == 108 ? (int32_t)(0u - (uint32_t)a) : 0);
            else
                PUSH(*pc == 108 ? I(a) / I(b) : I(a) % I(b));
            pc++;
            break;
        case 116: a = POP(); PUSH((int32_t)(0u - (uint32_t)a)); pc++; break;   /* ineg */
        case 120: b = POP(); a = POP(); PUSH((int32_t)((uint32_t)a << (b & 31))); pc++; break;
        case 122: b = POP(); a = POP(); PUSH(I(a) >> (b & 31)); pc++; break;   /* ishr */
        case 124: b = POP(); a = POP(); PUSH((int32_t)((uint32_t)a >> (b & 31))); pc++; break;
        case 126: b = POP(); a = POP(); PUSH(I(a) & I(b)); pc++; break;
        case 128: b = POP(); a = POP(); PUSH(I(a) | I(b)); pc++; break;
        case 130: b = POP(); a = POP(); PUSH(I(a) ^ I(b)); pc++; break;
        case 132:                                               /* iinc */
            locals[pc[1]] = (int32_t)((uint32_t)locals[pc[1]] + (uint32_t)(int8_t)pc[2]);
            pc += 3;
            break;
        case 145: a = POP(); PUSH((int8_t)a); pc++; break;     /* i2b */
        case 146: a = POP(); PUSH((uint16_t)a); pc++; break;   /* i2c */
        case 147: a = POP(); PUSH((int16_t)a); pc++; break;    /* i2s */
        case 153: a = POP(); BRANCH(I(a) == 0);
        case 154: a = POP(); BRANCH(I(a) != 0);
        case 155: a = POP(); BRANCH(I(a) < 0);
        case 156: a = POP(); BRANCH(I(a) >= 0);
        case 157: a = POP(); BRANCH(I(a) > 0);
        case 158: a = POP(); BRANCH(I(a) <= 0);
        case 159: b = POP(); a = POP(); BRANCH(I(a) == I(b));
        case 160: b = POP(); a = POP(); BRANCH(I(a) != I(b));
        case 161: b = POP(); a = POP(); BRANCH(I(a) < I(b));
        case 162: b = POP(); a = POP(); BRANCH(I(a) >= I(b));
        case 163: b = POP(); a = POP(); BRANCH(I(a) > I(b));
        case 164: b = POP(); a = POP(); BRANCH(I(a) <= I(b));
        case 165: b = POP(); a = POP(); BRANCH(a == b);         /* if_acmpeq */
        case 166: b = POP(); a = POP(); BRANCH(a != b);
        case 198: a = POP(); BRANCH(a == 0);                    /* ifnull */
        case 199: a = POP(); BRANCH(a != 0);
        case 167: pc += s2(pc + 1); break;                      /* goto */
        case 200: pc += s4(pc + 1); break;                      /* goto_w */
        case 170: {                                             /* tableswitch */
            const uint8_t *p = m->code + ((pc - m->code + 4) & ~3);
            int32_t key = I(POP()), low = s4(p + 4), high = s4(p + 8);
            if (key < low || key > high)
                pc += s4(p);
            else
                pc += s4(p + 12 + 4 * ((int64_t)key - low));
            break;
        }
        case 171: {                                             /* lookupswitch */
            const uint8_t *p = m->code + ((pc - m->code + 4) & ~3);
            int32_t key = I(POP()), n = s4(p + 4), lo = 0, hi = n - 1;
            int32_t to = s4(p);
            while (lo <= hi) {          /* the keys are sorted: verified */
                int32_t mid = lo + (hi - lo) / 2, k = s4(p + 8 + 8 * mid);
                if (k == key) { to = s4(p + 12 + 8 * mid); break; }
                if (k < key) lo = mid + 1; else hi = mid - 1;
            }
            pc += to;
            break;
        }
        case 172: case 176: case 177: {                         /* ireturn, areturn, return */
            Value v = *pc == 177 ? 0 : POP();
            depth--;
            if (depth == base)
                return;
            sp = locals;                /* the arguments are gone */
            m = calls[depth - 1].m;
            pc = calls[depth - 1].pc;
            locals = calls[depth - 1].locals;
            if (calls[depth].m->returns != 'V')
                PUSH(v);
            pc += 3;                    /* past the invokestatic */
            break;
        }
        case 178: {                                             /* getstatic */
            int i = u2(pc + 1);
            if (resolve(i) == SYSTEM_OUT)
                PUSH(&system_out);
            else
                PUSH(((Field *)cls->resolved[i])->value);
            pc += 3;
            break;
        }
        case 179:                                               /* putstatic */
            if (resolve(u2(pc + 1)) == SYSTEM_OUT)
                link_error("IllegalAccessError", "java/lang/System", "out");
            ((Field *)cls->resolved[u2(pc + 1)])->value = POP();
            pc += 3;
            break;
        case 182: {                                             /* invokevirtual */
            int i = u2(pc + 1);
            resolve(i);
            int which = printer[i];
            int takes = !(which == PRINTLN || which == FLUSH);
            Value v = takes ? POP() : 0;
            if (POP() != (Value)&system_out)
                throw("NullPointerException", NULL);
            print(which, v);
            pc += 3;
            break;
        }
        case 183:                                               /* invokespecial */
            resolve(u2(pc + 1));        /* Object's <init>: nothing to do */
            sp--;
            pc += 3;
            break;
        case 184: {                                             /* invokestatic */
            int i = u2(pc + 1);
            if (kind[i] != METHOD)
                resolve(i);
            Method *callee = cls->resolved[i];
            if (!callee->code)
                link_error("UnsatisfiedLinkError", cls->name, callee->name);
            Value *args = sp - callee->nargs;
            if (depth == MAX_FRAMES ||
                args + callee->max_locals + callee->max_stack > stack + STACK_VALUES)
                throw("StackOverflowError", NULL);
            calls[depth - 1].pc = pc;
            calls[depth - 1].sp = args;
            m = callee;
            locals = args;
            sp = locals + m->max_locals;
            pc = m->code;
            calls[depth++] = (Call){ m, pc, locals, sp };
            break;
        }
        case 188: {                                             /* newarray, of int */
            Array *arr = new_array(I(POP()));
            PUSH(arr);
            pc += 2;
            break;
        }
        case 190:                                               /* arraylength */
            a = POP();
            if (!a)
                throw("NullPointerException", NULL);
            PUSH(((Array *)a)->length);
            pc++;
            break;
        case 196: {                                             /* wide */
            int index = u2(pc + 2);
            switch (pc[1]) {
            case 21: case 25: PUSH(locals[index]); pc += 4; break;
            case 54: case 58: locals[index] = POP(); pc += 4; break;
            case 132:
                locals[index] = (int32_t)((uint32_t)locals[index] + (uint32_t)s2(pc + 4));
                pc += 6;
                break;
            }
            break;
        }
        default:            /* the verifier lets nothing else through */
            fprintf(stderr, "unverified instruction %d\n", *pc);
            exit(2);
        }
    }
}

int run_class(Class *c) {
    cls = c;
    stack = malloc(STACK_VALUES * sizeof *stack);
    calls = malloc(MAX_FRAMES * sizeof *calls);
    kind = calloc(c->count, 1);
    printer = calloc(c->count, sizeof *printer);
    Method *clinit = find_method(c, "<clinit>", "()V");
    if (clinit)
        execute(clinit, stack);
    Method *main = find_method(c, "main", "([Ljava/lang/String;)V");
    if (!main || !(main->access & 0x0008)) {
        char name[256];
        snprintf(name, sizeof name, "%s", c->name);
        for (char *p = name; *p; p++)
            if (*p == '/')
                *p = '.';
        fprintf(stderr, "Error: Main method not found in class %s\n", name);
        return 1;
    }
    stack[0] = (Value)new_array(0);         /* args: an empty String[] */
    execute(main, stack);
    fflush(stdout);
    return 0;
}
