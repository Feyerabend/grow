/*
 * Running programs: a module made by a C compiler, and the book's own
 * machine of chapter 23, compiled to WebAssembly.
 *
 *     wasm program.wasm
 *
 * runs a module that imports env.putchar (one i32, the byte to write)
 * and exports main, which returns the exit status: what each C program in programs/
 * becomes, compiled by clang for wasm32.
 *
 *     wasm -m vm.wasm [-g copy] [-S] program.vm
 *
 * runs chapter 23's machine, core.c compiled to WebAssembly, on a .vm
 * file, as its run.mjs does under Node.js: the module imports
 * env.host_write and env.host_trap, and the same messages come out, so
 * that chapter 23's conform.py can test it.
 */

#include "wasm.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static Store store;
static ModuleInst *instance;

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

static const char *put(void *context, const Value *args, Value *results)
{
    (void)context;
    (void)results;
    putchar((int)(uint8_t)args[0]);
    return NULL;
}

/* chapter 23's host_trap(why, at): why is a C string in the module's
 * memory. The trap ends the run, and its message is run.mjs's. */
static const char *host_trap(void *context, const Value *args, Value *results)
{
    (void)context;
    (void)results;
    static char message[256];
    MemInst *m = store.mems[instance->mem];
    uint32_t a = (uint32_t)args[0];
    char why[200];
    size_t n = 0;
    while (n + 1 < sizeof why && a + n < (uint64_t)m->pages * 65536 && m->data[a + n])
        why[n] = (char)m->data[a + n], n++;
    why[n] = 0;
    snprintf(message, sizeof message, "trap: %s at %d", why, (int32_t)args[1]);
    return message;
}

/* The host functions a module may import from env. */
typedef struct { const char *name; HostFunc f; } Host;

static const char *load(const char *path, const Host *hosts, int nhosts)
{
    size_t size;
    uint8_t *bytes = read_file(path, &size);
    if (!bytes)
        return "cannot open";
    Module *m = calloc(1, sizeof *m);
    const char *why = wasm_decode(m, bytes, size);
    free(bytes);
    if (!why)
        why = wasm_validate(m);
    if (why)
        return why;
    Extern *imports = calloc(m->nimports + 1, sizeof(Extern));
    for (uint32_t i = 0; i < m->nimports; i++) {
        Import *im = &m->imports[i];
        int found = 0;
        for (int h = 0; h < nhosts && !found; h++)
            if (im->kind == EXT_FUNC && strcmp(im->module.s, "env") == 0 &&
                strcmp(im->name.s, hosts[h].name) == 0) {
                imports[i] = (Extern){EXT_FUNC,
                    wasm_host_func(&store, &m->types[im->type], hosts[h].f, NULL)};
                found = 1;
            }
        if (!found)
            return "unknown import";
    }
    int trapped;
    why = wasm_instantiate(&store, m, imports, &instance, &trapped);
    free(imports);
    return why;
}

static uint32_t function(const char *name)
{
    const Export *e = wasm_export(instance, name, (uint32_t)strlen(name));
    if (!e || e->kind != EXT_FUNC) {
        fprintf(stderr, "wasm: no function %s\n", name);
        exit(2);
    }
    return instance->funcs[e->index];
}

static Value call(const char *name, Value a, Value b)
{
    Value args[2] = {a, b}, result = 0;
    const char *t = wasm_invoke(&store, function(name), args, &result);
    if (t) {
        fflush(stdout);
        fprintf(stderr, "%s\n", t);
        exit(1);
    }
    return result;
}

/* chapter 23's machine, as run.mjs drives it */
static int run_vm(int argc, char **argv)
{
    const char *module = argv[1], *path = argv[argc - 1];
    int copying = 0, stress = 0;
    for (int i = 2; i < argc - 1; i++) {
        if (strcmp(argv[i], "copy") == 0) copying = 1;
        if (strcmp(argv[i], "-S") == 0) stress = 1;
    }
    static const Host hosts[] = {{"host_write", put}, {"host_trap", host_trap}};
    const char *why = load(module, hosts, 2);
    if (why) {
        fprintf(stderr, "%s: %s\n", module, why);
        return 2;
    }
    size_t size;
    uint8_t *file = read_file(path, &size);
    if (!file) {
        fprintf(stderr, "%s: cannot open\n", path);
        return 2;
    }
    uint32_t input = (uint32_t)call("vm_input", 0, 0);
    uint32_t room = (uint32_t)call("vm_input_size", 0, 0);
    if (size > room)
        size = room;
    memcpy(store.mems[instance->mem]->data + input, file, size);
    uint32_t refused = (uint32_t)call("vm_load", size, 0);
    if (refused) {
        MemInst *m = store.mems[instance->mem];
        fprintf(stderr, "%s: %s\n", path, (char *)m->data + refused);
        return 2;
    }
    call("vm_set_collector", (Value)copying, (Value)stress);
    call("vm_reset", 0, 0);
    call("vm_run", 0, 0);
    fflush(stdout);
    return 0;
}

int run_program(int argc, char **argv)
{
    if (strcmp(argv[0], "-m") == 0 && argc >= 3)
        return run_vm(argc, argv);
    static const Host hosts[] = {{"putchar", put}};
    const char *why = load(argv[0], hosts, 1);
    if (why) {
        fprintf(stderr, "%s: %s\n", argv[0], why);
        return 2;
    }
    int status = (int)(int32_t)call("main", 0, 0);
    fflush(stdout);
    return status;
}
