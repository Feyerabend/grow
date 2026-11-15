/*
 * Reading a class file, JVMS 4.1 to 4.7, with the checks of its format that
 * the specification asks for before verification (4.8): the magic number,
 * the version, a constant pool whose entries are what they claim, and
 * attributes that do not run past their end.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "jvm.h"

char jvm_error[300];

typedef struct {
    const uint8_t *p, *end;
    int bad;
} Reader;

static unsigned u1(Reader *r) {
    if (r->p + 1 > r->end) { r->bad = 1; return 0; }
    return *r->p++;
}

static unsigned u2(Reader *r) {
    if (r->p + 2 > r->end) { r->bad = 1; return 0; }
    unsigned v = (unsigned)r->p[0] << 8 | r->p[1];
    r->p += 2;
    return v;
}

static uint32_t u4(Reader *r) {
    if (r->p + 4 > r->end) { r->bad = 1; return 0; }
    uint32_t v = (uint32_t)r->p[0] << 24 | (uint32_t)r->p[1] << 16 |
                 (uint32_t)r->p[2] << 8 | r->p[3];
    r->p += 4;
    return v;
}

static int fail(const char *message, const char *detail) {
    snprintf(jvm_error, sizeof jvm_error, "java.lang.ClassFormatError: %s%s",
             message, detail ? detail : "");
    return 0;
}

const char *cp_utf8(const Class *c, int i) {
    if (i < 1 || i >= c->count || c->pool[i].tag != CP_UTF8)
        return NULL;
    return c->pool[i].utf8;
}

const char *cp_class_name(const Class *c, int i) {
    if (i < 1 || i >= c->count || c->pool[i].tag != CP_CLASS)
        return NULL;
    return cp_utf8(c, c->pool[i].a);
}

/* A Fieldref or Methodref: its class, name and descriptor. */
int cp_member(const Class *c, int i, int tag,
              const char **cls, const char **name, const char **descriptor) {
    if (i < 1 || i >= c->count || c->pool[i].tag != tag)
        return 0;
    const Constant *k = &c->pool[i];
    *cls = cp_class_name(c, k->a);
    if (k->b < 1 || k->b >= c->count || c->pool[k->b].tag != CP_NAME_AND_TYPE)
        return 0;
    *name = cp_utf8(c, c->pool[k->b].a);
    *descriptor = cp_utf8(c, c->pool[k->b].b);
    return *cls && *name && *descriptor;
}

Method *find_method(Class *c, const char *name, const char *descriptor) {
    for (int i = 0; i < c->nmethods; i++)
        if (!strcmp(c->methods[i].name, name) &&
            !strcmp(c->methods[i].descriptor, descriptor))
            return &c->methods[i];
    return NULL;
}

Field *find_field(Class *c, const char *name, const char *descriptor) {
    for (int i = 0; i < c->nfields; i++)
        if (!strcmp(c->fields[i].name, name) &&
            !strcmp(c->fields[i].descriptor, descriptor))
            return &c->fields[i];
    return NULL;
}

/* The source line of an instruction, from the LineNumberTable: the entry
 * with the greatest start_pc not after pc. 0 if there is none. */
int line_of(const Method *m, int pc) {
    int line = 0, best = -1;
    for (int i = 0; i < m->nlines; i++)
        if (m->lines[i].start_pc <= pc && m->lines[i].start_pc > best) {
            best = m->lines[i].start_pc;
            line = m->lines[i].line;
        }
    return line;
}

/* The slots a method's arguments take, and what it returns; 0 if the
 * descriptor is not one (4.3.3). */
static int parse_descriptor(Method *m) {
    const char *d = m->descriptor;
    int n = (m->access & 0x0008) ? 0 : 1;       /* ACC_STATIC */
    if (*d++ != '(')
        return 0;
    while (*d && *d != ')') {
        while (*d == '[')
            d++;
        if (*d == 'L') {
            d = strchr(d, ';');
            if (!d)
                return 0;
        } else if (!strchr("BCDFIJSZ", *d))
            return 0;
        n += (*d == 'J' || *d == 'D') && d[-1] != '[' ? 2 : 1;
        d++;
    }
    if (*d++ != ')')
        return 0;
    m->nargs = n;
    m->returns = *d == 'V' ? 'V' : *d == 'L' || *d == '[' ? 'L' : *d;
    return 1;
}

static int read_code(Class *c, Method *m, Reader *r, uint32_t length) {
    Reader a = { r->p, r->p + length, 0 };
    r->p += length;
    m->max_stack = u2(&a);
    m->max_locals = u2(&a);
    m->code_length = u4(&a);
    if (a.bad || m->code_length == 0 || m->code_length >= 65536 ||
        a.p + m->code_length > a.end)
        return fail("bad code length in method ", m->name);
    m->code = a.p;
    a.p += m->code_length;
    m->exceptions = u2(&a);
    a.p += 8 * m->exceptions;
    unsigned nattributes = u2(&a);
    for (unsigned i = 0; i < nattributes && !a.bad; i++) {
        const char *name = cp_utf8(c, u2(&a));
        uint32_t len = u4(&a);
        if (!name || a.p + len > a.end)
            return fail("bad attribute in the code of ", m->name);
        Reader b = { a.p, a.p + len, 0 };
        if (!strcmp(name, "StackMapTable")) {
            if (m->stackmap)
                return fail("more than one StackMapTable in ", m->name);
            m->frames = u2(&b);
            m->stackmap = b.p;
            m->stackmap_length = len - 2;
        } else if (!strcmp(name, "LineNumberTable")) {
            int n = u2(&b);
            m->lines = realloc(m->lines, (m->nlines + n) * sizeof *m->lines);
            for (int k = 0; k < n; k++) {
                m->lines[m->nlines].start_pc = u2(&b);
                m->lines[m->nlines++].line = u2(&b);
            }
        }
        if (b.bad)
            return fail("truncated attribute in ", m->name);
        a.p += len;
    }
    if (a.bad || a.p != a.end)
        return fail("bad Code attribute in ", m->name);
    return 1;
}

static int read_members(Class *c, Reader *r, int methods) {
    int n = u2(r);
    if (methods) {
        c->nmethods = n;
        c->methods = calloc(n ? n : 1, sizeof *c->methods);
    } else {
        c->nfields = n;
        c->fields = calloc(n ? n : 1, sizeof *c->fields);
    }
    for (int i = 0; i < n && !r->bad; i++) {
        unsigned access = u2(r);
        const char *name = cp_utf8(c, u2(r));
        const char *descriptor = cp_utf8(c, u2(r));
        if (!name || !descriptor)
            return fail("bad name or descriptor of a member", NULL);
        Method *m = methods ? &c->methods[i] : NULL;
        if (m) {
            m->access = access;
            m->name = name;
            m->descriptor = descriptor;
            if (!parse_descriptor(m))
                return fail("bad method descriptor ", descriptor);
        } else {
            c->fields[i].access = access;
            c->fields[i].name = name;
            c->fields[i].descriptor = descriptor;
        }
        unsigned nattributes = u2(r);
        int code = 0;
        for (unsigned k = 0; k < nattributes && !r->bad; k++) {
            const char *aname = cp_utf8(c, u2(r));
            uint32_t len = u4(r);
            if (!aname || r->p + len > r->end)
                return fail("bad attribute of ", name);
            if (m && !strcmp(aname, "Code")) {
                if (code++)
                    return fail("more than one Code attribute in ", name);
                if (!read_code(c, m, r, len))
                    return 0;
            } else
                r->p += len;
        }
        /* A native or abstract method has no Code attribute, and every
         * other method has one (4.7.3); abstract is never static (4.6). */
        if (m && !code != !!(access & 0x0500))
            return fail(code ? "Code attribute in a native or abstract method "
                             : "no Code attribute in ", name);
        if (m && (access & 0x0400) && (access & 0x0008))
            return fail("illegal modifiers on method ", name);
    }
    return !r->bad;
}

Class *load_class(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) {
        snprintf(jvm_error, sizeof jvm_error, "cannot open %s", path);
        return NULL;
    }
    Class *c = calloc(1, sizeof *c);
    size_t cap = 1 << 16;
    c->bytes = malloc(cap);
    size_t got;
    while ((got = fread(c->bytes + c->size, 1, cap - c->size, f)) > 0)
        if ((c->size += got) == cap)
            c->bytes = realloc(c->bytes, cap *= 2);
    fclose(f);

    Reader r = { c->bytes, c->bytes + c->size, 0 };
    if (u4(&r) != 0xCAFEBABE) {
        fail("incompatible magic value", NULL);
        return NULL;
    }
    c->minor = u2(&r);
    c->major = u2(&r);
    /* Class files from Java SE 6 (version 50) to Java SE 21 (65): the ones
     * that are verified by type checking (4.10.1), in the edition read. */
    if (r.bad || c->major < 50 || c->major > 65 ||
        (c->major >= 56 && c->minor != 0)) {
        snprintf(jvm_error, sizeof jvm_error,
                 "java.lang.UnsupportedClassVersionError: version %u.%u, "
                 "where this machine takes 50.0 to 65.0", c->major, c->minor);
        return NULL;
    }
    c->count = u2(&r);
    if (c->count == 0) {
        fail("empty constant pool", NULL);
        return NULL;
    }
    c->pool = calloc(c->count, sizeof *c->pool);
    for (int i = 1; i < c->count && !r.bad; i++) {
        Constant *k = &c->pool[i];
        k->tag = u1(&r);
        switch (k->tag) {
        case CP_UTF8: {
            unsigned len = u2(&r);
            if (r.p + len > r.end) { r.bad = 1; break; }
            char *s = malloc(len + 1);
            memcpy(s, r.p, len);
            s[len] = 0;
            r.p += len;
            k->utf8 = s;
            break;
        }
        case CP_INTEGER: k->value = (int32_t)u4(&r); break;
        case CP_FLOAT: u4(&r); break;
        case CP_LONG: case CP_DOUBLE:   /* take two entries, 4.4.5 */
            u4(&r); u4(&r); i++; break;
        case CP_CLASS: case CP_STRING: case CP_METHOD_TYPE:
        case CP_MODULE: case CP_PACKAGE:
            k->a = u2(&r); break;
        case CP_FIELDREF: case CP_METHODREF: case CP_INTERFACE_METHODREF:
        case CP_NAME_AND_TYPE: case CP_DYNAMIC: case CP_INVOKE_DYNAMIC:
            k->a = u2(&r); k->b = u2(&r); break;
        case CP_METHOD_HANDLE: k->a = u1(&r); k->b = u2(&r); break;
        default:
            snprintf(jvm_error, sizeof jvm_error,
                     "java.lang.ClassFormatError: unknown constant tag %d at %d",
                     k->tag, i);
            return NULL;
        }
    }
    /* Each entry must name entries of the right kinds (4.4). */
    for (int i = 1; i < c->count; i++) {
        Constant *k = &c->pool[i];
        const char *x, *y, *z;
        int ok = 1;
        switch (k->tag) {
        case CP_CLASS: case CP_STRING: ok = cp_utf8(c, k->a) != NULL; break;
        case CP_NAME_AND_TYPE: ok = cp_utf8(c, k->a) && cp_utf8(c, k->b); break;
        case CP_FIELDREF: case CP_METHODREF: case CP_INTERFACE_METHODREF:
            ok = cp_member(c, i, k->tag, &x, &y, &z); break;
        }
        if (!ok) {
            snprintf(jvm_error, sizeof jvm_error,
                     "java.lang.ClassFormatError: bad constant pool entry %d", i);
            return NULL;
        }
    }
    c->access = u2(&r);
    c->name = cp_class_name(c, u2(&r));
    unsigned super = u2(&r);
    c->super = super ? cp_class_name(c, super) : NULL;
    if (!c->name || (super && !c->super)) {
        fail("bad this_class or super_class", NULL);
        return NULL;
    }
    unsigned ninterfaces = u2(&r);
    r.p += 2 * ninterfaces;
    if (!read_members(c, &r, 0) || !read_members(c, &r, 1))
        return r.bad ? (fail("truncated class file", NULL), NULL) : NULL;
    unsigned nattributes = u2(&r);
    for (unsigned i = 0; i < nattributes && !r.bad; i++) {
        const char *name = cp_utf8(c, u2(&r));
        uint32_t len = u4(&r);
        if (!name || r.p + len > r.end) { r.bad = 1; break; }
        if (!strcmp(name, "SourceFile")) {
            Reader s = { r.p, r.p + len, 0 };
            if (len != 2 || !(c->source = cp_utf8(c, u2(&s)))) {
                fail("invalid SourceFile attribute", NULL);
                return NULL;
            }
        }
        r.p += len;
    }
    if (r.bad) {
        fail("truncated class file", NULL);
        return NULL;
    }
    if (r.p != r.end) {
        fail("extra bytes at the end of the class file", NULL);
        return NULL;
    }
    c->resolved = calloc(c->count, sizeof *c->resolved);
    return c;
}
