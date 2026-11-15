/*
 * A WebAssembly 1.0 machine. See wasm.h.
 *
 * Written from the WebAssembly Core Specification, W3C Recommendation,
 * 5 December 2019, https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/
 * Copyright (c) 2019 W3C (MIT, ERCIM, Keio, Beihang). This software
 * includes material derived from that document. The section numbers in
 * the comments are the specification's.
 *
 * Four parts, as the specification has them: decoding the binary format
 * (5), validation (3), instantiation (4.5) and execution (4.4).
 */

#include "wasm.h"

#include <math.h>
#include <setjmp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

uint64_t wasm_steps, wasm_calls;

/* ---------------------------------------------------------------- */
/* Failing. Decoding and validation stop at the first thing wrong, by a
 * jump back to where they began; so does a trap. */

static jmp_buf failed;
static const char *failure;

__attribute__((noreturn)) static void fail(const char *message)
{
    failure = message;
    longjmp(failed, 1);
}

static void *grow(void *p, size_t n, size_t size)
{
    void *q = realloc(p, n * size ? n * size : 1);
    if (!q) {
        fprintf(stderr, "wasm: out of memory\n");
        exit(2);
    }
    return q;
}

/* ---------------------------------------------------------------- */
/* 5.2 Values in the binary format. */

typedef struct { const uint8_t *p, *end; } Reader;

static uint8_t byte(Reader *r)
{
    if (r->p >= r->end)
        fail("unexpected end");
    return *r->p++;
}

/* An unsigned LEB128 number of at most n bits: at most ceil(n/7) bytes,
 * and in the last of them no bit set beyond the n. */
static uint64_t unsigned_leb(Reader *r, unsigned n)
{
    uint64_t x = 0;
    unsigned shift = 0, most = (n + 6) / 7;
    for (unsigned i = 0;; i++) {
        uint8_t b = byte(r);
        if (i == most - 1) {
            if (b & 0x80)
                fail("integer representation too long");
            unsigned used = n - shift;
            if (used < 7 && (b >> used) != 0)
                fail("integer too large");
            return x | (uint64_t)b << shift;
        }
        x |= (uint64_t)(b & 0x7F) << shift;
        shift += 7;
        if (!(b & 0x80))
            return x;
    }
}

/* A signed one: in the last byte, the bits beyond the n must all be
 * copies of the sign. */
static int64_t signed_leb(Reader *r, unsigned n)
{
    uint64_t x = 0;
    unsigned shift = 0, most = (n + 6) / 7;
    for (unsigned i = 0;; i++) {
        uint8_t b = byte(r);
        if (i == most - 1) {
            if (b & 0x80)
                fail("integer representation too long");
            unsigned used = n - shift;
            if (used < 7) {
                unsigned sign = (b >> (used - 1)) & 1;
                unsigned rest = (b & 0x7F) >> used;
                if (rest != (sign ? 0x7Fu >> used : 0))
                    fail("integer too large");
            }
        }
        x |= (uint64_t)(b & 0x7F) << shift;
        shift += 7;
        if (!(b & 0x80)) {
            if (shift < 64 && (b & 0x40))
                x |= ~(uint64_t)0 << shift;
            return (int64_t)x;
        }
    }
}

static uint32_t u32(Reader *r) { return (uint32_t)unsigned_leb(r, 32); }

/* A vector's length. A vector of things of at least one byte cannot be
 * longer than what is left. */
static uint32_t length(Reader *r)
{
    uint32_t n = u32(r);
    if (n > (size_t)(r->end - r->p))
        fail("length out of bounds");
    return n;
}

/* A name: a vector of bytes that must be UTF-8 (5.2.4). */
static int utf8(const uint8_t *s, uint32_t n)
{
    for (uint32_t i = 0; i < n;) {
        uint8_t c = s[i];
        uint32_t k, cp;
        if (c < 0x80) { i++; continue; }
        else if (c >= 0xC2 && c <= 0xDF) { k = 1; cp = c & 0x1F; }
        else if (c >= 0xE0 && c <= 0xEF) { k = 2; cp = c & 0x0F; }
        else if (c >= 0xF0 && c <= 0xF4) { k = 3; cp = c & 0x07; }
        else return 0;
        for (uint32_t j = 1; j <= k; j++) {
            if (i + j >= n || (s[i + j] & 0xC0) != 0x80)
                return 0;
            cp = cp << 6 | (s[i + j] & 0x3F);
        }
        if ((k == 2 && cp < 0x800) || (k == 3 && (cp < 0x10000 || cp > 0x10FFFF)) ||
            (cp >= 0xD800 && cp <= 0xDFFF))
            return 0;
        i += k + 1;
    }
    return 1;
}

static Name name(Reader *r)
{
    uint32_t n = length(r);
    if (!utf8(r->p, n))
        fail("malformed UTF-8 encoding");
    Name x = {grow(NULL, n + 1, 1), n};
    memcpy(x.s, r->p, n);
    x.s[n] = 0;
    r->p += n;
    return x;
}

static int same_name(Name a, const char *s, uint32_t len)
{
    return a.len == len && memcmp(a.s, s, len) == 0;
}

static uint8_t valtype(Reader *r)
{
    uint8_t t = byte(r);
    if (t != I32 && t != I64 && t != F32 && t != F64)
        fail("malformed value type");
    return t;
}

static Limits limits(Reader *r)
{
    Limits l = {0, 0, 0};
    uint8_t flag = byte(r);
    if (flag > 1)
        fail("integer too large");
    l.min = u32(r);
    if (flag) {
        l.has_max = 1;
        l.max = u32(r);
    }
    return l;
}

/* ---------------------------------------------------------------- */
/* 5.4 Instructions: read only for their form here. Validation reads them
 * again for their types. */

/* Instructions with no immediates, past the control ones: 0x45 to 0xBF,
 * and drop, select. */
static int plain(uint8_t op) { return (op >= 0x45 && op <= 0xBF) || op == 0x1A || op == 0x1B; }

/* Read one expression, to its final end, checking every instruction is
 * one of 1.0's and its immediates well formed. */
static void expression(Reader *r)
{
    uint32_t depth = 0;
    for (;;) {
        uint8_t op = byte(r);
        if (plain(op) || op == 0x00 || op == 0x01 || op == 0x05 || op == 0x0F)
            continue;
        switch (op) {
        case 0x02: case 0x03: case 0x04: {
            uint8_t bt = byte(r);
            if (bt != 0x40 && bt != I32 && bt != I64 && bt != F32 && bt != F64)
                fail("malformed block type");
            depth++;
            break;
        }
        case 0x0B:
            if (depth-- == 0)
                return;
            break;
        case 0x0C: case 0x0D: case 0x10: case 0x20: case 0x21: case 0x22:
        case 0x23: case 0x24:
            u32(r);
            break;
        case 0x0E: {
            uint32_t n = length(r);
            for (uint32_t i = 0; i <= n; i++)
                u32(r);
            break;
        }
        case 0x11:
            u32(r);
            if (byte(r) != 0)
                fail("zero flag expected");
            break;
        case 0x3F: case 0x40:
            if (byte(r) != 0)
                fail("zero flag expected");
            break;
        case 0x41: signed_leb(r, 32); break;
        case 0x42: signed_leb(r, 64); break;
        case 0x43: for (int i = 0; i < 4; i++) byte(r); break;
        case 0x44: for (int i = 0; i < 8; i++) byte(r); break;
        default:
            if (op >= 0x28 && op <= 0x3E) {     /* memarg: align, offset */
                u32(r);
                u32(r);
                break;
            }
            fail("illegal opcode");
        }
    }
}

/* ---------------------------------------------------------------- */
/* 5.5 Modules. */

static void import_section(Reader *r, Module *m)
{
    uint32_t n = length(r);
    m->imports = grow(NULL, n, sizeof(Import));
    m->nimports = n;
    for (uint32_t i = 0; i < n; i++) {
        Import *im = &m->imports[i];
        memset(im, 0, sizeof *im);
        im->module = name(r);
        im->name = name(r);
        im->kind = byte(r);
        switch (im->kind) {
        case EXT_FUNC: im->type = u32(r); m->nfuncimports++; break;
        case EXT_TABLE:
            if (byte(r) != 0x70)
                fail("malformed element type");
            im->limits = limits(r);
            m->ntableimports++;
            break;
        case EXT_MEM: im->limits = limits(r); m->nmemimports++; break;
        case EXT_GLOBAL:
            im->valtype = valtype(r);
            im->mut = byte(r);
            if (im->mut > 1)
                fail("malformed mutability");
            m->nglobalimports++;
            break;
        default:
            fail("malformed import kind");
        }
    }
}

static void section(Reader *r, Module *m, uint8_t id)
{
    uint32_t n;
    switch (id) {
    case 1:     /* types */
        n = length(r);
        m->types = grow(NULL, n, sizeof(FuncType));
        m->ntypes = n;
        for (uint32_t i = 0; i < n; i++) {
            FuncType *t = &m->types[i];
            if (byte(r) != 0x60)
                fail("integer representation too long");
            t->nparams = length(r);
            t->params = grow(NULL, t->nparams, 1);
            for (uint32_t j = 0; j < t->nparams; j++)
                t->params[j] = valtype(r);
            t->nresults = length(r);
            for (uint32_t j = 0; j < t->nresults; j++)
                t->result = valtype(r);     /* validation allows one */
        }
        break;
    case 2:
        import_section(r, m);
        break;
    case 3:     /* functions: a type index for each */
        n = length(r);
        m->funcs = grow(NULL, n, sizeof(uint32_t));
        m->nfuncs = n;
        for (uint32_t i = 0; i < n; i++)
            m->funcs[i] = u32(r);
        break;
    case 4:
        n = length(r);
        m->tables = grow(NULL, n, sizeof(Limits));
        m->ntables = n;
        for (uint32_t i = 0; i < n; i++) {
            if (byte(r) != 0x70)
                fail("malformed element type");
            m->tables[i] = limits(r);
        }
        break;
    case 5:
        n = length(r);
        m->mems = grow(NULL, n, sizeof(Limits));
        m->nmems = n;
        for (uint32_t i = 0; i < n; i++)
            m->mems[i] = limits(r);
        break;
    case 6:
        n = length(r);
        m->globals = grow(NULL, n, sizeof(Global));
        m->nglobals = n;
        for (uint32_t i = 0; i < n; i++) {
            Global *g = &m->globals[i];
            g->valtype = valtype(r);
            g->mut = byte(r);
            if (g->mut > 1)
                fail("malformed mutability");
            g->init = r->p;
            expression(r);
            g->init_len = (size_t)(r->p - g->init);
        }
        break;
    case 7:
        n = length(r);
        m->exports = grow(NULL, n, sizeof(Export));
        m->nexports = n;
        for (uint32_t i = 0; i < n; i++) {
            m->exports[i].name = name(r);
            m->exports[i].kind = byte(r);
            if (m->exports[i].kind > EXT_GLOBAL)
                fail("malformed export kind");
            m->exports[i].index = u32(r);
        }
        break;
    case 8:
        m->start = u32(r);
        break;
    case 9:
        n = length(r);
        m->elems = grow(NULL, n, sizeof(Elem));
        m->nelems = n;
        for (uint32_t i = 0; i < n; i++) {
            Elem *e = &m->elems[i];
            e->table = u32(r);
            e->offset = r->p;
            expression(r);
            e->offset_len = (size_t)(r->p - e->offset);
            e->count = length(r);
            e->funcs = grow(NULL, e->count, sizeof(uint32_t));
            for (uint32_t j = 0; j < e->count; j++)
                e->funcs[j] = u32(r);
        }
        break;
    case 10:    /* code: each function's locals and body */
        n = length(r);
        m->codes = grow(NULL, n, sizeof(Code));
        m->ncodes = n;
        for (uint32_t i = 0; i < n; i++) {
            Code *c = &m->codes[i];
            memset(c, 0, sizeof *c);
            uint32_t size = length(r);
            Reader body = {r->p, r->p + size};
            uint32_t groups = length(&body);
            uint64_t total = 0;
            const uint8_t *start = body.p;
            for (uint32_t j = 0; j < groups; j++) {     /* first, count them */
                total += u32(&body);
                if (total > 0xFFFFFFFFu)
                    fail("too many locals");
                valtype(&body);
            }
            c->nlocals = (uint32_t)total;
            c->locals = grow(NULL, c->nlocals, 1);
            body.p = start;
            for (uint32_t j = 0, k = 0; j < groups; j++) {
                uint32_t count = u32(&body);
                uint8_t t = valtype(&body);
                memset(c->locals + k, t, count);
                k += count;
            }
            c->body = body.p;
            expression(&body);
            if (body.p != body.end)
                fail("section size mismatch");
            c->len = (size_t)(body.p - c->body);
            r->p = body.end;
        }
        break;
    case 11:
        n = length(r);
        m->datas = grow(NULL, n, sizeof(Data));
        m->ndatas = n;
        for (uint32_t i = 0; i < n; i++) {
            Data *d = &m->datas[i];
            d->mem = u32(r);
            d->offset = r->p;
            expression(r);
            d->offset_len = (size_t)(r->p - d->offset);
            d->len = length(r);
            d->bytes = r->p;
            r->p += d->len;
        }
        break;
    }
}

const char *wasm_decode(Module *m, const uint8_t *bytes, size_t size)
{
    memset(m, 0, sizeof *m);
    m->start = -1;
    m->bytes = grow(NULL, size, 1);
    memcpy(m->bytes, bytes, size);
    m->size = size;
    if (setjmp(failed))
        return failure;
    Reader r = {m->bytes, m->bytes + size};
    static const uint8_t magic[4] = {0x00, 0x61, 0x73, 0x6D};
    static const uint8_t version[4] = {0x01, 0x00, 0x00, 0x00};
    for (int i = 0; i < 4; i++)
        if (byte(&r) != magic[i])
            fail("magic header not detected");
    for (int i = 0; i < 4; i++)
        if (byte(&r) != version[i])
            fail("unknown binary version");
    int last = 0, saw_funcs = 0, saw_code = 0;
    while (r.p < r.end) {
        uint8_t id = byte(&r);
        uint32_t size = u32(&r);
        if (size > (size_t)(r.end - r.p))
            fail("section size mismatch");
        Reader s = {r.p, r.p + size};
        if (id == 0)            /* custom: a name, then anything */
            name(&s);
        else {
            if (id > 11)
                fail("malformed section id");
            if (id <= last)
                fail("junk after last section");    /* out of order, or twice */
            last = id;
            saw_funcs |= id == 3;
            saw_code |= id == 10;
            section(&s, m, id);
            if (s.p != s.end)
                fail("section size mismatch");
        }
        r.p += size;
    }
    if (m->nfuncs != m->ncodes)
        fail("function and code section have inconsistent lengths");
    (void)saw_funcs;
    (void)saw_code;
    return NULL;
}

/* ---------------------------------------------------------------- */
/* 3 Validation, by the algorithm of the specification's appendix (7.3):
 * a stack of the operands' types, and a stack of control frames. */

enum { UNKNOWN = 0 };

typedef struct {
    uint8_t label, end;         /* the label's type and the end's: 0 for none */
    uint32_t height;
    int unreachable;
    uint8_t opcode;             /* block, loop or if; else once seen */
    uint32_t start;             /* the block's offset in the body */
} Ctrl;

typedef struct {
    Module *m;
    FuncType **funcs;           /* every function's type, imports first */
    uint8_t *gtypes, *gmuts;    /* every global's */
    uint32_t nglobals, ntables, nmems;
    uint8_t *opds; uint32_t nopds, capopds, maxopds;
    Ctrl *ctrls; uint32_t nctrls, capctrls;
    uint8_t *locals; uint32_t nlocals;
    uint8_t result;             /* the function's, or 0 */
} Context;

static void push_opd(Context *c, uint8_t t)
{
    if (c->nopds == c->capopds) {
        c->capopds = c->capopds ? c->capopds * 2 : 64;
        c->opds = grow(c->opds, c->capopds, 1);
    }
    c->opds[c->nopds++] = t;
    if (c->nopds > c->maxopds)
        c->maxopds = c->nopds;
}

static uint8_t pop_any(Context *c)
{
    Ctrl *top = &c->ctrls[c->nctrls - 1];
    if (c->nopds == top->height && top->unreachable)
        return UNKNOWN;
    if (c->nopds == top->height)
        fail("type mismatch");
    return c->opds[--c->nopds];
}

static uint8_t pop_opd(Context *c, uint8_t expect)
{
    uint8_t actual = pop_any(c);
    if (actual == UNKNOWN)
        return expect;
    if (expect == UNKNOWN)
        return actual;
    if (actual != expect)
        fail("type mismatch");
    return actual;
}

static void push_ctrl(Context *c, uint8_t op, uint32_t start, uint8_t label, uint8_t end)
{
    if (c->nctrls == c->capctrls) {
        c->capctrls = c->capctrls ? c->capctrls * 2 : 16;
        c->ctrls = grow(c->ctrls, c->capctrls, sizeof(Ctrl));
    }
    c->ctrls[c->nctrls++] = (Ctrl){label, end, c->nopds, 0, op, start};
}

static Ctrl pop_ctrl(Context *c)
{
    if (c->nctrls == 0)
        fail("type mismatch");
    Ctrl f = c->ctrls[c->nctrls - 1];
    if (f.end)
        pop_opd(c, f.end);
    if (c->nopds != f.height)
        fail("type mismatch");
    c->nctrls--;
    return f;
}

static void unreachable(Context *c)
{
    c->nopds = c->ctrls[c->nctrls - 1].height;
    c->ctrls[c->nctrls - 1].unreachable = 1;
}

/* The label of the frame n out from the innermost: its type, 0 for none. */
static uint8_t label_type(Context *c, uint32_t n)
{
    if (n >= c->nctrls)
        fail("unknown label");
    return c->ctrls[c->nctrls - 1 - n].label;
}

/* The types of the numeric instructions, 0x45 to 0xBF: the operands'
 * type, how many, and the result's. */
typedef struct { uint8_t in, n, out; } Sig;

static Sig numeric(uint8_t op)
{
    if (op == 0x45) return (Sig){I32, 1, I32};
    if (op <= 0x4F) return (Sig){I32, 2, I32};
    if (op == 0x50) return (Sig){I64, 1, I32};
    if (op <= 0x5A) return (Sig){I64, 2, I32};
    if (op <= 0x60) return (Sig){F32, 2, I32};
    if (op <= 0x66) return (Sig){F64, 2, I32};
    if (op <= 0x69) return (Sig){I32, 1, I32};
    if (op <= 0x78) return (Sig){I32, 2, I32};
    if (op <= 0x7B) return (Sig){I64, 1, I64};
    if (op <= 0x8A) return (Sig){I64, 2, I64};
    if (op <= 0x91) return (Sig){F32, 1, F32};
    if (op <= 0x98) return (Sig){F32, 2, F32};
    if (op <= 0x9F) return (Sig){F64, 1, F64};
    if (op <= 0xA6) return (Sig){F64, 2, F64};
    static const uint8_t conv[][2] = {          /* 0xA7 to 0xBF: from, to */
        {I64, I32}, {F32, I32}, {F32, I32}, {F64, I32}, {F64, I32},
        {I32, I64}, {I32, I64}, {F32, I64}, {F32, I64}, {F64, I64}, {F64, I64},
        {I32, F32}, {I32, F32}, {I64, F32}, {I64, F32}, {F64, F32},
        {I32, F64}, {I32, F64}, {I64, F64}, {I64, F64}, {F32, F64},
        {F32, I32}, {F64, I64}, {I32, F32}, {I64, F64},
    };
    return (Sig){conv[op - 0xA7][0], 1, conv[op - 0xA7][1]};
}

/* Loads and stores, 0x28 to 0x3E: the value's type, and the width of
 * memory read or written, in bytes. */
static void memory_op(uint8_t op, uint8_t *type, uint32_t *width)
{
    static const uint8_t types[] = {I32, I64, F32, F64, I32, I32, I32, I32,
        I64, I64, I64, I64, I64, I64, I32, I64, F32, F64, I32, I32, I64, I64, I64};
    static const uint8_t widths[] = {4, 8, 4, 8, 1, 1, 2, 2, 1, 1, 2, 2, 4, 4,
        4, 8, 4, 8, 1, 2, 1, 2, 4};
    *type = types[op - 0x28];
    *width = widths[op - 0x28];
}

static uint8_t blocktype(Reader *r)
{
    uint8_t bt = byte(r);
    return bt == 0x40 ? 0 : bt;
}

static void validate_code(Context *c, Code *code, FuncType *type)
{
    c->nlocals = type->nparams + code->nlocals;
    c->locals = grow(c->locals, c->nlocals, 1);
    memcpy(c->locals, type->params, type->nparams);
    memcpy(c->locals + type->nparams, code->locals, code->nlocals);
    c->result = type->nresults ? type->result : 0;
    c->nopds = c->nctrls = c->maxopds = 0;
    code->ends = grow(NULL, code->len, sizeof(int32_t));
    code->elses = grow(NULL, code->len, sizeof(int32_t));
    for (size_t i = 0; i < code->len; i++)
        code->ends[i] = code->elses[i] = -1;
    code->max_labels = 1;
    /* the function's own block, at no offset: its end is the body's */
    push_ctrl(c, 0x02, UINT32_MAX, c->result, c->result);

    Reader r = {code->body, code->body + code->len};
    while (c->nctrls > 0) {
        uint32_t at = (uint32_t)(r.p - code->body);
        uint8_t op = byte(&r);
        if (op >= 0x45 && op <= 0xBF) {
            Sig s = numeric(op);
            for (int i = 0; i < s.n; i++)
                pop_opd(c, s.in);
            push_opd(c, s.out);
            continue;
        }
        if (op >= 0x28 && op <= 0x3E) {
            uint8_t t;
            uint32_t width;
            memory_op(op, &t, &width);
            if (c->nmems == 0)
                fail("unknown memory 0");
            uint32_t align = u32(&r);
            u32(&r);
            if (align >= 32 || (1u << align) > width)
                fail("alignment must not be larger than natural");
            if (op <= 0x35) {
                pop_opd(c, I32);
                push_opd(c, t);
            } else {
                pop_opd(c, t);
                pop_opd(c, I32);
            }
            continue;
        }
        switch (op) {
        case 0x00: unreachable(c); break;
        case 0x01: break;
        case 0x02: case 0x03: case 0x04: {
            uint8_t t = blocktype(&r);
            if (op == 0x04)
                pop_opd(c, I32);
            push_ctrl(c, op, at, op == 0x03 ? 0 : t, t);
            if (c->nctrls > code->max_labels)
                code->max_labels = c->nctrls;
            break;
        }
        case 0x05: {
            Ctrl f = pop_ctrl(c);
            if (f.opcode != 0x04)
                fail("else without if");
            code->elses[f.start] = (int32_t)at;
            push_ctrl(c, 0x05, f.start, f.label, f.end);
            break;
        }
        case 0x0B: {
            Ctrl f = pop_ctrl(c);
            /* an if with a result and no else would leave nothing */
            if (f.opcode == 0x04 && f.end)
                fail("type mismatch");
            if (f.start != UINT32_MAX)
                code->ends[f.start] = (int32_t)at;
            if (f.end)
                push_opd(c, f.end);
            break;
        }
        case 0x0C: {
            uint8_t t = label_type(c, u32(&r));
            if (t)
                pop_opd(c, t);
            unreachable(c);
            break;
        }
        case 0x0D: {
            uint8_t t = label_type(c, u32(&r));
            pop_opd(c, I32);
            if (t) {
                pop_opd(c, t);
                push_opd(c, t);
            }
            break;
        }
        case 0x0E: {
            uint32_t n = length(&r);
            uint32_t *labels = grow(NULL, n + 1, sizeof(uint32_t));
            for (uint32_t i = 0; i <= n; i++)
                labels[i] = u32(&r);
            uint8_t t = label_type(c, labels[n]);
            for (uint32_t i = 0; i < n; i++)
                if (label_type(c, labels[i]) != t)
                    fail("type mismatch");
            free(labels);
            pop_opd(c, I32);
            if (t)
                pop_opd(c, t);
            unreachable(c);
            break;
        }
        case 0x0F:
            if (c->result)
                pop_opd(c, c->result);
            unreachable(c);
            break;
        case 0x10: case 0x11: {
            FuncType *t;
            if (op == 0x10) {
                uint32_t f = u32(&r);
                if (f >= c->m->nfuncimports + c->m->nfuncs)
                    fail("unknown function");
                t = c->funcs[f];
            } else {
                uint32_t x = u32(&r);
                byte(&r);
                if (c->ntables == 0)
                    fail("unknown table");
                if (x >= c->m->ntypes)
                    fail("unknown type");
                t = &c->m->types[x];
                pop_opd(c, I32);
            }
            for (uint32_t i = t->nparams; i-- > 0;)
                pop_opd(c, t->params[i]);
            if (t->nresults)
                push_opd(c, t->result);
            break;
        }
        case 0x1A: pop_any(c); break;
        case 0x1B: {
            pop_opd(c, I32);
            uint8_t t1 = pop_any(c);
            uint8_t t2 = pop_opd(c, t1);
            push_opd(c, t2);
            break;
        }
        case 0x20: case 0x21: case 0x22: {
            uint32_t x = u32(&r);
            if (x >= c->nlocals)
                fail("unknown local");
            uint8_t t = c->locals[x];
            if (op == 0x20)
                push_opd(c, t);
            else {
                pop_opd(c, t);
                if (op == 0x22)
                    push_opd(c, t);
            }
            break;
        }
        case 0x23: case 0x24: {
            uint32_t x = u32(&r);
            if (x >= c->nglobals)
                fail("unknown global");
            if (op == 0x23)
                push_opd(c, c->gtypes[x]);
            else {
                if (!c->gmuts[x])
                    fail("global is immutable");
                pop_opd(c, c->gtypes[x]);
            }
            break;
        }
        case 0x3F: case 0x40:
            byte(&r);
            if (c->nmems == 0)
                fail("unknown memory 0");
            if (op == 0x40)
                pop_opd(c, I32);
            push_opd(c, I32);
            break;
        case 0x41: signed_leb(&r, 32); push_opd(c, I32); break;
        case 0x42: signed_leb(&r, 64); push_opd(c, I64); break;
        case 0x43: r.p += 4; push_opd(c, F32); break;
        case 0x44: r.p += 8; push_opd(c, F64); break;
        default:
            fail("illegal opcode");
        }
    }
    code->max_stack = c->maxopds;
}

/* A constant expression (3.3.7.2): one t.const, or a global.get of an
 * immutable global the context has, then end. */
static void validate_const(Context *c, const uint8_t *p, size_t len, uint8_t type,
                           uint32_t globals)
{
    Reader r = {p, p + len};
    uint8_t got;
    uint8_t op = byte(&r);
    switch (op) {
    case 0x41: signed_leb(&r, 32); got = I32; break;
    case 0x42: signed_leb(&r, 64); got = I64; break;
    case 0x43: r.p += 4; got = F32; break;
    case 0x44: r.p += 8; got = F64; break;
    case 0x23: {
        uint32_t x = u32(&r);
        if (x >= globals)
            fail("unknown global");
        if (c->gmuts[x])
            fail("constant expression required");
        got = c->gtypes[x];
        break;
    }
    case 0x0B:
        fail("type mismatch");
    default:
        fail("constant expression required");
    }
    if (byte(&r) != 0x0B)
        fail("constant expression required");
    if (got != type)
        fail("type mismatch");
}

static void validate_limits(Limits l, uint64_t most, const char *message)
{
    if (l.min > most || (l.has_max && l.max > most))
        fail(message);
    if (l.has_max && l.min > l.max)
        fail("size minimum must not be greater than maximum");
}

const char *wasm_validate(Module *m)
{
    Context c;
    memset(&c, 0, sizeof c);
    c.m = m;
    if (setjmp(failed)) {
        free(c.funcs); free(c.gtypes); free(c.gmuts);
        free(c.opds); free(c.ctrls); free(c.locals);
        return failure;
    }
    for (uint32_t i = 0; i < m->ntypes; i++)
        if (m->types[i].nresults > 1)
            fail("invalid result arity");
    uint32_t nf = m->nfuncimports + m->nfuncs;
    c.funcs = grow(NULL, nf, sizeof(FuncType *));
    c.nglobals = m->nglobalimports + m->nglobals;
    c.gtypes = grow(NULL, c.nglobals, 1);
    c.gmuts = grow(NULL, c.nglobals, 1);
    uint32_t fi = 0, gi = 0;
    for (uint32_t i = 0; i < m->nimports; i++) {
        Import *im = &m->imports[i];
        switch (im->kind) {
        case EXT_FUNC:
            if (im->type >= m->ntypes)
                fail("unknown type");
            c.funcs[fi++] = &m->types[im->type];
            break;
        case EXT_TABLE:
            validate_limits(im->limits, 0xFFFFFFFFu, "table size");
            c.ntables++;
            break;
        case EXT_MEM:
            validate_limits(im->limits, 65536, "memory size must be at most 65536 pages (4GiB)");
            c.nmems++;
            break;
        case EXT_GLOBAL:
            c.gtypes[gi] = im->valtype;
            c.gmuts[gi++] = im->mut;
            break;
        }
    }
    for (uint32_t i = 0; i < m->nfuncs; i++) {
        if (m->funcs[i] >= m->ntypes)
            fail("unknown type");
        c.funcs[fi++] = &m->types[m->funcs[i]];
    }
    for (uint32_t i = 0; i < m->ntables; i++)
        validate_limits(m->tables[i], 0xFFFFFFFFu, "table size");
    for (uint32_t i = 0; i < m->nmems; i++)
        validate_limits(m->mems[i], 65536, "memory size must be at most 65536 pages (4GiB)");
    c.ntables += m->ntables;
    c.nmems += m->nmems;
    if (c.ntables > 1)
        fail("multiple tables");
    if (c.nmems > 1)
        fail("multiple memories");
    /* A global's initialiser sees only the imported globals. */
    for (uint32_t i = 0; i < m->nglobals; i++) {
        validate_const(&c, m->globals[i].init, m->globals[i].init_len,
                       m->globals[i].valtype, m->nglobalimports);
        c.gtypes[gi] = m->globals[i].valtype;
        c.gmuts[gi++] = m->globals[i].mut;
    }
    for (uint32_t i = 0; i < m->nelems; i++) {
        if (m->elems[i].table >= c.ntables)
            fail("unknown table");
        validate_const(&c, m->elems[i].offset, m->elems[i].offset_len, I32, c.nglobals);
        for (uint32_t j = 0; j < m->elems[i].count; j++)
            if (m->elems[i].funcs[j] >= nf)
                fail("unknown function");
    }
    for (uint32_t i = 0; i < m->ndatas; i++) {
        if (m->datas[i].mem >= c.nmems)
            fail("unknown memory");
        validate_const(&c, m->datas[i].offset, m->datas[i].offset_len, I32, c.nglobals);
    }
    if (m->start >= 0) {
        if ((uint64_t)m->start >= nf)
            fail("unknown function");
        FuncType *t = c.funcs[m->start];
        if (t->nparams || t->nresults)
            fail("start function");
    }
    for (uint32_t i = 0; i < m->nexports; i++) {
        Export *e = &m->exports[i];
        uint32_t most = e->kind == EXT_FUNC ? nf : e->kind == EXT_TABLE ? c.ntables
                      : e->kind == EXT_MEM ? c.nmems : c.nglobals;
        if (e->index >= most)
            fail("unknown export");
        for (uint32_t j = 0; j < i; j++)
            if (same_name(m->exports[j].name, e->name.s, e->name.len))
                fail("duplicate export name");
    }
    for (uint32_t i = 0; i < m->ncodes; i++)
        validate_code(&c, &m->codes[i], &m->types[m->funcs[i]]);
    free(c.funcs); free(c.gtypes); free(c.gmuts);
    free(c.opds); free(c.ctrls); free(c.locals);
    return NULL;
}

/* ---------------------------------------------------------------- */
/* 4.2 The store, and allocation (4.5.3). */

static uint32_t new_func(Store *s, FuncInst f)
{
    if (s->nfuncs == s->capfuncs) {
        s->capfuncs = s->capfuncs ? s->capfuncs * 2 : 64;
        s->funcs = grow(s->funcs, s->capfuncs, sizeof(FuncInst));
    }
    s->funcs[s->nfuncs] = f;
    return s->nfuncs++;
}

uint32_t wasm_host_func(Store *s, const FuncType *type, HostFunc f, void *context)
{
    FuncInst fi = {*type, NULL, NULL, f, context};
    return new_func(s, fi);
}

uint32_t wasm_new_table(Store *s, Limits l)
{
    if (s->ntables == s->captables) {
        s->captables = s->captables ? s->captables * 2 : 8;
        s->tables = grow(s->tables, s->captables, sizeof(TableInst *));
    }
    TableInst *t = grow(NULL, 1, sizeof(TableInst));
    t->size = l.min;
    t->limits = l;
    t->elems = grow(NULL, l.min, sizeof(int32_t));
    for (uint32_t i = 0; i < l.min; i++)
        t->elems[i] = -1;          /* empty */
    s->tables[s->ntables] = t;
    return s->ntables++;
}

uint32_t wasm_new_mem(Store *s, Limits l)
{
    if (s->nmems == s->capmems) {
        s->capmems = s->capmems ? s->capmems * 2 : 8;
        s->mems = grow(s->mems, s->capmems, sizeof(MemInst *));
    }
    MemInst *m = grow(NULL, 1, sizeof(MemInst));
    m->pages = l.min;
    m->limits = l;
    m->data = calloc((size_t)l.min * 65536 + 1, 1);
    if (!m->data) {
        fprintf(stderr, "wasm: out of memory\n");
        exit(2);
    }
    s->mems[s->nmems] = m;
    return s->nmems++;
}

uint32_t wasm_new_global(Store *s, uint8_t valtype, uint8_t mut, Value v)
{
    if (s->nglobals == s->capglobals) {
        s->capglobals = s->capglobals ? s->capglobals * 2 : 64;
        s->globals = grow(s->globals, s->capglobals, sizeof(GlobalInst));
    }
    s->globals[s->nglobals] = (GlobalInst){valtype, mut, v};
    return s->nglobals++;
}

const Export *wasm_export(const ModuleInst *mi, const char *n, uint32_t len)
{
    for (uint32_t i = 0; i < mi->nexports; i++)
        if (same_name(mi->exports[i].name, n, len))
            return &mi->exports[i];
    return NULL;
}

Extern wasm_extern(const ModuleInst *mi, const Export *e)
{
    Extern x = {e->kind, 0};
    switch (e->kind) {
    case EXT_FUNC: x.addr = mi->funcs[e->index]; break;
    case EXT_TABLE: x.addr = mi->table; break;
    case EXT_MEM: x.addr = mi->mem; break;
    case EXT_GLOBAL: x.addr = mi->globals[e->index]; break;
    }
    return x;
}

/* ---------------------------------------------------------------- */
/* 4.4 Execution. */

static Store *store;
static jmp_buf trapped;
static const char *trap_message;

__attribute__((noreturn)) static void trap(const char *message)
{
    trap_message = message;
    longjmp(trapped, 1);
}

/* The stacks: values (the operands, and each frame's locals below its
 * operands), labels, and frames. Their sizes bound how deep calls go. */
enum { VALUES = 1 << 20, LABELS = 1 << 18, FRAMES = 1 << 14 };

typedef struct {
    uint32_t cont;      /* where a branch to it goes on */
    uint32_t height;    /* the operand stack's height at its start */
    uint32_t arity;     /* the values a branch to it carries: 0 or 1 */
} Label;

typedef struct {
    FuncInst *func;
    uint32_t pc;        /* the caller's, to go back to */
    uint32_t locals;    /* where this frame's locals begin */
    uint32_t labels;    /* where its labels begin */
} Frame;

static Value *values;
static Label *labels;
static Frame *frames;

static uint32_t f32_bits(float f) { uint32_t u; memcpy(&u, &f, 4); return u; }
static float bits_f32(uint32_t u) { float f; memcpy(&f, &u, 4); return f; }
static uint64_t f64_bits(double d) { uint64_t u; memcpy(&u, &d, 8); return u; }
static double bits_f64(uint64_t u) { double d; memcpy(&d, &u, 8); return d; }

/* Reading immediates again as the code runs: the bytes were checked by
 * decoding, so these need no checks. */
static uint32_t imm_u32(const uint8_t *b, uint32_t *pc)
{
    uint32_t x = 0;
    unsigned shift = 0;
    uint8_t c;
    do {
        c = b[(*pc)++];
        x |= (uint32_t)(c & 0x7F) << shift;
        shift += 7;
    } while (c & 0x80);
    return x;
}

static int64_t imm_s64(const uint8_t *b, uint32_t *pc)
{
    uint64_t x = 0;
    unsigned shift = 0;
    uint8_t c;
    do {
        c = b[(*pc)++];
        x |= (uint64_t)(c & 0x7F) << shift;
        shift += 7;
    } while (c & 0x80);
    if (shift < 64 && (c & 0x40))
        x |= ~(uint64_t)0 << shift;
    return (int64_t)x;
}

/* Floating point (4.3.3). The arithmetic is C's, which on this machine
 * is IEEE 754's; what C does not say is done here: min and max, which
 * order -0 below +0 and give a NaN if either is one, and the sign
 * operations, which touch only the sign bit, even of a NaN. */
static float fmin32(float a, float b)
{
    if (isnan(a) || isnan(b)) return a + b;
    if (a == b) return signbit(a) ? a : b;
    return a < b ? a : b;
}
static float fmax32(float a, float b)
{
    if (isnan(a) || isnan(b)) return a + b;
    if (a == b) return signbit(a) ? b : a;
    return a > b ? a : b;
}
static double fmin64(double a, double b)
{
    if (isnan(a) || isnan(b)) return a + b;
    if (a == b) return signbit(a) ? a : b;
    return a < b ? a : b;
}
static double fmax64(double a, double b)
{
    if (isnan(a) || isnan(b)) return a + b;
    if (a == b) return signbit(a) ? b : a;
    return a > b ? a : b;
}

static MemInst *memory(ModuleInst *mi) { return store->mems[mi->mem]; }

/* The address of width bytes at a + offset, or a trap. */
static uint8_t *at(ModuleInst *mi, uint32_t a, uint32_t offset, uint32_t width)
{
    MemInst *m = memory(mi);
    uint64_t ea = (uint64_t)a + offset;
    if (ea + width > (uint64_t)m->pages * 65536)
        trap("out of bounds memory access");
    return m->data + ea;
}

static void evaluate_const(ModuleInst *mi, const uint8_t *p, Value *v)
{
    uint32_t pc = 1;
    switch (p[0]) {
    case 0x41: *v = (uint32_t)imm_s64(p, &pc); break;
    case 0x42: *v = (uint64_t)imm_s64(p, &pc); break;
    case 0x43: { uint32_t u; memcpy(&u, p + 1, 4); *v = u; break; }
    case 0x44: memcpy(v, p + 1, 8); break;
    case 0x23: *v = store->globals[mi->globals[imm_u32(p, &pc)]].value; break;
    }
}

static int same_type(const FuncType *a, const FuncType *b)
{
    return a->nparams == b->nparams && a->nresults == b->nresults &&
           (a->nresults == 0 || a->result == b->result) &&
           memcmp(a->params, b->params, a->nparams) == 0;
}


/* The numeric instructions, 0x45 to 0xBF (4.4.1, 4.3). Each works on
 * the top of the value stack, and gives back the stack's new height. An
 * i32 or an f32 is kept in the low 32 bits, the rest 0. */

#define A32 ((uint32_t)values[sp - 2])
#define B32 ((uint32_t)values[sp - 1])
#define A64 (values[sp - 2])
#define B64 (values[sp - 1])
#define FA ((double)bits_f32(A32))
#define FB ((double)bits_f32(B32))
#define BIN32(e) (values[sp - 2] = (uint32_t)(e), sp - 1)
#define BIN64(e) (values[sp - 2] = (uint64_t)(e), sp - 1)
#define UN32(e) (values[sp - 1] = (uint32_t)(e), sp)
#define UN64(e) (values[sp - 1] = (uint64_t)(e), sp)
#define F32R(e) (f32_bits((float)(e)))
#define F64R(e) (f64_bits((double)(e)))

static uint32_t rotl32(uint32_t x, uint32_t n) { n &= 31; return n ? x << n | x >> (32 - n) : x; }
static uint32_t rotr32(uint32_t x, uint32_t n) { n &= 31; return n ? x >> n | x << (32 - n) : x; }
static uint64_t rotl64(uint64_t x, uint64_t n) { n &= 63; return n ? x << n | x >> (64 - n) : x; }
static uint64_t rotr64(uint64_t x, uint64_t n) { n &= 63; return n ? x >> n | x << (64 - n) : x; }

static uint32_t div32(uint32_t a, uint32_t b, int sign, int rem)
{
    if (b == 0)
        trap("integer divide by zero");
    if (!sign)
        return rem ? a % b : a / b;
    if ((int32_t)a == INT32_MIN && (int32_t)b == -1) {
        if (rem)
            return 0;
        trap("integer overflow");
    }
    return (uint32_t)(rem ? (int32_t)a % (int32_t)b : (int32_t)a / (int32_t)b);
}

static uint64_t div64(uint64_t a, uint64_t b, int sign, int rem)
{
    if (b == 0)
        trap("integer divide by zero");
    if (!sign)
        return rem ? a % b : a / b;
    if ((int64_t)a == INT64_MIN && (int64_t)b == -1) {
        if (rem)
            return 0;
        trap("integer overflow");
    }
    return (uint64_t)(rem ? (int64_t)a % (int64_t)b : (int64_t)a / (int64_t)b);
}

/* Truncation to an integer traps on a NaN, or on a value whose integer
 * part is out of range: above low and below high, or equal to low when
 * low itself is in range. */
static double in_range(double x, double low, double high, int low_too)
{
    if (isnan(x))
        trap("invalid conversion to integer");
    if (!((low_too ? x >= low : x > low) && x < high))
        trap("integer overflow");
    return trunc(x);
}

static uint32_t numeric_op(uint8_t op, uint32_t sp)
{
    float fa, fb;
    double da, db;
    switch (op) {
    /* i32 and i64 tests and comparisons */
    case 0x45: return UN32(B32 == 0);
    case 0x46: return BIN32(A32 == B32);
    case 0x47: return BIN32(A32 != B32);
    case 0x48: return BIN32((int32_t)A32 < (int32_t)B32);
    case 0x49: return BIN32(A32 < B32);
    case 0x4A: return BIN32((int32_t)A32 > (int32_t)B32);
    case 0x4B: return BIN32(A32 > B32);
    case 0x4C: return BIN32((int32_t)A32 <= (int32_t)B32);
    case 0x4D: return BIN32(A32 <= B32);
    case 0x4E: return BIN32((int32_t)A32 >= (int32_t)B32);
    case 0x4F: return BIN32(A32 >= B32);
    case 0x50: return UN32(B64 == 0);
    case 0x51: return BIN32(A64 == B64);
    case 0x52: return BIN32(A64 != B64);
    case 0x53: return BIN32((int64_t)A64 < (int64_t)B64);
    case 0x54: return BIN32(A64 < B64);
    case 0x55: return BIN32((int64_t)A64 > (int64_t)B64);
    case 0x56: return BIN32(A64 > B64);
    case 0x57: return BIN32((int64_t)A64 <= (int64_t)B64);
    case 0x58: return BIN32(A64 <= B64);
    case 0x59: return BIN32((int64_t)A64 >= (int64_t)B64);
    case 0x5A: return BIN32(A64 >= B64);
    /* f32 and f64 comparisons: false with a NaN, but for ne */
    case 0x5B: return BIN32(bits_f32(A32) == bits_f32(B32));
    case 0x5C: return BIN32(bits_f32(A32) != bits_f32(B32));
    case 0x5D: return BIN32(bits_f32(A32) < bits_f32(B32));
    case 0x5E: return BIN32(bits_f32(A32) > bits_f32(B32));
    case 0x5F: return BIN32(bits_f32(A32) <= bits_f32(B32));
    case 0x60: return BIN32(bits_f32(A32) >= bits_f32(B32));
    case 0x61: return BIN32(bits_f64(A64) == bits_f64(B64));
    case 0x62: return BIN32(bits_f64(A64) != bits_f64(B64));
    case 0x63: return BIN32(bits_f64(A64) < bits_f64(B64));
    case 0x64: return BIN32(bits_f64(A64) > bits_f64(B64));
    case 0x65: return BIN32(bits_f64(A64) <= bits_f64(B64));
    case 0x66: return BIN32(bits_f64(A64) >= bits_f64(B64));
    /* i32 arithmetic */
    case 0x67: return UN32(B32 ? __builtin_clz(B32) : 32);
    case 0x68: return UN32(B32 ? __builtin_ctz(B32) : 32);
    case 0x69: return UN32(__builtin_popcount(B32));
    case 0x6A: return BIN32(A32 + B32);
    case 0x6B: return BIN32(A32 - B32);
    case 0x6C: return BIN32(A32 * B32);
    case 0x6D: return BIN32(div32(A32, B32, 1, 0));
    case 0x6E: return BIN32(div32(A32, B32, 0, 0));
    case 0x6F: return BIN32(div32(A32, B32, 1, 1));
    case 0x70: return BIN32(div32(A32, B32, 0, 1));
    case 0x71: return BIN32(A32 & B32);
    case 0x72: return BIN32(A32 | B32);
    case 0x73: return BIN32(A32 ^ B32);
    case 0x74: return BIN32(A32 << (B32 & 31));
    case 0x75: return BIN32((uint32_t)((int32_t)A32 >> (B32 & 31)));
    case 0x76: return BIN32(A32 >> (B32 & 31));
    case 0x77: return BIN32(rotl32(A32, B32));
    case 0x78: return BIN32(rotr32(A32, B32));
    /* i64 arithmetic */
    case 0x79: return UN64(B64 ? __builtin_clzll(B64) : 64);
    case 0x7A: return UN64(B64 ? __builtin_ctzll(B64) : 64);
    case 0x7B: return UN64(__builtin_popcountll(B64));
    case 0x7C: return BIN64(A64 + B64);
    case 0x7D: return BIN64(A64 - B64);
    case 0x7E: return BIN64(A64 * B64);
    case 0x7F: return BIN64(div64(A64, B64, 1, 0));
    case 0x80: return BIN64(div64(A64, B64, 0, 0));
    case 0x81: return BIN64(div64(A64, B64, 1, 1));
    case 0x82: return BIN64(div64(A64, B64, 0, 1));
    case 0x83: return BIN64(A64 & B64);
    case 0x84: return BIN64(A64 | B64);
    case 0x85: return BIN64(A64 ^ B64);
    case 0x86: return BIN64(A64 << (B64 & 63));
    case 0x87: return BIN64((uint64_t)((int64_t)A64 >> (B64 & 63)));
    case 0x88: return BIN64(A64 >> (B64 & 63));
    case 0x89: return BIN64(rotl64(A64, B64));
    case 0x8A: return BIN64(rotr64(A64, B64));
    /* f32 arithmetic */
    case 0x8B: return UN32(B32 & 0x7FFFFFFFu);
    case 0x8C: return UN32(B32 ^ 0x80000000u);
    case 0x8D: return UN32(F32R(ceilf(bits_f32(B32))));
    case 0x8E: return UN32(F32R(floorf(bits_f32(B32))));
    case 0x8F: return UN32(F32R(truncf(bits_f32(B32))));
    case 0x90: return UN32(F32R(rintf(bits_f32(B32))));    /* to even */
    case 0x91: return UN32(F32R(sqrtf(bits_f32(B32))));
    case 0x92: fa = bits_f32(A32); fb = bits_f32(B32); return BIN32(F32R(fa + fb));
    case 0x93: fa = bits_f32(A32); fb = bits_f32(B32); return BIN32(F32R(fa - fb));
    case 0x94: fa = bits_f32(A32); fb = bits_f32(B32); return BIN32(F32R(fa * fb));
    case 0x95: fa = bits_f32(A32); fb = bits_f32(B32); return BIN32(F32R(fa / fb));
    case 0x96: return BIN32(F32R(fmin32(bits_f32(A32), bits_f32(B32))));
    case 0x97: return BIN32(F32R(fmax32(bits_f32(A32), bits_f32(B32))));
    case 0x98: return BIN32((A32 & 0x7FFFFFFFu) | (B32 & 0x80000000u));
    /* f64 arithmetic */
    case 0x99: return UN64(B64 & 0x7FFFFFFFFFFFFFFFu);
    case 0x9A: return UN64(B64 ^ 0x8000000000000000u);
    case 0x9B: return UN64(F64R(ceil(bits_f64(B64))));
    case 0x9C: return UN64(F64R(floor(bits_f64(B64))));
    case 0x9D: return UN64(F64R(trunc(bits_f64(B64))));
    case 0x9E: return UN64(F64R(rint(bits_f64(B64))));
    case 0x9F: return UN64(F64R(sqrt(bits_f64(B64))));
    case 0xA0: da = bits_f64(A64); db = bits_f64(B64); return BIN64(F64R(da + db));
    case 0xA1: da = bits_f64(A64); db = bits_f64(B64); return BIN64(F64R(da - db));
    case 0xA2: da = bits_f64(A64); db = bits_f64(B64); return BIN64(F64R(da * db));
    case 0xA3: da = bits_f64(A64); db = bits_f64(B64); return BIN64(F64R(da / db));
    case 0xA4: return BIN64(F64R(fmin64(bits_f64(A64), bits_f64(B64))));
    case 0xA5: return BIN64(F64R(fmax64(bits_f64(A64), bits_f64(B64))));
    case 0xA6: return BIN64((A64 & 0x7FFFFFFFFFFFFFFFu) | (B64 & 0x8000000000000000u));
    /* conversions */
    case 0xA7: return UN32((uint32_t)B64);
    case 0xA8: return UN32((int32_t)in_range(bits_f32(B32), -2147483649.0, 2147483648.0, 0));
    case 0xA9: return UN32((uint32_t)in_range(bits_f32(B32), -1.0, 4294967296.0, 0));
    case 0xAA: return UN32((int32_t)in_range(bits_f64(B64), -2147483649.0, 2147483648.0, 0));
    case 0xAB: return UN32((uint32_t)in_range(bits_f64(B64), -1.0, 4294967296.0, 0));
    case 0xAC: return UN64((uint64_t)(int64_t)(int32_t)B32);
    case 0xAD: return UN64((uint64_t)B32);
    case 0xAE: return UN64((int64_t)in_range(bits_f32(B32), -9223372036854775808.0, 9223372036854775808.0, 1));
    case 0xAF: return UN64((uint64_t)in_range(bits_f32(B32), -1.0, 18446744073709551616.0, 0));
    case 0xB0: return UN64((int64_t)in_range(bits_f64(B64), -9223372036854775808.0, 9223372036854775808.0, 1));
    case 0xB1: return UN64((uint64_t)in_range(bits_f64(B64), -1.0, 18446744073709551616.0, 0));
    case 0xB2: return UN32(f32_bits((float)(int32_t)B32));
    case 0xB3: return UN32(f32_bits((float)B32));
    case 0xB4: return UN32(f32_bits((float)(int64_t)B64));
    case 0xB5: return UN32(f32_bits((float)B64));
    case 0xB6: return UN32(f32_bits((float)bits_f64(B64)));
    case 0xB7: return UN64(f64_bits((double)(int32_t)B32));
    case 0xB8: return UN64(f64_bits((double)B32));
    case 0xB9: return UN64(f64_bits((double)(int64_t)B64));
    case 0xBA: return UN64(f64_bits((double)B64));
    case 0xBB: return UN64(f64_bits((double)bits_f32(B32)));
    default:   /* 0xBC to 0xBF: the reinterpretations change no bits */
        return sp;
    }
}

/* Run the function at funcaddr, whose arguments are on top of the value
 * stack, until it returns, and give the stack's height then. Calls do
 * not nest in C: a call pushes a frame here, and a return pops it. */
static uint32_t run(uint32_t funcaddr, uint32_t sp)
{
    uint32_t nframes = 0, ltop = 0, depth;
    FuncInst *f = NULL;
    Code *code = NULL;
    ModuleInst *mi = NULL;
    const uint8_t *body = NULL;
    uint32_t pc = 0, locals = 0, lbase = 0;
    uint32_t callee = funcaddr;

call: {
        FuncInst *g = &store->funcs[callee];
        wasm_calls++;
        if (g->host) {
            uint32_t n = g->type.nparams;
            Value result = 0;
            const char *t = g->host(g->context, values + sp - n, &result);
            if (t)
                trap(t);
            sp -= n;
            if (g->type.nresults)
                values[sp++] = result;
            if (nframes == 0)
                return sp;
            goto next;
        }
        Code *c = g->code;
        if (nframes == FRAMES ||
            (uint64_t)sp + c->nlocals + c->max_stack + 1 > VALUES ||
            (uint64_t)ltop + c->max_labels + 1 > LABELS)
            trap("call stack exhausted");
        if (nframes > 0)
            frames[nframes - 1].pc = pc;    /* where the caller goes on */
        f = g;
        code = c;
        mi = g->module;
        body = c->body;
        locals = sp - g->type.nparams;
        frames[nframes++] = (Frame){g, 0, locals, ltop};
        memset(values + sp, 0, sizeof(Value) * c->nlocals);
        sp += c->nlocals;
        lbase = ltop;
        labels[ltop++] = (Label){(uint32_t)c->len, sp, g->type.nresults};
        pc = 0;
    }

next:
    for (;;) {
        uint8_t op = body[pc++];
        wasm_steps++;
        switch (op) {
        case 0x00: trap("unreachable");
        case 0x01: break;
        case 0x02: case 0x03: {     /* block; loop, whose label goes back */
            uint32_t start = pc - 1;
            uint8_t bt = body[pc++];
            if (op == 0x02)
                labels[ltop++] = (Label){(uint32_t)code->ends[start] + 1, sp, bt != 0x40};
            else
                labels[ltop++] = (Label){start, sp, 0};
            break;
        }
        case 0x04: {                /* if */
            uint32_t start = pc - 1;
            uint8_t bt = body[pc++];
            uint32_t c = (uint32_t)values[--sp];
            Label l = {(uint32_t)code->ends[start] + 1, sp, bt != 0x40};
            if (c)
                labels[ltop++] = l;
            else if (code->elses[start] >= 0) {
                labels[ltop++] = l;
                pc = (uint32_t)code->elses[start] + 1;
            } else
                pc = l.cont;
            break;
        }
        case 0x05:                  /* else, reached at the end of the then */
            pc = labels[--ltop].cont;
            break;
        case 0x0B:                  /* end */
            if (--ltop == lbase)
                goto ret;
            break;
        case 0x0C:
            depth = imm_u32(body, &pc);
            goto branch;
        case 0x0D:
            depth = imm_u32(body, &pc);
            if ((uint32_t)values[--sp])
                goto branch;
            break;
        case 0x0E: {
            uint32_t n = imm_u32(body, &pc);
            uint32_t i = (uint32_t)values[--sp];
            uint32_t k = i < n ? i : n;
            for (uint32_t j = 0; j < k; j++)
                imm_u32(body, &pc);
            depth = imm_u32(body, &pc);
            goto branch;
        }
        case 0x0F:                  /* return: a branch to the function's label */
            depth = ltop - 1 - lbase;
            goto branch;
        case 0x10:
            callee = mi->funcs[imm_u32(body, &pc)];
            goto call;
        case 0x11: {
            uint32_t x = imm_u32(body, &pc);
            pc++;                   /* the reserved byte */
            uint32_t i = (uint32_t)values[--sp];
            TableInst *t = store->tables[mi->table];
            if (i >= t->size)
                trap("undefined element");
            if (t->elems[i] < 0)
                trap("uninitialized element");
            callee = (uint32_t)t->elems[i];
            if (!same_type(&store->funcs[callee].type, &mi->types[x]))
                trap("indirect call type mismatch");
            goto call;
        }
        case 0x1A: sp--; break;
        case 0x1B: {                /* select */
            uint32_t c = (uint32_t)values[--sp];
            sp--;
            if (!c)
                values[sp - 1] = values[sp];
            break;
        }
        case 0x20: values[sp++] = values[locals + imm_u32(body, &pc)]; break;
        case 0x21: values[locals + imm_u32(body, &pc)] = values[--sp]; break;
        case 0x22: values[locals + imm_u32(body, &pc)] = values[sp - 1]; break;
        case 0x23: values[sp++] = store->globals[mi->globals[imm_u32(body, &pc)]].value; break;
        case 0x24: store->globals[mi->globals[imm_u32(body, &pc)]].value = values[--sp]; break;
        case 0x3F:                  /* memory.size */
            pc++;
            values[sp++] = memory(mi)->pages;
            break;
        case 0x40: {                /* memory.grow: the old size, or -1 */
            pc++;
            MemInst *m = memory(mi);
            uint32_t n = (uint32_t)values[sp - 1];
            uint64_t len = (uint64_t)m->pages + n;
            uint64_t most = m->limits.has_max ? m->limits.max : 65536;
            if (len > most)
                values[sp - 1] = 0xFFFFFFFFu;
            else {
                m->data = grow(m->data, (size_t)len * 65536 + 1, 1);
                memset(m->data + (size_t)m->pages * 65536, 0, (size_t)n * 65536);
                values[sp - 1] = m->pages;
                m->pages = (uint32_t)len;
            }
            break;
        }
        case 0x41: values[sp++] = (uint32_t)imm_s64(body, &pc); break;
        case 0x42: values[sp++] = (uint64_t)imm_s64(body, &pc); break;
        case 0x43: {
            uint32_t u;
            memcpy(&u, body + pc, 4);
            pc += 4;
            values[sp++] = u;
            break;
        }
        case 0x44: memcpy(&values[sp++], body + pc, 8); pc += 8; break;
        default:
            if (op >= 0x28 && op <= 0x3E) {
                imm_u32(body, &pc);             /* the alignment: only a hint */
                uint32_t offset = imm_u32(body, &pc);
                uint8_t t;
                uint32_t width;
                memory_op(op, &t, &width);
                if (op <= 0x35) {               /* a load */
                    uint8_t *p = at(mi, (uint32_t)values[sp - 1], offset, width);
                    uint64_t x = 0;
                    memcpy(&x, p, width);       /* little-endian, as WebAssembly is */
                    switch (op) {
                    case 0x2C: x = (uint32_t)(int32_t)(int8_t)x; break;
                    case 0x2E: x = (uint32_t)(int32_t)(int16_t)x; break;
                    case 0x30: x = (uint64_t)(int64_t)(int8_t)x; break;
                    case 0x32: x = (uint64_t)(int64_t)(int16_t)x; break;
                    case 0x34: x = (uint64_t)(int64_t)(int32_t)x; break;
                    }
                    values[sp - 1] = x;
                } else {                        /* a store */
                    Value x = values[--sp];
                    uint8_t *p = at(mi, (uint32_t)values[--sp], offset, width);
                    memcpy(p, &x, width);
                }
            } else
                sp = numeric_op(op, sp);
        }
        continue;

    branch: {
            Label l = labels[ltop - 1 - depth];
            if (l.arity)
                values[l.height] = values[sp - 1];
            sp = l.height + l.arity;
            ltop -= depth + 1;
            pc = l.cont;
            if (ltop == lbase)
                goto ret;
        }
    }

ret: {
        /* the result is on top: move it down over the locals */
        if (f->type.nresults)
            values[locals] = values[sp - 1];
        sp = locals + f->type.nresults;
        nframes--;
        if (nframes == 0)
            return sp;
        Frame *fr = &frames[nframes - 1];
        f = fr->func;
        code = f->code;
        mi = f->module;
        body = code->body;
        pc = fr->pc;
        locals = fr->locals;
        lbase = fr->labels;
        goto next;
    }
}

const char *wasm_invoke(Store *s, uint32_t funcaddr, const Value *args, Value *results)
{
    if (!values) {
        values = grow(NULL, VALUES, sizeof(Value));
        labels = grow(NULL, LABELS, sizeof(Label));
        frames = grow(NULL, FRAMES, sizeof(Frame));
    }
    store = s;
    FuncInst *f = &s->funcs[funcaddr];
    memcpy(values, args, sizeof(Value) * f->type.nparams);
    if (setjmp(trapped))
        return trap_message;
    run(funcaddr, f->type.nparams);
    if (f->type.nresults)
        results[0] = values[0];
    return NULL;
}

/* ---------------------------------------------------------------- */
/* 4.5.4 Instantiation. */

static int limits_match(uint32_t size, Limits have, Limits want)
{
    if (size < want.min)
        return 0;
    if (want.has_max && (!have.has_max || have.max > want.max))
        return 0;
    return 1;
}

const char *wasm_instantiate(Store *s, Module *m, const Extern *imports,
                             ModuleInst **out, int *trap_out)
{
    store = s;
    *trap_out = 0;
    *out = NULL;
    /* 4: each import must be given something of its type */
    for (uint32_t i = 0; i < m->nimports; i++) {
        Import *im = &m->imports[i];
        Extern x = imports[i];
        int ok = x.kind == im->kind;
        if (ok) switch (im->kind) {
        case EXT_FUNC: ok = same_type(&s->funcs[x.addr].type, &m->types[im->type]); break;
        case EXT_TABLE: ok = limits_match(s->tables[x.addr]->size, s->tables[x.addr]->limits, im->limits); break;
        case EXT_MEM: ok = limits_match(s->mems[x.addr]->pages, s->mems[x.addr]->limits, im->limits); break;
        case EXT_GLOBAL:
            ok = s->globals[x.addr].valtype == im->valtype && s->globals[x.addr].mut == im->mut;
            break;
        }
        if (!ok)
            return "incompatible import type";
    }
    /* 5, 6: the module instance, with what it imports first */
    ModuleInst *mi = grow(NULL, 1, sizeof(ModuleInst));
    memset(mi, 0, sizeof *mi);
    mi->module = m;
    mi->types = m->types;
    mi->ntypes = m->ntypes;
    mi->nfuncs = m->nfuncimports + m->nfuncs;
    mi->funcs = grow(NULL, mi->nfuncs, sizeof(uint32_t));
    mi->nglobals = m->nglobalimports + m->nglobals;
    mi->globals = grow(NULL, mi->nglobals, sizeof(uint32_t));
    mi->table = mi->mem = UINT32_MAX;
    mi->exports = m->exports;
    mi->nexports = m->nexports;
    uint32_t fi = 0, gi = 0;
    for (uint32_t i = 0; i < m->nimports; i++)
        switch (imports[i].kind) {
        case EXT_FUNC: mi->funcs[fi++] = imports[i].addr; break;
        case EXT_TABLE: mi->table = imports[i].addr; break;
        case EXT_MEM: mi->mem = imports[i].addr; break;
        case EXT_GLOBAL: mi->globals[gi++] = imports[i].addr; break;
        }
    for (uint32_t i = 0; i < m->nfuncs; i++) {
        FuncInst fn = {m->types[m->funcs[i]], mi, &m->codes[i], NULL, NULL};
        mi->funcs[fi++] = new_func(s, fn);
    }
    if (m->ntables)
        mi->table = wasm_new_table(s, m->tables[0]);
    if (m->nmems)
        mi->mem = wasm_new_mem(s, m->mems[0]);
    for (uint32_t i = 0; i < m->nglobals; i++) {
        Value v = 0;
        evaluate_const(mi, m->globals[i].init, &v);  /* sees only imports */
        mi->globals[gi++] = wasm_new_global(s, m->globals[i].valtype, m->globals[i].mut, v);
    }
    /* 9, 10: every segment must fit, before any is written */
    uint32_t *eo = grow(NULL, m->nelems, sizeof(uint32_t));
    uint32_t *dof = grow(NULL, m->ndatas, sizeof(uint32_t));
    for (uint32_t i = 0; i < m->nelems; i++) {
        Value v = 0;
        evaluate_const(mi, m->elems[i].offset, &v);
        eo[i] = (uint32_t)v;
        if ((uint64_t)eo[i] + m->elems[i].count > s->tables[mi->table]->size) {
            free(eo); free(dof);
            return "elements segment does not fit";
        }
    }
    for (uint32_t i = 0; i < m->ndatas; i++) {
        Value v = 0;
        evaluate_const(mi, m->datas[i].offset, &v);
        dof[i] = (uint32_t)v;
        if ((uint64_t)dof[i] + m->datas[i].len > (uint64_t)s->mems[mi->mem]->pages * 65536) {
            free(eo); free(dof);
            return "data segment does not fit";
        }
    }
    /* 13, 14: then write them */
    for (uint32_t i = 0; i < m->nelems; i++)
        for (uint32_t j = 0; j < m->elems[i].count; j++)
            s->tables[mi->table]->elems[eo[i] + j] = (int32_t)mi->funcs[m->elems[i].funcs[j]];
    for (uint32_t i = 0; i < m->ndatas; i++)
        if (m->datas[i].len)
            memcpy(s->mems[mi->mem]->data + dof[i], m->datas[i].bytes, m->datas[i].len);
    free(eo);
    free(dof);
    *out = mi;
    /* 15: the start function */
    if (m->start >= 0) {
        const char *t = wasm_invoke(s, mi->funcs[m->start], NULL, NULL);
        if (t) {
            *trap_out = 1;
            return t;
        }
    }
    return NULL;
}
