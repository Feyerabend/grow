/*
 * A small Java Virtual Machine, from The Java Virtual Machine Specification,
 * Java SE 21 Edition (JVMS), read on docs.oracle.com: chapter 4 for the class
 * file and its verification by type checking (4.10.1), chapter 6 for the
 * instructions.
 *
 * It runs one class: static methods and static fields, int and int[], and
 * System.out as the only way out. Every method is verified before anything
 * runs, so the interpreter checks only what the specification says it must
 * check at run time: division by zero, array bounds, null and the length of
 * a new array.
 */
#ifndef JVM_H
#define JVM_H

#include <stdint.h>
#include <stddef.h>

/* The constant pool's tags, JVMS 4.4. */
enum {
    CP_UTF8 = 1, CP_INTEGER = 3, CP_FLOAT = 4, CP_LONG = 5, CP_DOUBLE = 6,
    CP_CLASS = 7, CP_STRING = 8, CP_FIELDREF = 9, CP_METHODREF = 10,
    CP_INTERFACE_METHODREF = 11, CP_NAME_AND_TYPE = 12, CP_METHOD_HANDLE = 15,
    CP_METHOD_TYPE = 16, CP_DYNAMIC = 17, CP_INVOKE_DYNAMIC = 18,
    CP_MODULE = 19, CP_PACKAGE = 20
};

typedef struct {
    uint8_t tag;
    uint16_t a, b;          /* indices into the pool, by tag */
    int32_t value;          /* CP_INTEGER */
    const char *utf8;       /* CP_UTF8, made a C string */
} Constant;

/* A value at run time. The verifier has proved what each one holds, so it
 * carries no tag: an int, or a pointer to an array, a string constant or
 * System.out. */
typedef intptr_t Value;

typedef struct {
    int32_t length;
    int32_t data[];
} Array;

typedef struct {
    uint16_t start_pc, line;
} Line;

typedef struct Method Method;
struct Method {
    uint16_t access;
    const char *name, *descriptor;
    int nargs;              /* slots taken by the arguments, this included */
    char returns;           /* 'V', 'I' or 'L' */
    /* the Code attribute */
    uint16_t max_stack, max_locals;
    uint32_t code_length;
    const uint8_t *code;
    uint16_t exceptions;    /* entries in exception_table */
    const uint8_t *stackmap;  /* the StackMapTable's entries, or NULL */
    uint16_t frames;        /* number_of_entries */
    uint32_t stackmap_length;
    Line *lines;
    int nlines;
};

typedef struct {
    uint16_t access;
    const char *name, *descriptor;
    Value value;            /* a static field's value */
} Field;

typedef struct {
    uint16_t major, minor;
    uint16_t count;         /* constant_pool_count */
    Constant *pool;
    uint16_t access;
    const char *name, *super;
    const char *source;     /* the SourceFile attribute, or NULL */
    int nfields, nmethods;
    Field *fields;
    Method *methods;
    void **resolved;        /* per constant: the Method or Field it names */
    uint8_t *bytes;         /* the file, which the methods' code points into */
    size_t size;
} Class;

/* class.c: read a class file; on failure, the message is in jvm_error */
Class *load_class(const char *path);
extern char jvm_error[300];
const char *cp_utf8(const Class *c, int i);         /* NULL if not a Utf8 */
const char *cp_class_name(const Class *c, int i);   /* NULL if not a Class */
int cp_member(const Class *c, int i, int tag,
              const char **cls, const char **name, const char **descriptor);
Method *find_method(Class *c, const char *name, const char *descriptor);
Field *find_field(Class *c, const char *name, const char *descriptor);
int line_of(const Method *m, int pc);

/* verify.c: 1 if every method checks; else 0, with the reason in jvm_error */
int verify_class(Class *c);
extern int verify_trace;    /* print each frame as it is checked */
extern const char *const opname[202];
int instruction_length(const uint8_t *code, uint32_t length, uint32_t pc);

/* run.c: run <clinit> and main; the exit status */
int run_class(Class *c);

#endif
