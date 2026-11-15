/*
 * cek.c — Lark C CEK machine.
 *
 * The machine has three global variables representing the current state:
 *   _mode  — EVAL (reduce an expression) or RET (deliver a value to a frame)
 *   _expr  — expression to reduce (EVAL mode)
 *   _env   — local environment (EVAL mode)
 *   _val   — value to deliver (RET mode)
 *
 * The continuation is a fixed-size stack of LkFrame values.
 *
 * All runtime heap objects (closures, tuples, constructors, environment
 * cells, strings built at runtime) live in a heap that a copying garbage
 * collector keeps (below). In Lark's own machine they lived in an arena
 * that was never freed.
 */

#include "cek.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/* -- The heap --
 *
 * Two spaces, as in Cheney's copying collector of 1970: objects are
 * made in one, by moving a pointer along it; when it is half full, the
 * objects still in use are copied to the other, and the first is given
 * up. Every object has a header, its kind and its size, so that the
 * collector knows what it is copying and which of its words point to
 * other objects. A copied object's header says so, and its first word
 * then holds where it went.
 *
 * Collection happens only between steps of the machine, when every
 * pointer into the heap is in the machine's state, its continuation,
 * or its tables, and none in a variable of C's. So a step must find
 * room for what it makes without collecting: half the space is kept
 * free for it. If much survives a collection, the next space is twice
 * the size, up to LARK_HEAP_MAX.
 */

#ifndef LARK_HEAP_START
#  define LARK_HEAP_START (1u << 20)             /* 1 MB */
#endif
#ifndef LARK_HEAP_MAX
#  define LARK_HEAP_MAX   ((size_t)1 << 30)      /* 1 GB */
#endif

typedef enum {
    OBJ_ENV, OBJ_TUPLE, OBJ_CON, OBJ_PARTIAL, OBJ_CLOSURE, OBJ_STRING,
    OBJ_BOX,            /* one LkVal: the IO value print holds */
    OBJ_MOVED,          /* copied: the first word says where */
} ObjKind;

typedef struct { uint32_t kind, size; } Header;     /* size: of what follows */

static char*  _heap;        /* the space objects are made in */
static size_t _cap, _used;
static size_t _collections, _copied, _peak;
static int    _half_full;   /* set by allocate, looked at between steps */

static void* allocate(ObjKind kind, size_t bytes) {
    bytes = (bytes + 7u) & ~(size_t)7u;
    if (bytes < 8) bytes = 8;                     /* room for a forwarding address */
    if (_used + sizeof(Header) + bytes > _cap) {
        fputs("lark: heap exhausted\n", stderr);
        exit(1);
    }
    Header* h = (Header*)(_heap + _used);
    h->kind = kind;
    h->size = (uint32_t)bytes;
    _used += sizeof(Header) + bytes;
    if (_used > _cap / 2) {
        _half_full = 1;
        if (_used > _peak) _peak = _used;
    }
    return h + 1;
}

#define AR(kind, bytes) allocate((kind), (bytes))


/* -- Top-level environment -- */

/*
 * Top-level names (functions, lets, constructors) are stored in a flat
 * mutable array rather than the persistent linked list used for locals.
 * This means closures created at the top level do not need to capture a
 * snapshot of the top-level env — they just look things up here at call
 * time.  Mutual recursion therefore works without backpatching.
 */

#ifndef LARK_TOP_MAX
#  define LARK_TOP_MAX 512
#endif

typedef struct { const char* name; LkVal val; } TopEntry;
static TopEntry _top[LARK_TOP_MAX];
static int      _top_n = 0;

static void top_set(const char* name, LkVal val) {
    for (int i = 0; i < _top_n; i++) {
        if (strcmp(_top[i].name, name) == 0) { _top[i].val = val; return; }
    }
    _top[_top_n++] = (TopEntry){ name, val };
}

/* A top-level name's slot, or -1. The table only grows, and a name
 * keeps its slot, so a slot once found stays right. */
static int top_index(const char* name) {
    for (int i = 0; i < _top_n; i++)
        if (strcmp(_top[i].name, name) == 0) return i;
    return -1;
}

static LkVal* top_get(const char* name) {
    for (int i = 0; i < _top_n; i++) {
        if (strcmp(_top[i].name, name) == 0) return &_top[i].val;
    }
    return NULL;
}


/* -- Local environment -- */

static LkEnv* env_bind(LkEnv* env, const char* name, LkVal val) {
    LkEnv* node  = AR(OBJ_ENV, sizeof(LkEnv));
    node->name   = name;
    node->val    = val;
    node->next   = env;
    return node;
}

/* A variable, by position: depth cells out from env, or, if
 * depth is -1, in the top-level table, at the slot found the
 * first time and kept in the expression. Lark's own machine
 * compared the name with each cell's, then with each top-level
 * name's, every time. The cells still carry their names: built
 * with LARK_CHECK_DEPTH, the machine checks that the cell it
 * reaches is the one the name says. */
static LkVal env_lookup(LkEnv* env, const LkExpr* e) {
    if (e->depth >= 0) {
        LkEnv* n = env;
        for (int d = e->depth; d > 0 && n; d--)
            n = n->next;
        if (!n) {
            fprintf(stderr, "lark: no variable %s at depth %d\n",
                    e->name, e->depth);
            exit(1);
        }
#ifdef LARK_CHECK_DEPTH
        if (strcmp(n->name, e->name) != 0) {
            fprintf(stderr, "lark: %s at depth %d is %s\n",
                    e->name, e->depth, n->name);
            exit(3);
        }
#endif
        return n->val;
    }
    if (e->slot < 0) {
        int slot = top_index(e->name);
        if (slot < 0) {
            fprintf(stderr, "lark: unbound: %s\n", e->name);
            exit(1);
        }
        /* the tree is the machine's own, read from a file */
        ((LkExpr*)e)->slot = slot;
    }
    return _top[e->slot].val;
}


/* -- Dispatch table -- */

#ifndef LARK_DISPATCH_MAX
#  define LARK_DISPATCH_MAX 128
#endif

typedef struct { const char* method; const char* type_; LkVal impl; } DispEntry;
static DispEntry _disp[LARK_DISPATCH_MAX];
static int       _disp_n = 0;

static void disp_set(const char* method, const char* type_, LkVal impl) {
    for (int i = 0; i < _disp_n; i++) {
        if (strcmp(_disp[i].method, method) == 0 &&
            strcmp(_disp[i].type_,  type_)  == 0) { _disp[i].impl = impl; return; }
    }
    _disp[_disp_n++] = (DispEntry){ method, type_, impl };
}

static LkVal* disp_get(const char* method, const char* type_) {
    for (int i = 0; i < _disp_n; i++) {
        if (strcmp(_disp[i].method, method) == 0 &&
            strcmp(_disp[i].type_,  type_)  == 0) return &_disp[i].impl;
    }
    return NULL;
}


/* -- Constructor table -- */

#ifndef LARK_CON_MAX
#  define LARK_CON_MAX 128
#endif

typedef struct { const char* tag; const char* type_name; int arity; } ConEntry;
static ConEntry _con[LARK_CON_MAX];
static int      _con_n = 0;

static void con_register(const char* tag, const char* type_name, int arity) {
    for (int i = 0; i < _con_n; i++) {
        if (strcmp(_con[i].tag, tag) == 0) {
            _con[i].type_name = type_name; _con[i].arity = arity; return;
        }
    }
    _con[_con_n++] = (ConEntry){ tag, type_name, arity };
}

static const char* con_type(const char* tag) {
    for (int i = 0; i < _con_n; i++)
        if (strcmp(_con[i].tag, tag) == 0) return _con[i].type_name;
    return tag;
}


/* -- Value factories -- */

static LkVal lk_int(int32_t i)        { return (LkVal){ .kind=V_INT,     .i=i   }; }
static LkVal lk_float(uint32_t f)     { return (LkVal){ .kind=V_FLOAT,   .f=f   }; }
static LkVal lk_bool(int b)           { return (LkVal){ .kind=V_BOOL,    .b=b   }; }
static LkVal lk_str(const char* s)    { return (LkVal){ .kind=V_STR,     .s=s   }; }
static LkVal lk_unit(void)            { return (LkVal){ .kind=V_UNIT             }; }
static LkVal lk_io(void)              { return (LkVal){ .kind=V_IO               }; }
/* The built-in functions, by number; their names are for messages. */
typedef enum {
    B_PRINT, B_READ, B_SHOW, B_INT_TO_FLOAT, B_FLOAT_TO_INT, B_INT_TO_STRING,
    B_FLOAT_TO_STRING, B_INT_ABS, B_FLOAT_ABS, B_FLOAT_SQRT, B_FLOAT_FLOOR,
    B_FLOAT_CEIL, B_STRING_LENGTH, N_BUILTINS,
} Builtin;

static const char* const builtin_names[N_BUILTINS] = {
    "print", "read", "show", "int_to_float", "float_to_int", "int_to_string",
    "float_to_string", "int_abs", "float_abs", "float_sqrt", "float_floor",
    "float_ceil", "string_length",
};

static LkVal lk_builtin(Builtin b)    { return (LkVal){ .kind=V_BUILTIN, .builtin=(int)b }; }
static LkVal lk_dispatch(const char* m){ return (LkVal){ .kind=V_DISPATCH,.method=m  }; }

static LkVal lk_tuple(const LkVal* elems, int n) {
    LkTuple* t = AR(OBJ_TUPLE, sizeof(LkTuple) + (size_t)n * sizeof(LkVal));
    t->n = n;
    memcpy(t->elems, elems, (size_t)n * sizeof(LkVal));
    return (LkVal){ .kind=V_TUPLE, .tup=t };
}

static LkVal lk_con(const char* tag, const LkVal* fields, int n) {
    LkCon* c = AR(OBJ_CON, sizeof(LkCon) + (size_t)n * sizeof(LkVal));
    c->tag = tag; c->n = n;
    if (n > 0) memcpy(c->fields, fields, (size_t)n * sizeof(LkVal));
    return (LkVal){ .kind=V_CON, .con=c };
}

static LkVal lk_partial(const char* tag, int arity, const LkVal* args, int n) {
    LkPartCon* pc = AR(OBJ_PARTIAL, sizeof(LkPartCon) + (size_t)n * sizeof(LkVal));
    pc->tag = tag; pc->arity = arity; pc->n = n;
    if (n > 0) memcpy(pc->args, args, (size_t)n * sizeof(LkVal));
    return (LkVal){ .kind=V_PARTIAL, .part=pc };
}

static LkVal lk_closure(const char* param, const LkExpr* body,
                         LkEnv* env, const char* rec) {
    LkClosure* c = AR(OBJ_CLOSURE, sizeof(LkClosure));
    c->param = param; c->body = body; c->env = env; c->rec = rec;
    return (LkVal){ .kind=V_CLOSURE, .clos=c };
}

static LkVal lk_print_io(LkVal io) {
    LkVal* p = AR(OBJ_BOX, sizeof(LkVal));
    *p = io;
    return (LkVal){ .kind=V_PRINT_IO, .pio=p };
}


/* -- Float helpers -- */

static float bits_f32(uint32_t bits) {
    float f; memcpy(&f, &bits, 4); return f;
}
static uint32_t f32_bits(float f) {
    uint32_t bits; memcpy(&bits, &f, 4); return bits;
}


/* -- String helpers -- */

/* Concatenate two C strings into a new string in the heap. */
static const char* str_cat(const char* a, const char* b) {
    size_t la = strlen(a), lb = strlen(b);
    char*  s  = AR(OBJ_STRING, la + lb + 1);
    memcpy(s, a, la);
    memcpy(s + la, b, lb);
    s[la + lb] = '\0';
    return s;
}

/* Copy a string into the heap. */
static const char* str_dup(const char* s) {
    size_t n = strlen(s);
    char*  d = AR(OBJ_STRING, n + 1);
    memcpy(d, s, n + 1);
    return d;
}

/* Format float32 bits as a Lark float literal string. */
static const char* show_float(uint32_t bits) {
    char buf[32];
    float f = bits_f32(bits);
    snprintf(buf, sizeof buf, "%.7g", f);
    if (!strchr(buf, '.') && !strchr(buf, 'e') &&
        !strchr(buf, 'n') && !strchr(buf, 'i')) {
        size_t n = strlen(buf);
        buf[n] = '.'; buf[n+1] = '0'; buf[n+2] = '\0';
    }
    return str_dup(buf);
}


/* -- Show -- */

static const char* val_show(LkVal v) {
    char buf[32];
    switch (v.kind) {
        case V_INT:   snprintf(buf, sizeof buf, "%d", v.i);  return str_dup(buf);
        case V_FLOAT: return show_float(v.f);
        case V_BOOL:  return v.b ? "true" : "false";
        case V_STR:   return v.s;
        case V_UNIT:  return "()";
        case V_TUPLE: {
            const char* r = "(";
            for (int i = 0; i < v.tup->n; i++) {
                if (i) r = str_cat(r, ", ");
                r = str_cat(r, val_show(v.tup->elems[i]));
            }
            return str_cat(r, ")");
        }
        case V_CON:
            if (v.con->n == 0) return v.con->tag;
            {
                const char* r = str_cat(v.con->tag, "(");
                for (int i = 0; i < v.con->n; i++) {
                    if (i) r = str_cat(r, ", ");
                    r = str_cat(r, val_show(v.con->fields[i]));
                }
                return str_cat(r, ")");
            }
        default:
            snprintf(buf, sizeof buf, "<val:%d>", v.kind);
            return str_dup(buf);
    }
}


/* -- Runtime type name (for dispatch) -- */

static const char* val_type(LkVal v) {
    switch (v.kind) {
        case V_INT:   return "Int";
        case V_FLOAT: return "Float";
        case V_BOOL:  return "Bool";
        case V_STR:   return "String";
        case V_UNIT:  return "()";
        case V_CON:   return con_type(v.con->tag);
        default:      return "?";
    }
}


/* -- Value equality (used by literal patterns) -- */

static int val_eq(LkVal a, LkVal b) {
    if (a.kind != b.kind) return 0;
    switch (a.kind) {
        case V_INT:   return a.i == b.i;
        case V_FLOAT: return a.f == b.f;
        case V_BOOL:  return a.b == b.b;
        case V_STR:   return strcmp(a.s, b.s) == 0;
        case V_UNIT:  return 1;
        default:      return 0;
    }
}

static LkVal lit_val(LkLit lit) {
    switch (lit.kind) {
        case LIT_INT:   return lk_int(lit.i);
        case LIT_FLOAT: return lk_float(lit.f);
        case LIT_BOOL:  return lk_bool(lit.b);
        case LIT_STR:   return lk_str(lit.s);
        case LIT_UNIT:  return lk_unit();
    }
    return lk_unit();
}


/* -- Binary / unary operations -- */

/* The operators, by number (Op, in cek.h); op is their name, for the
 * message if one is given values it has no meaning for. Int is wrapping
 * two's-complement i32, as on RISC-V: arithmetic is done in uint32_t,
 * whose overflow C defines, as signed overflow it does not. */
static LkVal binop(Op code, const char* op, LkVal l, LkVal r) {
    if (code == OP_ADD && l.kind == V_STR && r.kind == V_STR)
        return lk_str(str_cat(l.s, r.s));

    if (l.kind == V_INT && r.kind == V_INT) {
        int32_t a = l.i, b = r.i;
        uint32_t ua = (uint32_t)a, ub = (uint32_t)b;
        switch (code) {
            case OP_ADD: return lk_int((int32_t)(ua + ub));
            case OP_SUB: return lk_int((int32_t)(ua - ub));
            case OP_MUL: return lk_int((int32_t)(ua * ub));
            case OP_DIV:
                /* RISC-V DIV: x/0 = -1; INT_MIN / -1 = INT_MIN (C would trap). */
                if (b == 0) return lk_int(-1);
                if (a == INT32_MIN && b == -1) return lk_int(INT32_MIN);
                return lk_int(a / b);
            case OP_REM:
                /* RISC-V REM: x%0 = x; INT_MIN % -1 = 0. */
                if (b == 0) return lk_int(a);
                if (a == INT32_MIN && b == -1) return lk_int(0);
                return lk_int(a % b);   /* C '%' truncates toward zero, as RV32 */
            case OP_EQ: return lk_bool(a == b);
            case OP_NE: return lk_bool(a != b);
            case OP_LT: return lk_bool(a <  b);
            case OP_LE: return lk_bool(a <= b);
            case OP_GT: return lk_bool(a >  b);
            case OP_GE: return lk_bool(a >= b);
            default: break;
        }
    }

    if (l.kind == V_FLOAT && r.kind == V_FLOAT) {
        float a = bits_f32(l.f), b = bits_f32(r.f);
        switch (code) {
            case OP_ADD: return lk_float(f32_bits(a + b));
            case OP_SUB: return lk_float(f32_bits(a - b));
            case OP_MUL: return lk_float(f32_bits(a * b));
            case OP_DIV: return lk_float(b==0.0f ? 0x7FC00000u : f32_bits(a/b));
            case OP_EQ: return lk_bool(a == b);
            case OP_NE: return lk_bool(a != b);
            case OP_LT: return lk_bool(a <  b);
            case OP_LE: return lk_bool(a <= b);
            case OP_GT: return lk_bool(a >  b);
            case OP_GE: return lk_bool(a >= b);
            default: break;
        }
    }

    if (code == OP_AND)
        return lk_bool(l.kind==V_BOOL && r.kind==V_BOOL && l.b && r.b);
    if (code == OP_OR)
        return lk_bool((l.kind==V_BOOL && l.b) || (r.kind==V_BOOL && r.b));

    fprintf(stderr, "lark: bad binop '%s'\n", op); exit(1);
}

static LkVal unaryop(Op code, const char* op, LkVal v) {
    if (code == OP_NEG) {
        if (v.kind == V_INT)   return lk_int((int32_t)(0u - (uint32_t)v.i));
        if (v.kind == V_FLOAT) return lk_float(f32_bits(-bits_f32(v.f)));
    }
    if (code == OP_NOT && v.kind == V_BOOL) return lk_bool(!v.b);
    fprintf(stderr, "lark: bad unaryop '%s'\n", op); exit(1);
}


/* -- Pattern matching -- */

/* Try to match val against pat.  On success return 1 and add bindings to
 * *env_out.  On failure return 0; *env_out may have been partially extended
 * but the caller discards the result. */
static int match_pat(const LkPat* pat, LkVal val, LkEnv** env_out) {
    switch (pat->kind) {
        case PAT_WILD:
            return 1;

        case PAT_VAR:
            *env_out = env_bind(*env_out, pat->var, val);
            return 1;

        case PAT_LIT:
            return val_eq(val, lit_val(pat->lit));

        case PAT_CON:
            if (strcmp(pat->con.name, "True")  == 0 && pat->con.n_args == 0)
                return val.kind == V_BOOL && val.b;
            if (strcmp(pat->con.name, "False") == 0 && pat->con.n_args == 0)
                return val.kind == V_BOOL && !val.b;
            if (val.kind != V_CON) return 0;
            if (strcmp(val.con->tag, pat->con.name) != 0) return 0;
            if (val.con->n != pat->con.n_args) return 0;
            for (int i = 0; i < pat->con.n_args; i++)
                if (!match_pat(pat->con.args[i], val.con->fields[i], env_out)) return 0;
            return 1;

        case PAT_TUPLE:
            if (val.kind != V_TUPLE || val.tup->n != pat->tup.n) return 0;
            for (int i = 0; i < pat->tup.n; i++)
                if (!match_pat(pat->tup.elems[i], val.tup->elems[i], env_out)) return 0;
            return 1;
    }
    return 0;
}


/* -- Built-in functions -- */

/* Abort with a clear message if arg has the wrong kind. */
#define BUILTIN_EXPECT(kind_name, kind_enum) \
    do { if (arg.kind != (kind_enum)) { \
        fprintf(stderr, "lark: %s expects %s (got kind %d)\n", \
                name, (kind_name), arg.kind); \
        exit(1); \
    } } while (0)

static LkVal apply_builtin(Builtin id, LkVal arg) {
    const char* name = builtin_names[id];   /* for the messages */
    if (id == B_PRINT) {
        BUILTIN_EXPECT("IO", V_IO);
        return lk_print_io(arg);
    }

    if (id == B_READ) {
        BUILTIN_EXPECT("IO", V_IO);
        char buf[1024];
        if (!fgets(buf, sizeof buf, stdin)) buf[0] = '\0';
        size_t n = strlen(buf);
        if (n && buf[n-1] == '\n') buf[n-1] = '\0';
        LkVal pair[2] = { arg, lk_str(str_dup(buf)) };
        return lk_tuple(pair, 2);
    }

    if (id == B_SHOW)
        return lk_str(val_show(arg));

    if (id == B_INT_TO_FLOAT) {
        BUILTIN_EXPECT("Int", V_INT);
        return lk_float(f32_bits((float)arg.i));
    }

    if (id == B_FLOAT_TO_INT) {
        BUILTIN_EXPECT("Float", V_FLOAT);
        return lk_int((int32_t)bits_f32(arg.f));
    }

    if (id == B_INT_TO_STRING)
        return lk_str(val_show(arg));

    if (id == B_FLOAT_TO_STRING)
        return lk_str(val_show(arg));

    if (id == B_INT_ABS) {
        BUILTIN_EXPECT("Int", V_INT);
        /* Wrapping i32: int_abs(INT32_MIN) = INT32_MIN, matching the
         * Python backends and RV32 (negation wraps). */
        int32_t v = arg.i;
        return lk_int(v < 0 ? (int32_t)(0u - (uint32_t)v) : v);
    }

    if (id == B_FLOAT_ABS) {
        BUILTIN_EXPECT("Float", V_FLOAT);
        return lk_float(arg.f & 0x7FFFFFFFu);
    }

    if (id == B_FLOAT_SQRT) {
        BUILTIN_EXPECT("Float", V_FLOAT);
        return lk_float(f32_bits(sqrtf(bits_f32(arg.f))));
    }

    if (id == B_FLOAT_FLOOR) {
        BUILTIN_EXPECT("Float", V_FLOAT);
        return lk_float(f32_bits(floorf(bits_f32(arg.f))));
    }

    if (id == B_FLOAT_CEIL) {
        BUILTIN_EXPECT("Float", V_FLOAT);
        return lk_float(f32_bits(ceilf(bits_f32(arg.f))));
    }

    if (id == B_STRING_LENGTH) {
        BUILTIN_EXPECT("String", V_STR);
        return lk_int((int32_t)strlen(arg.s));
    }

    fprintf(stderr, "lark: unknown builtin: %s\n", name);
    exit(1);
}

#undef BUILTIN_EXPECT


/* -- Machine state -- */

typedef enum { MODE_EVAL, MODE_RET } CekMode;

static CekMode        _mode;
static const LkExpr*  _expr;
static LkEnv*         _env;
static LkVal          _val;


/* -- Continuation stack -- */

#ifndef LARK_KONT_MAX
#  define LARK_KONT_MAX 2048
#endif

static LkFrame _kont[LARK_KONT_MAX];
static int     _ksp = 0;

static void kont_push(LkFrame f) {
    if (_ksp >= LARK_KONT_MAX) {
        fputs("lark: continuation stack overflow\n", stderr); exit(1);
    }
    _kont[_ksp++] = f;
}

static LkFrame kont_pop(void) { return _kont[--_ksp]; }


/* -- Collecting --
 *
 * Copy every object the roots reach into a new space, as Cheney does:
 * the roots first, each object they point to copied once; then the new
 * space is read from its start, each object's pointers copied in turn,
 * until the reading catches up with the copying.
 */

static char*  _from_start;
static size_t _from_used;
static char*  _to;
static size_t _to_used;

static int in_from(const void* p) {
    const char* c = p;
    return c >= _from_start && c < _from_start + _from_used;
}

/* Where the object at p is now: copied, if it was not already.
 * Pointers outside the old space, to string literals of the
 * program, say, are left as they are. */
static void* move(void* p) {
    if (!p || !in_from(p)) return p;
    Header* h = (Header*)p - 1;
    if (h->kind == OBJ_MOVED) return *(void**)p;
    Header* n = (Header*)(_to + _to_used);
    memcpy(n, h, sizeof(Header) + h->size);
    _to_used += sizeof(Header) + h->size;
    _copied += sizeof(Header) + h->size;
    h->kind = OBJ_MOVED;
    *(void**)p = n + 1;
    return n + 1;
}

static void move_val(LkVal* v) {
    switch (v->kind) {
        case V_STR:      v->s    = move((void*)v->s); break;
        case V_TUPLE:    v->tup  = move(v->tup);      break;
        case V_CON:      v->con  = move(v->con);      break;
        case V_PARTIAL:  v->part = move(v->part);     break;
        case V_CLOSURE:  v->clos = move(v->clos);     break;
        case V_PRINT_IO: v->pio  = move(v->pio);      break;
        default: break;     /* no pointer into the heap */
    }
}

static void move_vals(LkVal* v, int n) {
    for (int i = 0; i < n; i++) move_val(&v[i]);
}

static int   _grow;    /* did more than a quarter of the space survive? */
static char* _spare;   /* the other space, kept between collections */

static void collect(void) {
    size_t to_cap = _cap;
    /* if much survived last time, more room this time */
    if (_grow && _cap * 2 <= LARK_HEAP_MAX)
        to_cap = _cap * 2;
    _from_start = _heap;
    _from_used = _used;
    if (_spare && to_cap == _cap)
        _to = _spare;              /* the two spaces, in turn */
    else {
        free(_spare);
        _to = malloc(to_cap);
        if (!_to) { fputs("lark: out of memory\n", stderr); exit(1); }
    }
    _to_used = 0;

    /* the roots */
    move_val(&_val);
    _env = move(_env);
    for (int i = 0; i < _ksp; i++) {
        LkFrame* f = &_kont[i];
        f->env = move(f->env);
        if (f->kind == FRAME_APPLY_ARG)
            move_val(&f->apply_arg.fn_val);
        if (f->kind == FRAME_BINOP_R)
            move_val(&f->binop_r.left);
        if (f->kind == FRAME_TUPLE)
            f->tuple.tup = move(f->tuple.tup);
    }
    for (int i = 0; i < _top_n; i++)  move_val(&_top[i].val);
    for (int i = 0; i < _disp_n; i++) move_val(&_disp[i].impl);

    /* then everything they reach */
    for (size_t at = 0; at < _to_used; ) {
        Header* h = (Header*)(_to + at);
        void* o = h + 1;
        switch ((ObjKind)h->kind) {
            case OBJ_ENV: {
                LkEnv* e = o;
                move_val(&e->val);
                e->next = move(e->next);
                break;
            }
            case OBJ_TUPLE:   move_vals(((LkTuple*)o)->elems, ((LkTuple*)o)->n); break;
            case OBJ_CON:     move_vals(((LkCon*)o)->fields, ((LkCon*)o)->n); break;
            case OBJ_PARTIAL: move_vals(((LkPartCon*)o)->args, ((LkPartCon*)o)->n); break;
            case OBJ_CLOSURE: ((LkClosure*)o)->env = move(((LkClosure*)o)->env); break;
            case OBJ_BOX:     move_val((LkVal*)o); break;
            default: break;   /* a string holds no pointer */
        }
        at += sizeof(Header) + h->size;
    }

    if (to_cap == _cap)
        _spare = _heap;            /* kept, for the next collection */
    else {
        free(_heap);               /* too small now: the next space is new */
        _spare = NULL;
    }
    _heap = _to;
    _cap = to_cap;
    _used = _to_used;
    _collections++;
    _grow = _used > _cap / 4;
}

/* Between steps: collect if half the space is used, which allocate notes
 * in a flag. The test is marked as rarely true. Without that hint, clang
 * 21 at -O2 made the loop benchmark (bench/loop.lark) take 0.77 seconds,
 * where with it, it takes 0.62, as it did before there was a collector;
 * the collections themselves take almost none of either. */
static void maybe_collect(void) {
#ifdef LARK_COLLECT_ALWAYS
    /* for testing: collect before every step, so that a pointer the
     * collector did not know of is used at once after its object moved */
    _half_full = 1;
#endif
    if (__builtin_expect(_half_full, 0)) {
        if (_used > _peak) _peak = _used;
        collect();
        _half_full = _used > _cap / 2;
    }
}


/* -- Apply a function value to an argument -- */

/*
 * Applying to a closure sets _mode = MODE_EVAL and returns 0 (caller should
 * continue the main loop).  Applying to a builtin / partial / print-IO
 * returns 1 and places the result in _val (caller should set _mode=MODE_RET).
 *
 * The split avoids a recursive call to the main loop for the common case of
 * entering a closure body.  Multi-arg applications that produce intermediate
 * closures still call cek_run_until (below) for correctness.
 */
static int apply_val(LkVal fn, LkVal arg);   /* returns 1 if result in _val */

static int apply_val(LkVal fn, LkVal arg) {
    switch (fn.kind) {
        case V_CLOSURE: {
            LkClosure* c  = fn.clos;
            LkEnv*     e  = env_bind(c->env, c->param, arg);
            if (c->rec) e = env_bind(e, c->rec, fn);
            _mode = MODE_EVAL;
            _expr = c->body;
            _env  = e;
            return 0;
        }

        case V_PARTIAL: {
            LkPartCon* pc  = fn.part;
            int        n   = pc->n + 1;
            if (n > pc->arity) {
                fprintf(stderr,
                        "lark: constructor '%s' over-applied (%d/%d args)\n",
                        pc->tag, n, pc->arity);
                exit(1);
            }
            if (n == pc->arity) {
                LkCon* c = AR(OBJ_CON, sizeof(LkCon) + (size_t)n * sizeof(LkVal));
                c->tag = pc->tag; c->n = n;
                memcpy(c->fields, pc->args, (size_t)pc->n * sizeof(LkVal));
                c->fields[pc->n] = arg;
                _val = (LkVal){ .kind=V_CON, .con=c };
            } else {
                LkPartCon* nc = AR(OBJ_PARTIAL, sizeof(LkPartCon) + (size_t)n * sizeof(LkVal));
                nc->tag = pc->tag; nc->arity = pc->arity; nc->n = n;
                memcpy(nc->args, pc->args, (size_t)pc->n * sizeof(LkVal));
                nc->args[pc->n] = arg;
                _val = (LkVal){ .kind=V_PARTIAL, .part=nc };
            }
            return 1;
        }

        case V_BUILTIN:
            _val = apply_builtin((Builtin)fn.builtin, arg);
            return 1;

        case V_PRINT_IO:
            if (arg.kind != V_STR) {
                fputs("lark: print expects String\n", stderr); exit(1);
            }
            printf("%s\n", arg.s);
            _val = *fn.pio;
            return 1;

        case V_DISPATCH: {
            const char* tn   = val_type(arg);
            LkVal*      impl = disp_get(fn.method, tn);
            if (!impl) {
                fprintf(stderr, "lark: no impl of '%s' for '%s'\n",
                        fn.method, tn);
                exit(1);
            }
            return apply_val(*impl, arg);
        }

        default:
            fprintf(stderr, "lark: not a function (kind=%d)\n", fn.kind);
            exit(1);
    }
}


/* -- CEK main loop -- */

/*
 * Run until the continuation stack depth returns to `stop_sp` and the
 * machine is in MODE_RET.  Used both for the top-level run (stop_sp=0) and
 * for sub-computations inside multi-arg application (stop_sp = current depth
 * after the pending frame has been popped).
 */
static LkVal cek_run_until(int stop_sp) {
    for (;;) {
        if (_mode == MODE_RET && _ksp == stop_sp) return _val;
        maybe_collect();

        if (_mode == MODE_EVAL) {
            const LkExpr* e   = _expr;
            LkEnv*        env = _env;

            switch (e->kind) {

                case EXPR_LIT:
                    _mode = MODE_RET;
                    _val  = lit_val(e->lit);
                    break;

                case EXPR_VAR:
                case EXPR_CON:
                    _mode = MODE_RET;
                    _val  = env_lookup(env, e);
                    break;

                case EXPR_TUPLE:
                    if (e->tup.n == 0) {
                        _mode = MODE_RET; _val = lk_unit();
                    } else {
                        /* Pre-allocate the complete LkTuple (header + FAM) so that
                         * each FRAME_TUPLE pop writes directly into the final object —
                         * no per-element copies, no extra allocations. */
                        LkTuple* tup = AR(OBJ_TUPLE, sizeof(LkTuple) +
                                          (size_t)e->tup.n * sizeof(LkVal));
                        tup->n = e->tup.n;
                        /* Its elements come one by one; until then they are
                         * unit, so that a collection finds no stray pointer. */
                        for (int k = 0; k < tup->n; k++)
                            tup->elems[k] = lk_unit();
                        kont_push((LkFrame){
                            .kind  = FRAME_TUPLE, .env = env,
                            .tuple = { .remaining   = e->tup.elems + 1,
                                       .n_remaining = e->tup.n - 1,
                                       .tup         = tup,
                                       .n_done      = 0 }
                        });
                        _expr = e->tup.elems[0];
                    }
                    break;

                case EXPR_APPLY:
                    kont_push((LkFrame){
                        .kind     = FRAME_APPLY_FN, .env = env,
                        .apply_fn = { .args   = e->app.args,
                                      .n_args = e->app.n_args }
                    });
                    _expr = e->app.fn;
                    break;

                case EXPR_BINOP:
                    kont_push((LkFrame){
                        .kind    = FRAME_BINOP_L, .env = env,
                        .binop_l = { .op = e->binop.op, .code = e->binop.code,
                                     .right = e->binop.right }
                    });
                    _expr = e->binop.left;
                    break;

                case EXPR_UNARY:
                    kont_push((LkFrame){
                        .kind  = FRAME_UNARY,
                        .unary = { .op = e->unary.op, .code = e->unary.code }
                    });
                    _expr = e->unary.operand;
                    break;

                case EXPR_LET:
                    kont_push((LkFrame){
                        .kind = FRAME_LET, .env = env,
                        .let  = { .name = e->let.name, .body = e->let.body }
                    });
                    _expr = e->let.val;
                    break;

                case EXPR_IF:
                    kont_push((LkFrame){
                        .kind = FRAME_IF, .env = env,
                        .if_  = { .then_ = e->if_.then_, .else_ = e->if_.else_ }
                    });
                    _expr = e->if_.cond;
                    break;

                case EXPR_MATCH:
                    kont_push((LkFrame){
                        .kind  = FRAME_MATCH, .env = env,
                        .match = { .arms = e->match.arms, .n_arms = e->match.n_arms }
                    });
                    _expr = e->match.scrutinee;
                    break;

                case EXPR_LAMBDA:
                    _mode = MODE_RET;
                    _val  = lk_closure(e->lam.param, e->lam.body, env, NULL);
                    break;

                default:
                    fprintf(stderr, "lark: unknown expr kind %d\n", e->kind);
                    exit(1);
            }

        } else { /* MODE_RET — deliver _val to the top frame */
            LkFrame fr  = kont_pop();
            LkVal   val = _val;

            switch (fr.kind) {

                case FRAME_TUPLE: {
                    /* Write the just-evaluated element directly into the
                     * pre-allocated LkTuple (no memcpy, no extra allocation). */
                    fr.tuple.tup->elems[fr.tuple.n_done] = val;
                    int nd = fr.tuple.n_done + 1;
                    if (fr.tuple.n_remaining == 0) {
                        _mode = MODE_RET;
                        _val  = (LkVal){ .kind=V_TUPLE, .tup=fr.tuple.tup };
                    } else {
                        kont_push((LkFrame){
                            .kind  = FRAME_TUPLE, .env = fr.env,
                            .tuple = { .remaining   = fr.tuple.remaining + 1,
                                       .n_remaining = fr.tuple.n_remaining - 1,
                                       .tup         = fr.tuple.tup,
                                       .n_done      = nd }
                        });
                        _mode = MODE_EVAL;
                        _expr = fr.tuple.remaining[0];
                        _env  = fr.env;
                    }
                    break;
                }

                case FRAME_APPLY_FN:
                    /* val is the function; start on the first argument */
                    if (fr.apply_fn.n_args == 0) {
                        fputs("lark: internal error: application with zero arguments\n",
                              stderr);
                        exit(1);
                    }
                    kont_push((LkFrame){
                        .kind      = FRAME_APPLY_ARG, .env = fr.env,
                        .apply_arg = { .fn_val      = val,
                                       .remaining   = fr.apply_fn.args + 1,
                                       .n_remaining = fr.apply_fn.n_args - 1 }
                    });
                    _mode = MODE_EVAL;
                    _expr = fr.apply_fn.args[0];
                    _env  = fr.env;
                    break;

                case FRAME_APPLY_ARG:
                    if (fr.apply_arg.n_remaining == 0) {
                        /* Last argument — apply and stay in the loop. */
                        if (!apply_val(fr.apply_arg.fn_val, val))
                            continue;          /* closure entered; MODE_EVAL set */
                        _mode = MODE_RET;      /* builtin / partial returned _val */
                    } else {
                        /*
                         * An argument with more to come: f a b is (f a) b.
                         * Apply f to a; what that gives is a function, to be
                         * delivered to a frame that goes on with the rest of
                         * the arguments, as if (f a) were the function of a
                         * new application. (Lark's own machine ran the
                         * application to its end in a nested loop here, in
                         * C's own frame, where a collector could not see it.)
                         */
                        kont_push((LkFrame){
                            .kind     = FRAME_APPLY_FN, .env = fr.env,
                            .apply_fn = { .args   = fr.apply_arg.remaining,
                                          .n_args = fr.apply_arg.n_remaining }
                        });
                        if (!apply_val(fr.apply_arg.fn_val, val))
                            continue;          /* closure entered; MODE_EVAL set */
                        _mode = MODE_RET;      /* builtin / partial returned _val */
                    }
                    break;

                case FRAME_LET:
                    _mode = MODE_EVAL;
                    _expr = fr.let.body;
                    _env  = env_bind(fr.env, fr.let.name, val);
                    break;

                case FRAME_IF:
                    if (val.kind != V_BOOL) {
                        fputs("lark: if condition not Bool\n", stderr); exit(1);
                    }
                    _mode = MODE_EVAL;
                    _expr = val.b ? fr.if_.then_ : fr.if_.else_;
                    _env  = fr.env;
                    break;

                case FRAME_MATCH: {
                    int matched = 0;
                    for (int i = 0; i < fr.match.n_arms; i++) {
                        LkEnv* new_env = fr.env;
                        if (match_pat(fr.match.arms[i].pat, val, &new_env)) {
                            _mode = MODE_EVAL;
                            _expr = fr.match.arms[i].body;
                            _env  = new_env;
                            matched = 1;
                            break;
                        }
                    }
                    if (!matched) {
                        fputs("lark: non-exhaustive match\n", stderr); exit(1);
                    }
                    break;
                }

                case FRAME_BINOP_L:
                    kont_push((LkFrame){
                        .kind    = FRAME_BINOP_R,
                        .binop_r = { .op = fr.binop_l.op, .code = fr.binop_l.code,
                                     .left = val }
                    });
                    _mode = MODE_EVAL;
                    _expr = fr.binop_l.right;
                    _env  = fr.env;
                    break;

                case FRAME_BINOP_R:
                    _mode = MODE_RET;
                    _val  = binop(fr.binop_r.code, fr.binop_r.op, fr.binop_r.left, val);
                    break;

                case FRAME_UNARY:
                    _mode = MODE_RET;
                    _val  = unaryop(fr.unary.code, fr.unary.op, val);
                    break;

                default:
                    fprintf(stderr, "lark: unknown frame kind %d\n", fr.kind);
                    exit(1);
            }
        }
    }
}


/* -- Program evaluation -- */

/* Register built-in constructors and names shared by all programs. */
static void register_builtins(void) {
    con_register("Nil",  "List",   0);
    con_register("Cons", "List",   2);
    con_register("Ok",   "Result", 1);
    con_register("Err",  "Result", 1);

    top_set("print",          lk_builtin(B_PRINT));
    top_set("read",           lk_builtin(B_READ));
    top_set("show",           lk_builtin(B_SHOW));
    top_set("int_to_float",   lk_builtin(B_INT_TO_FLOAT));
    top_set("float_to_int",   lk_builtin(B_FLOAT_TO_INT));
    top_set("int_to_string",  lk_builtin(B_INT_TO_STRING));
    top_set("float_to_string",lk_builtin(B_FLOAT_TO_STRING));
    top_set("int_abs",        lk_builtin(B_INT_ABS));
    top_set("float_abs",      lk_builtin(B_FLOAT_ABS));
    top_set("float_sqrt",     lk_builtin(B_FLOAT_SQRT));
    top_set("float_floor",    lk_builtin(B_FLOAT_FLOOR));
    top_set("float_ceil",     lk_builtin(B_FLOAT_CEIL));
    top_set("string_length",  lk_builtin(B_STRING_LENGTH));
    top_set("Nil",  lk_con("Nil", NULL, 0));
    top_set("Cons", lk_partial("Cons", 2, NULL, 0));
    top_set("Ok",   lk_partial("Ok",  1, NULL, 0));
    top_set("Err",  lk_partial("Err", 1, NULL, 0));
    top_set("True",  lk_bool(1));
    top_set("False", lk_bool(0));
}

static void eval_prog(const LkProg* prog) {
    for (int i = 0; i < prog->n_decls; i++) {
        const LkDecl* d = prog->decls[i];
        switch (d->kind) {

            case DECL_FN:
                /* Top-level closures capture NULL local env; lookups fall
                 * through to top_env so mutual recursion works without
                 * any backpatching. */
                top_set(d->name, lk_closure(d->fn.param, d->fn.body,
                                            NULL, d->name));
                break;

            case DECL_LET:
                _mode = MODE_EVAL; _expr = d->let_val; _env = NULL;
                top_set(d->name, cek_run_until(0));
                break;

            case DECL_TYPE:
                for (int j = 0; j < d->type_.n_variants; j++) {
                    const LkVariant* v = &d->type_.variants[j];
                    con_register(v->name, d->name, v->arity);
                    LkVal cv = v->arity == 0
                        ? lk_con(v->name, NULL, 0)
                        : lk_partial(v->name, v->arity, NULL, 0);
                    top_set(v->name, cv);
                }
                break;

            case DECL_IMPL:
                for (int j = 0; j < d->impl.n_methods; j++) {
                    const LkMethod* m = &d->impl.methods[j];
                    LkVal closure = lk_closure(m->param, m->body, NULL, m->name);
                    disp_set(m->name, d->name, closure);
                    if (!top_get(m->name))
                        top_set(m->name, lk_dispatch(m->name));
                }
                break;
        }
    }
}


/* -- Entry point -- */

void cek_run(const LkProg* prog) {
    _cap  = LARK_HEAP_START;
    _heap = malloc(_cap);
    if (!_heap) { fputs("lark: out of memory\n", stderr); exit(1); }
    _used = 0;
    _ksp  = 0;
    _top_n = 0;
    _disp_n = 0;
    _con_n  = 0;

    register_builtins();
    eval_prog(prog);

    LkVal* main_fn = top_get("main");
    if (!main_fn) {
        fputs("lark: no main\n", stderr); exit(1);
    }

    /* Call main(io) */
    if (!apply_val(*main_fn, lk_io())) {
        cek_run_until(0);
    }

    if (getenv("LARK_STATS"))
        fprintf(stderr, "lark: %zu collections, %zu bytes copied, "
                "heap at most %zu bytes of %zu\n", _collections, _copied, _peak, _cap);
}
