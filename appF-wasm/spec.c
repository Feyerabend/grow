/*
 * The specification's own tests, run on this machine.
 *
 * Each .wast file of the test suite is turned by WABT's wast2json into
 * binary modules and a JSON script of commands: load this module,
 * register it under a name, invoke this function and expect that
 * result, or a trap; expect this module to be malformed, invalid,
 * unlinkable. This runs a script and counts what passes.
 *
 * The host module "spectest", which the tests import from, is the one
 * of the specification's reference interpreter (interpreter/host/
 * spectest.ml at the tag wg-1.0): functions that print, which here print
 * nothing; globals of 666 and 666.6; a table of 10 to 20 elements; a
 * memory of 1 to 2 pages.
 */

#include "wasm.h"
#include "spec.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ---------------------------------------------------------------- */
/* Enough JSON for wast2json's output: objects, arrays, strings and
 * numbers. */

typedef struct Json Json;
struct Json {
    char type;                  /* o object, a array, s string, n number */
    char *text;                 /* a string's or a number's */
    uint32_t len;               /* its length: a string may hold a 0 */
    char **keys;                /* an object's */
    Json **items;               /* an object's values, an array's items */
    int n;
};

static const char *jp;

static void space(void) { while (*jp == ' ' || *jp == '\n' || *jp == '\r' || *jp == '\t') jp++; }

static Json *parse(void);

static char *string(uint32_t *len)
{
    jp++;                       /* the opening quote */
    size_t cap = 16, n = 0;
    char *s = malloc(cap);
    while (*jp && *jp != '"') {
        char c = *jp++;
        if (c == '\\') {
            c = *jp++;
            if (c == 'n') c = '\n';
            else if (c == 't') c = '\t';
            else if (c == 'u') {    /* \u00XX: wast2json's escape for a byte */
                unsigned v;
                sscanf(jp, "%4x", &v);
                jp += 4;
                c = (char)v;
            }
        }
        if (n + 2 > cap)
            s = realloc(s, cap *= 2);
        s[n++] = c;
    }
    jp++;
    s[n] = 0;
    if (len)
        *len = (uint32_t)n;
    return s;
}

static Json *parse(void)
{
    Json *j = calloc(1, sizeof *j);
    space();
    if (*jp == '{' || *jp == '[') {
        char close = *jp == '{' ? '}' : ']';
        j->type = *jp == '{' ? 'o' : 'a';
        jp++;
        space();
        while (*jp != close) {
            j->items = realloc(j->items, sizeof(Json *) * (size_t)(j->n + 1));
            if (j->type == 'o') {
                j->keys = realloc(j->keys, sizeof(char *) * (size_t)(j->n + 1));
                j->keys[j->n] = string(NULL);
                space();
                jp++;           /* : */
            }
            j->items[j->n++] = parse();
            space();
            if (*jp == ',')
                jp++;
            space();
        }
        jp++;
    } else if (*jp == '"') {
        j->type = 's';
        j->text = string(&j->len);
    } else {
        const char *start = jp;
        while (*jp && !strchr(",}] \n", *jp))
            jp++;
        j->type = 'n';
        j->text = strndup(start, (size_t)(jp - start));
    }
    return j;
}

static Json *get(Json *o, const char *key)
{
    if (!o || o->type != 'o')
        return NULL;
    for (int i = 0; i < o->n; i++)
        if (strcmp(o->keys[i], key) == 0)
            return o->items[i];
    return NULL;
}

static const char *text(Json *o, const char *key)
{
    Json *j = get(o, key);
    return j ? j->text : NULL;
}

/* ---------------------------------------------------------------- */

static Store store;

typedef struct { char *name; uint32_t len; ModuleInst *inst; } Named;
static Named *registry, *named;
static int nregistry, nnamed;
static ModuleInst *current;

/* spectest */
static Extern spectest_global_i32, spectest_global_i64, spectest_global_f32,
              spectest_global_f64, spectest_table, spectest_memory;

static const char *print(void *context, const Value *args, Value *results)
{
    (void)context; (void)args; (void)results;
    return NULL;
}

static uint8_t param_types[2][2] = {{I32, F32}, {F64, F64}};

static int spectest(const Import *im, Extern *out)
{
    const char *n = im->name.s;
    if (strlen(n) != im->name.len)
        return 0;
    if (strncmp(n, "print", 5) == 0) {
        /* a function of the type the import asks for, if print has one */
        static const struct { const char *name; uint32_t n; uint8_t a, b; } prints[] = {
            {"print", 0, 0, 0}, {"print_i32", 1, I32, 0}, {"print_i64", 1, I64, 0},
            {"print_f32", 1, F32, 0}, {"print_f64", 1, F64, 0},
            {"print_i32_f32", 2, I32, F32}, {"print_f64_f64", 2, F64, F64},
        };
        for (size_t i = 0; i < sizeof prints / sizeof prints[0]; i++)
            if (strcmp(n, prints[i].name) == 0) {
                uint8_t *params = malloc(2);
                params[0] = prints[i].a;
                params[1] = prints[i].b;
                FuncType t = {prints[i].n, 0, params, 0};
                *out = (Extern){EXT_FUNC, wasm_host_func(&store, &t, print, NULL)};
                return 1;
            }
        return 0;
    }
    if (strcmp(n, "global_i32") == 0) { *out = spectest_global_i32; return 1; }
    if (strcmp(n, "global_i64") == 0) { *out = spectest_global_i64; return 1; }
    if (strcmp(n, "global_f32") == 0) { *out = spectest_global_f32; return 1; }
    if (strcmp(n, "global_f64") == 0) { *out = spectest_global_f64; return 1; }
    if (strcmp(n, "table") == 0) { *out = spectest_table; return 1; }
    if (strcmp(n, "memory") == 0) { *out = spectest_memory; return 1; }
    return 0;
}

/* Each script starts with a store of its own, as each runs in a process
 * of its own under the reference interpreter. */
static void start_store(void)
{
    memset(&store, 0, sizeof store);
    nregistry = nnamed = 0;
    (void)param_types;
    float f = 666.6f;
    double d = 666.6;
    uint32_t fb;
    uint64_t db;
    memcpy(&fb, &f, 4);
    memcpy(&db, &d, 8);
    spectest_global_i32 = (Extern){EXT_GLOBAL, wasm_new_global(&store, I32, 0, 666)};
    spectest_global_i64 = (Extern){EXT_GLOBAL, wasm_new_global(&store, I64, 0, 666)};
    spectest_global_f32 = (Extern){EXT_GLOBAL, wasm_new_global(&store, F32, 0, fb)};
    spectest_global_f64 = (Extern){EXT_GLOBAL, wasm_new_global(&store, F64, 0, db)};
    spectest_table = (Extern){EXT_TABLE, wasm_new_table(&store, (Limits){10, 20, 1})};
    spectest_memory = (Extern){EXT_MEM, wasm_new_mem(&store, (Limits){1, 2, 1})};
}

static ModuleInst *find(Named *list, int n, const char *name, uint32_t len)
{
    for (int i = n - 1; i >= 0; i--)
        if (list[i].len == len && memcmp(list[i].name, name, len) == 0)
            return list[i].inst;
    return NULL;
}

/* Every import resolved: from spectest, or a module registered. */
static const char *resolve(Module *m, Extern *out)
{
    for (uint32_t i = 0; i < m->nimports; i++) {
        Import *im = &m->imports[i];
        if (im->module.len == 8 && memcmp(im->module.s, "spectest", 8) == 0) {
            if (!spectest(im, &out[i]))
                return "unknown import";
            continue;
        }
        ModuleInst *mi = find(registry, nregistry, im->module.s, im->module.len);
        const Export *e = mi ? wasm_export(mi, im->name.s, im->name.len) : NULL;
        if (!e)
            return "unknown import";
        out[i] = wasm_extern(mi, e);
    }
    return NULL;
}

static uint8_t *read_file(const char *path, size_t *size)
{
    FILE *f = fopen(path, "rb");
    if (!f)
        return NULL;
    fseek(f, 0, SEEK_END);
    long n = ftell(f);
    fseek(f, 0, SEEK_SET);
    uint8_t *b = malloc((size_t)n + 1);
    *size = fread(b, 1, (size_t)n, f);
    fclose(f);
    return b;
}

/* What became of loading a module: which step failed, and why. */
enum { LOADED, MALFORMED, INVALID, UNLINKABLE, TRAPPED, NOFILE };

static int load(const char *dir, const char *file, ModuleInst **out, const char **why)
{
    char path[1024];
    snprintf(path, sizeof path, "%s/%s", dir, file);
    size_t size;
    uint8_t *bytes = read_file(path, &size);
    if (!bytes) {
        *why = "no file";
        return NOFILE;
    }
    Module *m = calloc(1, sizeof *m);
    if ((*why = wasm_decode(m, bytes, size)))
        return free(bytes), MALFORMED;
    free(bytes);
    if ((*why = wasm_validate(m)))
        return INVALID;
    Extern *imports = calloc(m->nimports + 1, sizeof(Extern));
    if ((*why = resolve(m, imports)))
        return free(imports), UNLINKABLE;
    int trapped;
    *why = wasm_instantiate(&store, m, imports, out, &trapped);
    free(imports);
    if (*why)
        return trapped ? TRAPPED : UNLINKABLE;
    return LOADED;
}

/* Is this result what was expected? A NaN may be expected only as
 * canonical (the payload with only its top bit) or arithmetic (that bit
 * set), with any sign. */
static int matches(Json *expect, Value v)
{
    const char *t = text(expect, "type"), *x = text(expect, "value");
    int f32 = strcmp(t, "f32") == 0;
    if (strncmp(x, "nan:", 4) == 0) {
        uint64_t exponent = f32 ? 0x7F800000u : 0x7FF0000000000000u;
        uint64_t quiet = f32 ? 0x00400000u : 0x0008000000000000u;
        uint64_t payload = f32 ? 0x007FFFFFu : 0x000FFFFFFFFFFFFFu;
        if ((v & exponent) != exponent)
            return 0;
        if (strcmp(x, "nan:canonical") == 0)
            return (v & payload) == quiet;
        return (v & quiet) != 0;
    }
    return v == strtoull(x, NULL, 10);
}

/* Invoke, or get a global. Returns the trap's message, or NULL. */
static const char *act(Json *action, Value *result, int *nresults, const char **problem)
{
    const char *module = text(action, "module");
    ModuleInst *mi = module ? find(named, nnamed, module, (uint32_t)strlen(module)) : current;
    *problem = NULL;
    if (!mi) {
        *problem = "no module";
        return NULL;
    }
    Json *field = get(action, "field");
    const Export *e = wasm_export(mi, field->text, field->len);
    if (!e) {
        *problem = "no such export";
        return NULL;
    }
    Extern x = wasm_extern(mi, e);
    if (strcmp(text(action, "type"), "get") == 0) {
        *result = store.globals[x.addr].value;
        *nresults = 1;
        return NULL;
    }
    Json *args = get(action, "args");
    Value a[64];
    for (int i = 0; args && i < args->n && i < 64; i++)
        a[i] = strtoull(text(args->items[i], "value"), NULL, 10);
    FuncInst *f = &store.funcs[x.addr];
    *nresults = (int)f->type.nresults;
    return wasm_invoke(&store, x.addr, a, result);
}

/* Do two messages agree? The suite's may say more than ours. */
static int same_message(const char *expected, const char *got)
{
    if (!got)
        return 0;
    size_t n = strlen(got);
    return strncmp(expected, got, n) == 0 || strncmp(got, expected, strlen(expected)) == 0;
}

int spec_run(const char *script, int verbose, Counts *c)
{
    size_t size;
    uint8_t *source = read_file(script, &size);
    if (!source) {
        perror(script);
        return 1;
    }
    source[size] = 0;
    char dir[1024];
    snprintf(dir, sizeof dir, "%s", script);
    char *slash = strrchr(dir, '/');
    if (slash)
        *slash = 0;
    else
        strcpy(dir, ".");
    jp = (const char *)source;
    Json *root = parse();
    Json *commands = get(root, "commands");
    start_store();
    current = NULL;
    nnamed = 0;

    for (int i = 0; commands && i < commands->n; i++) {
        Json *cmd = commands->items[i];
        const char *type = text(cmd, "type"), *line = text(cmd, "line");
        const char *why = NULL, *problem = NULL;
        int ok = 1, skipped = 0;
        ModuleInst *mi = NULL;
        char detail[256] = "";

        if (strcmp(type, "module") == 0) {
            int r = load(dir, text(cmd, "filename"), &mi, &why);
            ok = r == LOADED;
            if (ok) {
                current = mi;
                if (text(cmd, "name")) {
                    named = realloc(named, sizeof(Named) * (size_t)(nnamed + 1));
                    named[nnamed++] = (Named){strdup(text(cmd, "name")),
                                              (uint32_t)strlen(text(cmd, "name")), mi};
                }
            }
            snprintf(detail, sizeof detail, "module: %s", why ? why : "");
        } else if (strcmp(type, "register") == 0) {
            const char *n = text(cmd, "name");
            mi = n ? find(named, nnamed, n, (uint32_t)strlen(n)) : current;
            Json *as = get(cmd, "as");
            registry = realloc(registry, sizeof(Named) * (size_t)(nregistry + 1));
            char *copy = malloc(as->len + 1);
            memcpy(copy, as->text, as->len + 1);
            registry[nregistry++] = (Named){copy, as->len, mi};
            ok = mi != NULL;
        } else if (strcmp(type, "action") == 0 || strcmp(type, "assert_return") == 0) {
            Value result = 0;
            int nresults = 0;
            const char *t = act(get(cmd, "action"), &result, &nresults, &problem);
            Json *expected = get(cmd, "expected");
            if (problem || t)
                ok = 0, snprintf(detail, sizeof detail, "%s", problem ? problem : t);
            else if (strcmp(type, "assert_return") == 0) {
                if (expected && expected->n > 0)
                    ok = nresults == 1 && matches(expected->items[0], result);
                else
                    ok = nresults == 0;
                snprintf(detail, sizeof detail, "got %llu (0x%llx)",
                         (unsigned long long)result, (unsigned long long)result);
            }
        } else if (strcmp(type, "assert_trap") == 0 || strcmp(type, "assert_exhaustion") == 0) {
            Value result;
            int nresults;
            const char *t = act(get(cmd, "action"), &result, &nresults, &problem);
            ok = !problem && same_message(text(cmd, "text"), t);
            snprintf(detail, sizeof detail, "expected trap '%s', got '%s'",
                     text(cmd, "text"), problem ? problem : t ? t : "no trap");
        } else if (strcmp(type, "assert_malformed") == 0 || strcmp(type, "assert_invalid") == 0 ||
                   strcmp(type, "assert_unlinkable") == 0 || strcmp(type, "assert_uninstantiable") == 0) {
            const char *mt = text(cmd, "module_type");
            if (mt && strcmp(mt, "text") == 0)
                skipped = 1;    /* a test of the text format, not of this machine */
            else {
                int want = type[7] == 'm' ? MALFORMED : type[7] == 'i' ? INVALID
                         : type[9] == 'l' ? UNLINKABLE : TRAPPED;
                int r = load(dir, text(cmd, "filename"), &mi, &why);
                ok = r == want;
                if (ok && r == LOADED)
                    ok = 0;
                snprintf(detail, sizeof detail, "expected %s '%s', got %d: %s", type,
                         text(cmd, "text"), r, why ? why : "loaded");
            }
        } else {
            skipped = 1;
        }

        if (skipped)
            c->skipped++;
        else if (ok)
            c->passed++;
        else {
            c->failed++;
            if (verbose)
                printf("%s:%s: %s failed: %s\n", script, line, type, detail);
        }
    }
    free(source);
    return 0;
}
