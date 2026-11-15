/*
 * Reading a program: the typed tree emit.py writes, as an S-expression,
 * built into the structures cek.h declares, the same ones Lark's
 * emit_c_ast.py wrote out as C data. See emit.py for the format.
 */

#include "cek.h"
#include "tree.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *text, *at;   /* the file, and where reading is */
static const char *path;

static void bad(const char *why)
{
    fprintf(stderr, "%s: not a tree: %s at byte %ld\n", path, why, (long)(at - text));
    exit(2);
}

static void *room(size_t n)
{
    void *p = calloc(1, n ? n : 1);
    if (!p) {
        fputs("lark: out of memory\n", stderr);
        exit(2);
    }
    return p;
}

static void space(void)
{
    while (*at == ' ' || *at == '\n' || *at == '\t' || *at == '\r')
        at++;
}

static void open_(void)
{
    space();
    if (*at++ != '(')
        bad("( expected");
}

static void close_(void)
{
    space();
    if (*at++ != ')')
        bad(") expected");
}

static int closing(void)
{
    space();
    return *at == ')';
}

/* A word: a node's kind, or a number. */
static const char *word(void)
{
    static char w[32];
    size_t n = 0;
    space();
    while (*at && !strchr(" \n\t\r()\"", *at)) {
        if (n + 1 < sizeof w)
            w[n++] = *at;
        at++;
    }
    w[n] = 0;
    if (!n)
        bad("a word expected");
    return w;
}

static long long number(void)
{
    const char *w = word();
    char *end;
    long long x = strtoll(w, &end, 10);
    if (*end)
        bad("a number expected");
    return x;
}

static const char *string(void)
{
    space();
    if (*at++ != '"')
        bad("a string expected");
    size_t cap = 16, n = 0;
    char *s = room(cap);
    while (*at != '"') {
        char c = *at++;
        if (!c)
            bad("a string not ended");
        if (c == '\\') {
            c = *at++;
            switch (c) {
            case 'n': c = '\n'; break;
            case 'r': c = '\r'; break;
            case 't': c = '\t'; break;
            case 'x': {
                char hex[3] = {at[0], at[1], 0};
                c = (char)strtol(hex, NULL, 16);
                at += 2;
                break;
            }
            }
        }
        if (n + 2 > cap)
            s = realloc(s, cap *= 2);
        s[n++] = c;
    }
    at++;
    s[n] = 0;
    return s;
}

static LkLit literal(const char *kind)
{
    LkLit l;
    memset(&l, 0, sizeof l);
    if (strcmp(kind, "int") == 0) { l.kind = LIT_INT; l.i = (int32_t)number(); }
    else if (strcmp(kind, "float") == 0) { l.kind = LIT_FLOAT; l.f = (uint32_t)number(); }
    else if (strcmp(kind, "bool") == 0) { l.kind = LIT_BOOL; l.b = (int)number(); }
    else if (strcmp(kind, "str") == 0) { l.kind = LIT_STR; l.s = string(); }
    else if (strcmp(kind, "unit") == 0) l.kind = LIT_UNIT;
    else bad("a literal expected");
    return l;
}

static int is_literal(const char *k)
{
    return !strcmp(k, "int") || !strcmp(k, "float") || !strcmp(k, "bool") ||
           !strcmp(k, "str") || !strcmp(k, "unit");
}

/* An operator's number. */
static Op op_code(const char *op, int unary)
{
    static const struct { const char *name; Op code; } binary[] = {
        {"+", OP_ADD}, {"-", OP_SUB}, {"*", OP_MUL}, {"/", OP_DIV}, {"%", OP_REM},
        {"==", OP_EQ}, {"!=", OP_NE}, {"<", OP_LT}, {"<=", OP_LE}, {">", OP_GT},
        {">=", OP_GE}, {"and", OP_AND}, {"or", OP_OR},
    };
    if (unary) {
        if (!strcmp(op, "-")) return OP_NEG;
        if (!strcmp(op, "not")) return OP_NOT;
    } else
        for (size_t i = 0; i < sizeof binary / sizeof binary[0]; i++)
            if (!strcmp(op, binary[i].name))
                return binary[i].code;
    bad("an operator Lark does not have");
    return OP_ADD;
}

static const LkExpr *expr(void);
static const LkPat *pattern(void);

/* The rest of a list, as an array of expressions, and how many. */
static const LkExpr *const *exprs(int *n)
{
    int cap = 4;
    const LkExpr **v = room(sizeof *v * (size_t)cap);
    *n = 0;
    while (!closing()) {
        if (*n == cap)
            v = realloc(v, sizeof *v * (size_t)(cap *= 2));
        v[(*n)++] = expr();
    }
    return v;
}

static const LkPat *const *patterns(int *n)
{
    int cap = 4;
    const LkPat **v = room(sizeof *v * (size_t)cap);
    *n = 0;
    while (!closing()) {
        if (*n == cap)
            v = realloc(v, sizeof *v * (size_t)(cap *= 2));
        v[(*n)++] = pattern();
    }
    return v;
}

static const LkExpr *expr(void)
{
    LkExpr *e = room(sizeof *e);
    open_();
    char kind[32];
    strcpy(kind, word());
    if (is_literal(kind)) {
        e->kind = EXPR_LIT;
        e->lit = literal(kind);
    } else if (!strcmp(kind, "var") || !strcmp(kind, "con")) {
        e->kind = kind[0] == 'v' ? EXPR_VAR : EXPR_CON;
        e->name = string();
        e->depth = (int)number();
        e->slot = -1;
    } else if (!strcmp(kind, "tuple")) {
        e->kind = EXPR_TUPLE;
        e->tup.elems = exprs(&e->tup.n);
    } else if (!strcmp(kind, "apply")) {
        e->kind = EXPR_APPLY;
        e->app.fn = expr();
        e->app.args = exprs(&e->app.n_args);
        if (e->app.n_args == 0)
            bad("an application with no argument");
    } else if (!strcmp(kind, "binop")) {
        e->kind = EXPR_BINOP;
        e->binop.op = string();
        e->binop.code = op_code(e->binop.op, 0);
        e->binop.left = expr();
        e->binop.right = expr();
    } else if (!strcmp(kind, "unary")) {
        e->kind = EXPR_UNARY;
        e->unary.op = string();
        e->unary.code = op_code(e->unary.op, 1);
        e->unary.operand = expr();
    } else if (!strcmp(kind, "let")) {
        e->kind = EXPR_LET;
        e->let.name = string();
        e->let.val = expr();
        e->let.body = expr();
    } else if (!strcmp(kind, "if")) {
        e->kind = EXPR_IF;
        e->if_.cond = expr();
        e->if_.then_ = expr();
        e->if_.else_ = expr();
    } else if (!strcmp(kind, "lambda")) {
        e->kind = EXPR_LAMBDA;
        e->lam.param = string();
        e->lam.body = expr();
    } else if (!strcmp(kind, "match")) {
        e->kind = EXPR_MATCH;
        e->match.scrutinee = expr();
        int cap = 4, n = 0;
        LkArm *arms = room(sizeof *arms * (size_t)cap);
        while (!closing()) {
            if (n == cap)
                arms = realloc(arms, sizeof *arms * (size_t)(cap *= 2));
            open_();
            if (strcmp(word(), "arm") != 0)
                bad("arm expected");
            arms[n].pat = pattern();
            arms[n].body = expr();
            n++;
            close_();
        }
        e->match.arms = arms;
        e->match.n_arms = n;
    } else
        bad("an expression expected");
    close_();
    return e;
}

static const LkPat *pattern(void)
{
    LkPat *p = room(sizeof *p);
    open_();
    char kind[32];
    strcpy(kind, word());
    if (!strcmp(kind, "wild"))
        p->kind = PAT_WILD;
    else if (!strcmp(kind, "pvar")) {
        p->kind = PAT_VAR;
        p->var = string();
    } else if (!strcmp(kind, "plit")) {
        p->kind = PAT_LIT;
        open_();
        char lk[32];
        strcpy(lk, word());
        p->lit = literal(lk);
        close_();
    } else if (!strcmp(kind, "pcon")) {
        p->kind = PAT_CON;
        p->con.name = string();
        p->con.args = patterns(&p->con.n_args);
    } else if (!strcmp(kind, "ptuple")) {
        p->kind = PAT_TUPLE;
        p->tup.elems = patterns(&p->tup.n);
    } else
        bad("a pattern expected");
    close_();
    return p;
}

static const LkDecl *decl(void)
{
    LkDecl *d = room(sizeof *d);
    open_();
    char kind[32];
    strcpy(kind, word());
    d->name = string();
    if (!strcmp(kind, "fn")) {
        d->kind = DECL_FN;
        d->fn.param = string();
        d->fn.body = expr();
    } else if (!strcmp(kind, "let")) {
        d->kind = DECL_LET;
        d->let_val = expr();
    } else if (!strcmp(kind, "type")) {
        d->kind = DECL_TYPE;
        int cap = 4, n = 0;
        LkVariant *v = room(sizeof *v * (size_t)cap);
        while (!closing()) {
            if (n == cap)
                v = realloc(v, sizeof *v * (size_t)(cap *= 2));
            open_();
            v[n].name = string();
            v[n].arity = (int)number();
            close_();
            n++;
        }
        d->type_.variants = v;
        d->type_.n_variants = n;
    } else if (!strcmp(kind, "impl")) {
        d->kind = DECL_IMPL;
        d->impl.trait_name = string();
        int cap = 4, n = 0;
        LkMethod *m = room(sizeof *m * (size_t)cap);
        while (!closing()) {
            if (n == cap)
                m = realloc(m, sizeof *m * (size_t)(cap *= 2));
            open_();
            m[n].name = string();
            m[n].param = string();
            m[n].body = expr();
            close_();
            n++;
        }
        d->impl.methods = m;
        d->impl.n_methods = n;
    } else
        bad("a declaration expected");
    close_();
    return d;
}

LkProg tree_read(const char *file)
{
    path = file;
    FILE *f = fopen(file, "rb");
    if (!f) {
        fprintf(stderr, "%s: cannot open\n", file);
        exit(2);
    }
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);
    char *buf = room((size_t)size + 1);
    size_t got = fread(buf, 1, (size_t)size, f);
    fclose(f);
    buf[got] = 0;
    text = at = buf;

    open_();
    if (strcmp(word(), "lark") != 0 || number() != 2)
        bad("(lark 2 expected");
    int cap = 16, n = 0;
    const LkDecl **decls = room(sizeof *decls * (size_t)cap);
    while (!closing()) {
        if (n == cap)
            decls = realloc(decls, sizeof *decls * (size_t)(cap *= 2));
        decls[n++] = decl();
    }
    close_();
    space();
    if (*at)
        bad("something after the program");
    return (LkProg){decls, n};
}
