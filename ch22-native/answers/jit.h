/*
 * Exercise 22.3: a small JIT for arm64, for verified programs.
 *
 * Every run of instructions that it can translate, PUSH, ADD, LOAD, STORE,
 * JZ and JMP, and with -DJIT_MORE also SUB and AND, becomes machine code,
 * in memory from mmap made executable. Each instruction of a run is also an
 * entry: the interpreter's threaded code gets, at its address, the label of
 * a handler that calls the machine code there. The code runs until it
 * reaches an instruction it cannot translate, or a jump out of the run, and
 * returns the address it stopped at; the interpreter runs that instruction
 * itself, and goes on. Everything else is the interpreter's.
 *
 * Traps are the interpreter's too. Before an instruction changes anything,
 * the machine code makes the checks the interpreter would make there, that
 * the stack has room and that values are numbers, and if one fails it stops
 * at that instruction, and the interpreter runs it, and traps, with its own
 * message, at its own address. The checks the verifier made are not made.
 *
 * The code is called as  int f(struct value *stack, int *sp, int fp)
 *
 *   x0  the stack           x9   sp, kept in a register while the code runs
 *   x1  where sp is kept    x10-x13  scratch
 *   x2  fp
 *
 * A value is eight bytes: is_ref in the low four, n in the high four. So a
 * number n is n << 32; two numbers add, subtract and and as 64-bit words,
 * wrapping as the machine's arithmetic wraps; and a value is a number 0
 * exactly when all 64 bits are 0.
 */

#include <libkern/OSCacheControl.h>
#include <pthread.h>
#include <sys/mman.h>

typedef int (*native_code)(struct value *, int *, int);
static native_code *native;         /* by address: its entry, or NULL */
static int jit_instructions = 0, jit_runs = 0, jit_words = 0;

static uint32_t *buf;
static int at, limit;

static void emit(uint32_t w) {
    if (at == limit) {
        fprintf(stderr, "out of memory for machine code\n");
        exit(2);
    }
    buf[at++] = w;
}

/* The arm64 instructions used, as words. */
#define LDR_W9_X1       0xB9400029u                     /* ldr w9, [x1] */
#define STR_W9_X1       0xB9000029u                     /* str w9, [x1] */
#define MOV_W2_W2       0x2A0203E2u                     /* mov w2, w2: clear the top */
#define A64_RET         0xD65F03C0u
static uint32_t movz_w0(int imm) { return 0x52800000u | (uint32_t) (imm & 0xFFFF) << 5; }
static uint32_t movk_w0_16(int imm) { return 0x72A00000u | (uint32_t) (imm & 0xFFFF) << 5; }
static uint32_t movz_x_32(int d, uint32_t imm) { return 0xD2C00000u | (imm & 0xFFFF) << 5 | d; }
static uint32_t movk_x_48(int d, uint32_t imm) { return 0xF2E00000u | (imm & 0xFFFF) << 5 | d; }
static uint32_t cmp_x_imm(int n, int imm) { return 0xF100001Fu | (uint32_t) imm << 10 | n << 5; }
static uint32_t add_x_imm(int d, int n, int imm) { return 0x91000000u | (uint32_t) imm << 10 | n << 5 | d; }
static uint32_t sub_x_imm(int d, int n, int imm) { return 0xD1000000u | (uint32_t) imm << 10 | n << 5 | d; }
static uint32_t add_x(int d, int n, int m) { return 0x8B000000u | m << 16 | n << 5 | d; }
static uint32_t sub_x(int d, int n, int m) { return 0xCB000000u | m << 16 | n << 5 | d; }
static uint32_t and_x(int d, int n, int m) { return 0x8A000000u | m << 16 | n << 5 | d; }
static uint32_t ldr_x_idx(int t, int n, int m) { return 0xF8607800u | m << 16 | n << 5 | t; }
static uint32_t str_x_idx(int t, int n, int m) { return 0xF8207800u | m << 16 | n << 5 | t; }

/* Branches, filled in once every place is known. */
enum { B, BEQ, CBZ_X10, CBNZ_W10, CBNZ_W11 };
struct fixup { int at, kind, to_pc; };
static struct fixup *fixups;
static int nfixups;

static void branch(int kind, int to_pc) {
    fixups[nfixups].at = at;
    fixups[nfixups].kind = kind;
    fixups[nfixups].to_pc = to_pc;
    nfixups++;
    emit(0);
}

static int jittable(int op) {
    switch (op) {
    case PUSH: case ADD: case LOAD: case STORE: case JZ: case JMP:
        return 1;
#ifdef JIT_MORE
    case SUB: case AND:
        return 1;
#endif
    }
    return 0;
}

/* Translate one run, from s to e, the addresses where its instructions begin. */
static void run_of(const int *starts, int count) {
    int *body = calloc(code_len + 1, sizeof (int));     /* where each instruction's code is */
    int *exits = malloc((code_len + 1) * sizeof (int));
    int *entries = malloc(count * sizeof (int));
    int k, first_fixup = nfixups;

    for (k = 0; k <= code_len; k++)
        exits[k] = -1;
    /* An entry for each instruction: load sp, and go to its code. */
    for (k = 0; k < count; k++) {
        entries[k] = at;
        emit(MOV_W2_W2);
        emit(LDR_W9_X1);
        branch(B, starts[k]);
    }
    for (k = 0; k < count; k++) {
        int a = starts[k], op = code[a];
        body[a] = at + 1;               /* +1: 0 means none */
        switch (op) {
        case PUSH: {
            uint32_t n = (uint32_t) code[a + 1];
            emit(cmp_x_imm(9, STACK_SIZE));
            branch(BEQ, -a - 1);            /* full: stop here, and let it trap */
            emit(movz_x_32(10, n & 0xFFFF));
            emit(movk_x_48(10, n >> 16));
            emit(str_x_idx(10, 0, 9));
            emit(add_x_imm(9, 9, 1));
            break;
        }
        case LOAD:
            emit(cmp_x_imm(9, STACK_SIZE));
            branch(BEQ, -a - 1);
            emit(add_x_imm(11, 2, code[a + 1]));
            emit(ldr_x_idx(10, 0, 11));
            emit(str_x_idx(10, 0, 9));
            emit(add_x_imm(9, 9, 1));
            break;
        case STORE:
            emit(sub_x_imm(9, 9, 1));
            emit(ldr_x_idx(10, 0, 9));
            emit(add_x_imm(11, 2, code[a + 1]));
            emit(str_x_idx(10, 0, 11));
            break;
        case ADD: case SUB: case AND:
            emit(sub_x_imm(12, 9, 2));      /* v, the first */
            emit(sub_x_imm(13, 9, 1));      /* w, on top */
            emit(ldr_x_idx(10, 0, 12));
            emit(ldr_x_idx(11, 0, 13));
            branch(CBNZ_W10, -a - 1);       /* a reference: stop, and let it trap */
            branch(CBNZ_W11, -a - 1);
            emit(op == ADD ? add_x(10, 10, 11) : op == SUB ? sub_x(10, 10, 11) : and_x(10, 10, 11));
            emit(str_x_idx(10, 0, 12));
            emit(sub_x_imm(9, 9, 1));
            break;
        case JZ:
            emit(sub_x_imm(9, 9, 1));
            emit(ldr_x_idx(10, 0, 9));
            branch(CBZ_X10, code[a + 1]);
            break;
        case JMP:
            branch(B, code[a + 1]);
            break;
        }
        jit_instructions++;
    }
    /* After the last, if it goes on: stop at the next. */
    {
        int last = starts[count - 1];
        if (code[last] != JMP)
            branch(B, last + 1 + noperands[code[last]]);
    }
    /*
     * Fill in the branches. A branch to an instruction of this run goes to
     * its code; any other, and every stop (written as -a - 1), to a stub
     * that puts sp back and returns the address.
     */
    for (k = first_fixup; k < nfixups; k++) {
        struct fixup *f = &fixups[k];
        int target, p = f->to_pc < 0 ? -f->to_pc - 1 : f->to_pc;
        int32_t off;
        if (f->to_pc >= 0 && body[p])
            target = body[p] - 1;
        else {
            if (exits[p] < 0) {
                exits[p] = at;
                emit(STR_W9_X1);
                emit(movz_w0(p));
                emit(movk_w0_16(p >> 16));
                emit(A64_RET);
            }
            target = exits[p];
        }
        off = target - f->at;
        switch (f->kind) {
        case B:        buf[f->at] = 0x14000000u | ((uint32_t) off & 0x3FFFFFF); break;
        case BEQ:      buf[f->at] = 0x54000000u | ((uint32_t) off & 0x7FFFF) << 5; break;
        case CBZ_X10:  buf[f->at] = 0xB4000000u | ((uint32_t) off & 0x7FFFF) << 5 | 10; break;
        case CBNZ_W10: buf[f->at] = 0x35000000u | ((uint32_t) off & 0x7FFFF) << 5 | 10; break;
        case CBNZ_W11: buf[f->at] = 0x35000000u | ((uint32_t) off & 0x7FFFF) << 5 | 11; break;
        }
    }
    nfixups = first_fixup;
    for (k = 0; k < count; k++)
        native[starts[k]] = (native_code) (void *) (buf + entries[k]);
    jit_runs++;
    free(body);
    free(exits);
    free(entries);
}

static void jit(void) {
    size_t bytes;
    int a, *starts = malloc((code_len + 1) * sizeof (int)), count = 0;

    native = calloc(code_len + 1, sizeof (native_code));
    fixups = malloc(4 * (code_len + 1) * sizeof (struct fixup));
    limit = 24 * (code_len + 1) + 64;
    bytes = (size_t) limit * 4;
    buf = mmap(NULL, bytes, PROT_READ | PROT_WRITE | PROT_EXEC,
               MAP_PRIVATE | MAP_ANON | MAP_JIT, -1, 0);
    if (buf == MAP_FAILED || !native || !fixups || !starts) {
        fprintf(stderr, "cannot make memory for machine code\n");
        exit(2);
    }
    pthread_jit_write_protect_np(0);            /* writable, not executable */
    /* The program is verified: read from the start, every instruction is whole. */
    for (a = 0; a < code_len; a += 1 + noperands[code[a]]) {
        if (jittable(code[a]))
            starts[count++] = a;
        else if (count > 0) {
            run_of(starts, count);
            count = 0;
        }
    }
    if (count > 0)
        run_of(starts, count);
    pthread_jit_write_protect_np(1);            /* executable, not writable */
    sys_icache_invalidate(buf, bytes);
    jit_words = at;
    free(starts);
}
