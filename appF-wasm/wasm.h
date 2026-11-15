/*
 * A WebAssembly 1.0 machine: the binary format decoded, every function
 * validated, the module instantiated, and its code run.
 *
 * Written from the WebAssembly Core Specification, W3C Recommendation,
 * 5 December 2019, https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/
 * Copyright (c) 2019 W3C (MIT, ERCIM, Keio, Beihang). This software
 * includes material derived from that document.
 */

#ifndef WASM_H
#define WASM_H

#include <stddef.h>
#include <stdint.h>

/* The four value types, by their codes in the binary format. */
enum { I32 = 0x7F, I64 = 0x7E, F32 = 0x7D, F64 = 0x7C };

/* A value is kept as its bits: an f32 in the low 32, so that a NaN keeps
 * its payload through every instruction that only moves it. */
typedef uint64_t Value;

typedef struct {
    uint32_t nparams, nresults;     /* in 1.0, nresults is 0 or 1 */
    uint8_t *params;
    uint8_t result;                 /* the result's type, if there is one */
} FuncType;

typedef struct { uint32_t min, max; int has_max; } Limits;

/* A name: bytes of UTF-8, which may hold a 0, so with their length. */
typedef struct { char *s; uint32_t len; } Name;

/* The kinds of import and export. */
enum { EXT_FUNC, EXT_TABLE, EXT_MEM, EXT_GLOBAL };

typedef struct {
    Name module, name;
    int kind;
    uint32_t type;                  /* a function's type index */
    Limits limits;                  /* a table's or a memory's */
    uint8_t valtype, mut;           /* a global's */
} Import;

typedef struct { Name name; int kind; uint32_t index; } Export;

typedef struct {
    uint8_t valtype, mut;
    const uint8_t *init;            /* a constant expression */
    size_t init_len;
} Global;

typedef struct {
    uint32_t table;                 /* 0, the only table 1.0 allows */
    const uint8_t *offset;          /* a constant expression */
    size_t offset_len;
    uint32_t count, *funcs;
} Elem;

typedef struct {
    uint32_t mem;                   /* 0, the only memory 1.0 allows */
    const uint8_t *offset;
    size_t offset_len;
    const uint8_t *bytes;
    uint32_t len;
} Data;

typedef struct {
    uint32_t type;                  /* index into the module's types */
    uint32_t nlocals;               /* past the parameters */
    uint8_t *locals;
    const uint8_t *body;            /* the expression, ending with end */
    size_t len;
    /* Made by validation: for a block, loop or if at offset o in the
     * body, where its else and its end are. */
    int32_t *ends, *elses;
    uint32_t max_labels;            /* the deepest the blocks nest */
    uint32_t max_stack;             /* the most operands at once */
} Code;

/* A module as decoded: everything points into the bytes it came from. */
typedef struct {
    uint8_t *bytes;
    size_t size;
    FuncType *types; uint32_t ntypes;
    Import *imports; uint32_t nimports;
    uint32_t nfuncimports, ntableimports, nmemimports, nglobalimports;
    uint32_t *funcs; uint32_t nfuncs;   /* type index of each defined function */
    Limits *tables; uint32_t ntables;
    Limits *mems; uint32_t nmems;
    Global *globals; uint32_t nglobals;
    Export *exports; uint32_t nexports;
    int64_t start;                      /* -1 if none */
    Elem *elems; uint32_t nelems;
    Data *datas; uint32_t ndatas;
    Code *codes; uint32_t ncodes;
} Module;

/* The store: every function, table, memory and global instance, of every
 * module instantiated, reached by address. */
typedef struct ModuleInst ModuleInst;
typedef const char *(*HostFunc)(void *context, const Value *args, Value *results);

typedef struct {
    FuncType type;
    ModuleInst *module;             /* NULL for a host function */
    Code *code;
    HostFunc host;
    void *context;
} FuncInst;

typedef struct { uint32_t size; Limits limits; int32_t *elems; } TableInst;
typedef struct { uint32_t pages; Limits limits; uint8_t *data; } MemInst;
typedef struct { uint8_t valtype, mut; Value value; } GlobalInst;

struct ModuleInst {
    Module *module;
    FuncType *types; uint32_t ntypes;
    uint32_t *funcs; uint32_t nfuncs;   /* store addresses */
    uint32_t table, mem;                /* store addresses, or UINT32_MAX */
    uint32_t *globals; uint32_t nglobals;
    Export *exports; uint32_t nexports;
};

typedef struct {
    FuncInst *funcs; uint32_t nfuncs, capfuncs;
    TableInst **tables; uint32_t ntables, captables;
    MemInst **mems; uint32_t nmems, capmems;
    GlobalInst *globals; uint32_t nglobals, capglobals;
} Store;

/* An external value: what an import is given, or an export gives. */
typedef struct { int kind; uint32_t addr; } Extern;

/* Each returns NULL on success, or a message saying what is wrong. */
const char *wasm_decode(Module *m, const uint8_t *bytes, size_t size);
const char *wasm_validate(Module *m);
/* trapped is set when the start function trapped, not a link failing */
const char *wasm_instantiate(Store *s, Module *m, const Extern *imports,
                             ModuleInst **out, int *trapped);
const char *wasm_invoke(Store *s, uint32_t funcaddr, const Value *args,
                        Value *results);

uint32_t wasm_host_func(Store *s, const FuncType *type, HostFunc f, void *context);
uint32_t wasm_new_table(Store *s, Limits limits);
uint32_t wasm_new_mem(Store *s, Limits limits);
uint32_t wasm_new_global(Store *s, uint8_t valtype, uint8_t mut, Value v);

/* The export of this name, or NULL. */
const Export *wasm_export(const ModuleInst *mi, const char *name, uint32_t len);
/* The external value an export gives. */
Extern wasm_extern(const ModuleInst *mi, const Export *e);

/* Counts, kept as the machine runs: instructions and calls. */
extern uint64_t wasm_steps, wasm_calls;

#endif
