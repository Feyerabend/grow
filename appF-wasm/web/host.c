/*
 * Appendix F's machine for a web page: wasm.c, as it stands, compiled to
 * WebAssembly 1.0, with this file as its host in place of main.c and
 * program.c. It runs chapter 23's machine, vm.wasm, on a .vm program,
 * as program.c's -m does, and so is a WebAssembly machine running a
 * WebAssembly module, inside a browser's own.
 *
 * There is no C library. The headers in libc/ say what wasm.c gets
 * instead: memory, taken and never given back, since the page makes a
 * new machine for every run; WebAssembly's own instructions for the
 * mathematics; and, for longjmp, a call to the page, which throws.
 *
 * The page gives two functions: web_write(c), a byte of output, and
 * web_fail(kind, message), which does not return: kind 0 is a module
 * refused, decoding or validating it, and kind 1 a trap.
 */

#include "../wasm.c"

#define IMPORT(name) __attribute__((import_module("env"), import_name(#name)))
#define EXPORT(name) __attribute__((export_name(#name)))

IMPORT(web_write) void web_write(int c);
IMPORT(web_fail) __attribute__((noreturn)) void web_fail(int kind, const char *message);

/* ---- what the C library would have given ---- */

extern unsigned char __heap_base;
static uintptr_t heap_top;

void *malloc(size_t n)
{
    if (!heap_top)
        heap_top = (uintptr_t)&__heap_base;
    uintptr_t p = (heap_top + 15) & ~(uintptr_t)15;
    uintptr_t end = p + 16 + n;             /* 16 bytes before it: its size */
    size_t have = __builtin_wasm_memory_size(0) * 65536;
    if (end > have &&
        __builtin_wasm_memory_grow(0, (end - have + 65535) / 65536) == (size_t)-1)
        return NULL;
    *(size_t *)p = n;
    heap_top = end;
    return (void *)(p + 16);
}

/* New memory is all zeros, and none is used twice. */
void *calloc(size_t n, size_t size) { return malloc(n * size); }

void free(void *p) { (void)p; }

void *realloc(void *p, size_t n)
{
    void *q = malloc(n);
    if (q && p) {
        size_t old = *(size_t *)((uintptr_t)p - 16);
        memcpy(q, p, old < n ? old : n);
    }
    return q;
}

void exit(int status)
{
    (void)status;
    web_fail(1, "the machine ran out of memory");
}

void *memcpy(void *to, const void *from, size_t n)
{
    unsigned char *t = to;
    const unsigned char *f = from;
    while (n--) *t++ = *f++;
    return to;
}

void *memmove(void *to, const void *from, size_t n)
{
    unsigned char *t = to;
    const unsigned char *f = from;
    if (t < f)
        while (n--) *t++ = *f++;
    else
        while (n--) t[n] = f[n];
    return to;
}

void *memset(void *p, int c, size_t n)
{
    unsigned char *q = p;
    while (n--) *q++ = (unsigned char)c;
    return p;
}

int memcmp(const void *a, const void *b, size_t n)
{
    const unsigned char *x = a, *y = b;
    for (; n; n--, x++, y++)
        if (*x != *y) return *x - *y;
    return 0;
}

size_t strlen(const char *s)
{
    size_t n = 0;
    while (s[n]) n++;
    return n;
}

int strcmp(const char *a, const char *b)
{
    while (*a && *a == *b) a++, b++;
    return (unsigned char)*a - (unsigned char)*b;
}

/* longjmp: say why to the page, which throws. wasm.c's two places to
 * jump back to are failing, while decoding and validating, and trapping. */
void web_longjmp(int *b)
{
    if (b == failed)
        web_fail(0, failure);
    web_fail(1, trap_message);
}

/* ---- the host, as program.c's for -m ---- */

static Store the_store;
static ModuleInst *instance;
static char message[256];

static const char *put(void *context, const Value *args, Value *results)
{
    (void)context; (void)results;
    web_write((int)(uint8_t)args[0]);
    return NULL;
}

/* chapter 23's host_trap(why, at): why is a C string in the module's
 * memory; the message is run.mjs's. */
static const char *host_trap(void *context, const Value *args, Value *results)
{
    (void)context; (void)results;
    MemInst *m = the_store.mems[instance->mem];
    uint32_t a = (uint32_t)args[0];
    size_t n = 0;
    memcpy(message, "trap: ", 6);
    while (6 + n + 24 < sizeof message && a + n < (uint64_t)m->pages * 65536 && m->data[a + n])
        message[6 + n] = (char)m->data[a + n], n++;
    char *p = message + 6 + n;
    memcpy(p, " at ", 4), p += 4;
    int32_t at = (int32_t)args[1];
    if (at < 0) *p++ = '-', at = -at;
    char digits[12];
    int k = 0;
    do digits[k++] = (char)('0' + at % 10); while (at /= 10);
    while (k) *p++ = digits[--k];
    *p = 0;
    return message;
}

/* A buffer of n bytes for the page to write a module or a program into. */
EXPORT(web_buffer) uint8_t *web_buffer(uint32_t n) { return malloc(n); }

/* Decode, validate and instantiate the module of size bytes at bytes,
 * giving it env.host_write, env.host_trap and env.putchar. A refusal
 * throws, through longjmp; a module that will not link returns why. */
EXPORT(web_load) const char *web_load(const uint8_t *bytes, uint32_t size)
{
    Module *m = calloc(1, sizeof *m);
    const char *why = wasm_decode(m, bytes, size);
    if (!why)
        why = wasm_validate(m);
    if (why)
        return why;
    Extern *imports = calloc(m->nimports + 1, sizeof(Extern));
    for (uint32_t i = 0; i < m->nimports; i++) {
        Import *im = &m->imports[i];
        HostFunc f = NULL;
        if (im->kind == EXT_FUNC && strcmp(im->module.s, "env") == 0) {
            if (strcmp(im->name.s, "host_write") == 0 || strcmp(im->name.s, "putchar") == 0)
                f = put;
            else if (strcmp(im->name.s, "host_trap") == 0)
                f = host_trap;
        }
        if (!f)
            return "unknown import";
        imports[i] = (Extern){EXT_FUNC, wasm_host_func(&the_store, &m->types[im->type], f, NULL)};
    }
    int trapped;
    return wasm_instantiate(&the_store, m, imports, &instance, &trapped);
}

static Value call(const char *name, Value a, Value b)
{
    const Export *e = wasm_export(instance, name, (uint32_t)strlen(name));
    if (!e || e->kind != EXT_FUNC)
        web_fail(1, "no such function in the module");
    Value args[2] = {a, b}, result = 0;
    const char *t = wasm_invoke(&the_store, instance->funcs[e->index], args, &result);
    if (t)
        web_fail(1, t);
    return result;
}

/* Run chapter 23's machine, loaded by web_load, on the .vm file of size
 * bytes at file. Returns NULL, or why the file was refused. */
EXPORT(web_run_vm) const char *web_run_vm(const uint8_t *file, uint32_t size)
{
    uint32_t input = (uint32_t)call("vm_input", 0, 0);
    uint32_t room = (uint32_t)call("vm_input_size", 0, 0);
    if (size > room)
        size = room;
    memcpy(the_store.mems[instance->mem]->data + input, file, size);
    uint32_t refused = (uint32_t)call("vm_load", size, 0);
    if (refused)
        return (const char *)the_store.mems[instance->mem]->data + refused;
    call("vm_set_collector", 0, 0);
    call("vm_reset", 0, 0);
    call("vm_run", 0, 0);
    return NULL;
}

/* How many WebAssembly instructions appendix F's machine has run. */
EXPORT(web_steps) double web_steps(void) { return (double)wasm_steps; }
