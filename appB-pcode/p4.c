/*
 * The P4 machine: the p-code of Pascal-P4 (Zurich, 1976), the last of
 * the portable Pascal-P compilers, in C.
 *
 * Pascal-P4 is two programs in Pascal. pcom compiles Pascal to p-code,
 * as text; pint reads that text, assembles it, and runs it. This is a
 * second pint. It reads the same text, keeps the same store with the
 * same layout and limits, and runs every instruction as pint does, so
 * that a program prints the same here as there, to the character. It
 * was written from Pemberton and Daniels's account of pint in Pascal
 * Implementation (chapters 10 to 12), with pint.p open where the book
 * does not say: the form of each operand, the sizes of the tables, and
 * exactly where new and ent find the store full.
 *
 * Where pint leaves a thing to chance, this machine stops: an address
 * outside the store, a jump to where there is no instruction, a
 * division by zero, a label used and never defined. With -u it also
 * stops at a variable used before it has a value.
 *
 *     p4 [-t] [-u] [-s] program.p4 [prr]
 *
 * -t traces each instruction on stderr; -s counts them, and prints the
 * counts on stderr at the end. prr, if given, is the file the program
 * writes as prr; without it, prr goes to stdout, as under pint.
 *
 * The store is an array of words. Every value of every type takes one
 * word: integers, reals, characters, booleans, sets, and addresses,
 * which are indices into the store. pint keeps the types apart by the
 * variant it reads a word through; here a word is a union, and the
 * instruction says which part to read.
 *
 *   0 .. MAXSTK        the stack, growing up from 0, and the heap,
 *                      growing down from MAXSTK
 *   MAXSTK+1 .. OVERM  the constants the loader puts aside: large
 *                      integers, reals, sets, pairs of bounds, strings
 *
 * nil is MAXSTR, one past the end, an address nothing can reach.
 */

#include <ctype.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* pint's sizes, from pint.p. The tables of constants are smaller than
 * their comments in pint.p say: a table is full when its pointer
 * reaches its end, and the entry that fills it is refused, so the
 * tables of large integers and of reals hold three constants each, not
 * five. */
enum {
    PCMAX = 17500,      /* the most instructions */
    MAXSTK = 13650,     /* the stack and the heap */
    OVERI = MAXSTK + 5, /* the end of the table of large integers */
    OVERR = OVERI + 5,  /* of reals */
    OVERS = OVERR + 70, /* of sets */
    OVERB = OVERS + 90, /* of pairs of bounds */
    OVERM = OVERB + 4180, /* of strings, and of the store */
    MAXSTR = OVERM + 1, /* nil */
    LARGEINT = 26144,   /* an integer this large goes in the table */
    BEGINCODE = 3,      /* the program is placed from here */
    MAXLABEL = 1850,
    STRLEN = 16,        /* a string constant is 16 characters */
    INPUT = 5, OUTPUT = 6, PRD = 7, PRR = 8,    /* the files' words */
};

/* The opcodes are pint's numbers, so that a trap here prints the same
 * register line as pint does. An instruction with a type letter has one
 * number for each type: lodi is LOD, and loda to lodc are 105 to 109, in
 * the order a, r, s, b, c. */
enum {
    LOD, LDO, STR, SRO, LDA, LAO, STO, LDC, LCI, IND, INC, MST, CUP, ENT,
    RET, CSP, IXA, EQU, NEQ, GEQ, GRT, LEQ, LES, UJP, FJP, XJP, CHK, EOF_,
    ADI, ADR, SBI, SBR, SGS, FLT, FLO, TRC, NGI, NGR, SQI, SQR, ABI, ABR,
    NOT, AND, IOR, DIF, INT, UNI, INN, MOD, ODD, MPI, MPR, DVI, DVR, MOV,
    LCA, DEC, STP, ORD, CHR, UJC,
    NINSTR,
    /* the typed forms: the base number for the type letter i, these for
     * a, r, s, b and c */
    LDOT = 65, STRT = 70, SROT = 75, STOT = 80, INDT = 85, INCT = 90,
    CHKT = 95, DECT = 100, LODT = 105,
    CHKA = CHKT,
    NONE = 255,         /* no instruction here */
};

static const char *names[NINSTR] = {
    "lod", "ldo", "str", "sro", "lda", "lao", "sto", "ldc", "...", "ind",
    "inc", "mst", "cup", "ent", "ret", "csp", "ixa", "equ", "neq", "geq",
    "grt", "leq", "les", "ujp", "fjp", "xjp", "chk", "eof", "adi", "adr",
    "sbi", "sbr", "sgs", "flt", "flo", "trc", "ngi", "ngr", "sqi", "sqr",
    "abi", "abr", "not", "and", "ior", "dif", "int", "uni", "inn", "mod",
    "odd", "mpi", "mpr", "dvi", "dvr", "mov", "lca", "dec", "stp", "ord",
    "chr", "ujc",
};

/* The standard procedures, called by csp q. */
enum {
    GET, PUT, RST, RLN, NEW, WLN, WRS, ELN, WRI, WRR, WRC, RDI, RDR, RDC,
    SIN, COS, EXP, LOG, SQT, ATN, SAV, NSP,
};

static const char *spnames[NSP] = {
    "get", "put", "rst", "rln", "new", "wln", "wrs", "eln", "wri", "wrr",
    "wrc", "rdi", "rdr", "rdc", "sin", "cos", "exp", "log", "sqt", "atn",
    "sav",
};

/* A set is a word of bits; P4's sets hold 0 to 58. */
enum { SETMAX = 58 };

typedef union {
    int32_t i;          /* integers, characters, booleans, addresses */
    double r;
    uint64_t s;
} Word;

static Word store[OVERM + 1];
static unsigned char defined[OVERM + 1];    /* has the word a value? */

static unsigned char op[PCMAX + 1];
static unsigned char pp[PCMAX + 1];
static int32_t qq[PCMAX + 1];

static int32_t pc, sp, mp, np, ep;
static int instr, p;            /* the instruction running, and its p */
static int32_t q;               /* and its q */

static int undefined_traps;     /* -u */
static int tracing;             /* -t */
static long counts[256];        /* -s */
static int counting;

/* ---------------------------------------------------------------- */
/* Files. A Pascal text file has a window, f^, onto its next character.
 * Here a file holds that character in ahead, or EOF at the end. pint's
 * files are those of Free Pascal, and these do what Free Pascal's do,
 * as far as can be seen from a program: at the end of a line the window
 * holds the newline, reading it gives a space, and at the end of the
 * file the window holds 0. */

typedef struct {
    FILE *f;
    int ahead;
    int waiting;        /* the first character is not read yet */
} Text;

static Text input, prd;
static FILE *output, *prr;

/* The first character is read only when the program first looks at the
 * file, so that a program that reads nothing does not wait for input
 * from a keyboard. (pint reads it at once.) */
static void text_open(Text *t, FILE *f) { t->f = f; t->waiting = 1; }

static Text *ready(Text *t)
{
    if (t->waiting) {
        t->ahead = getc(t->f);
        t->waiting = 0;
    }
    return t;
}

static int text_eof(Text *t) { return ready(t)->ahead == EOF; }
static int text_eoln(Text *t) { return ready(t)->ahead == EOF || t->ahead == '\n'; }
static int text_window(Text *t) { return ready(t)->ahead == EOF ? 0 : t->ahead; }

static void text_get(Text *t)
{
    if (ready(t)->ahead != EOF)
        t->ahead = getc(t->f);
}

static int text_read_char(Text *t)
{
    int c = ready(t)->ahead;
    text_get(t);
    return c == EOF || c == '\n' ? ' ' : c;
}

static void text_readln(Text *t)
{
    while (ready(t)->ahead != EOF && t->ahead != '\n')
        text_get(t);
    text_get(t);
}

static void trap(const char *message);

/* Read a number as Pascal's read does: skip blanks and line ends, then
 * take the longest run of characters that can be part of one. It is an
 * error if there is none, as it is under pint (Free Pascal's runtime
 * error 106). */
static int can_follow(int c, int last, int real)
{
    if (isdigit(c))
        return 1;
    if (!real || c == EOF)
        return 0;
    if (c == '.' || c == 'e' || c == 'E')
        return 1;
    return (c == '+' || c == '-') && (last == 'e' || last == 'E');
}

static double text_read_number(Text *t, int real)
{
    char text[64];
    int n = 0, digits = 0;
    while (ready(t)->ahead == ' ' || t->ahead == '\t' || t->ahead == '\n')
        text_get(t);
    if (t->ahead == '+' || t->ahead == '-') {
        text[n++] = (char)t->ahead;
        text_get(t);
    }
    while (n < 60 && can_follow(t->ahead, n ? text[n - 1] : 0, real)) {
        digits += isdigit(t->ahead) != 0;
        text[n++] = (char)t->ahead;
        text_get(t);
    }
    text[n] = 0;
    char *end;
    double x = strtod(text, &end);
    if (digits == 0 || *end != 0)
        trap(" no number to read");
    if (!real && (x > INT32_MAX || x < INT32_MIN))
        trap(" number too large to read");
    return x;
}

/* ---------------------------------------------------------------- */
/* Stopping. pint's messages are kept, and its line of registers after
 * them; its dump of the whole store is not. pint goes on to end as if
 * the program had finished; this machine ends with status 1. */

static void registers(void)
{
    fprintf(output, " pc =%5d op =%3d  sp =%5d  mp =%5d  np =%5d\n",
            pc - 1, instr, sp, mp, np);
}

static void trap(const char *message)
{
    fflush(prr);
    fprintf(output, "\n%s\n", message);
    registers();
    fflush(output);
    exit(1);
}

/* ---------------------------------------------------------------- */
/* The store. Every address the program computes is checked before it
 * is used; pint checks none. */

static int32_t at(int32_t a)
{
    if (a < 0 || a > OVERM)
        trap(a == MAXSTR ? " nil pointer used" : " address outside the store");
    if (a == INPUT && input.waiting)    /* input^, looked at for the first time */
        store[INPUT].i = text_window(&input);
    return a;
}

static void set_word(int32_t a, Word w)
{
    a = at(a);
    store[a] = w;
    defined[a] = 1;
}

static Word get_word(int32_t a)
{
    a = at(a);
    if (undefined_traps && !defined[a])
        trap(" undefined value");
    return store[a];
}

static void copy_word(int32_t to, int32_t from)
{
    to = at(to);
    from = at(from);
    store[to] = store[from];
    defined[to] = defined[from];
}

static void forget(int32_t from, int32_t to)
{
    for (int32_t a = from; a <= to; a++)
        defined[at(a)] = 0;
}

static Word integer(int32_t i) { Word w; w.s = 0; w.i = i; return w; }
static Word real(double r) { Word w; w.r = r; return w; }
static Word set(uint64_t s) { Word w; w.s = s; return w; }

#define TOP store[sp]
#define NEXT store[sp - 1]

static void push(Word w)
{
    if (sp + 1 > MAXSTK)
        trap(" store overflow");
    set_word(++sp, w);
}

/* The frame l static links out from this one: the frame of the
 * procedure l levels out from this one, in the text. */
static long links;               /* static links followed, for -s */

static int32_t base(int l)
{
    int32_t a = mp;
    links += l;
    while (l-- > 0)
        a = store[at(a + 1)].i;
    return a;
}

/* Integer arithmetic wraps at 32 bits, as Free Pascal's does. */
static int32_t wrap(int64_t x) { return (int32_t)(uint32_t)(uint64_t)x; }

/* ---------------------------------------------------------------- */
/* Writing, in the forms Free Pascal gives write(x:w). */

static void write_spaces(FILE *f, int n)
{
    while (n-- > 0)
        putc(' ', f);
}

static void write_integer(FILE *f, int32_t i, int width)
{
    char text[16];
    int n = snprintf(text, sizeof text, "%d", i);
    write_spaces(f, width - n);
    fputs(text, f);
}

/* A real in floating-point form: a space or a minus, one digit, a
 * point, width-8 more digits (at least 1, at most 16), and an exponent
 * of three digits after a small e: write(1.5:12) is " 1.5000e+000".
 *
 * Free Pascal does not round as C's printf does: 2.25 to two figures is
 * 2.3, not 2.2. Its digits come from a method of its own. This is the
 * nearest rule found by comparing with it from outside: take the
 * seventeen figures that are correctly rounded, and round those half up
 * to as many as are wanted. Of 76000 numbers written by pint and by
 * this machine, 22 differ, each by one in the last figure. */
static void write_real(FILE *f, double r, int width)
{
    char text[64];
    if (isnan(r))
        snprintf(text, sizeof text, "Nan");
    else if (isinf(r))
        snprintf(text, sizeof text, r > 0 ? "+Inf" : "-Inf");
    else {
        int n = width - 8;          /* figures after the point */
        n = 1 + (n < 1 ? 1 : n > 16 ? 16 : n);
        char e[32], d[20];
        snprintf(e, sizeof e, "%.16e", fabs(r));
        d[0] = e[0];
        memcpy(d + 1, e + 2, 16);   /* the seventeen figures, no point */
        int exponent = atoi(strchr(e, 'e') + 1);
        if (n < 17 && d[n] >= '5') {
            int i = n - 1;
            while (i >= 0 && d[i] == '9')
                d[i--] = '0';
            if (i >= 0)
                d[i]++;
            else {                  /* 9.99 became 10.0 */
                d[0] = '1';
                exponent++;
            }
        }
        int t = snprintf(text, sizeof text, "%c%c.", signbit(r) ? '-' : ' ', d[0]);
        memcpy(text + t, d + 1, (size_t)(n - 1));
        snprintf(text + t + n - 1, sizeof text - (size_t)(t + n - 1), "e%c%03d",
                 exponent < 0 ? '-' : '+', abs(exponent));
    }
    write_spaces(f, width - (int)strlen(text));
    fputs(text, f);
}

/* ---------------------------------------------------------------- */
/* The standard procedures. The word on top of the stack is the address
 * of the file: 5 input, 6 output, 7 prd, 8 prr. Writing is allowed only
 * to output and prr, reading only from input and prd. */

static FILE *writing(const char *what)
{
    static char message[64];
    switch (TOP.i) {
    case OUTPUT: return output;
    case PRR: return prr;
    case INPUT: snprintf(message, sizeof message, " %s on input file", what); break;
    case PRD: snprintf(message, sizeof message, " %s on prd file", what); break;
    default: snprintf(message, sizeof message, " %s on no file", what); break;
    }
    trap(message);
    return NULL;
}

static Text *reading(const char *what)
{
    static char message[64];
    switch (TOP.i) {
    case INPUT: return &input;
    case PRD: return &prd;
    case OUTPUT: snprintf(message, sizeof message, " %s on output file", what); break;
    case PRR: snprintf(message, sizeof message, " %s on prr file", what); break;
    default: snprintf(message, sizeof message, " %s on no file", what); break;
    }
    trap(message);
    return NULL;
}

/* After a read, the file's word holds its window again. */
static void window(Text *t)
{
    set_word(t == &input ? INPUT : PRD, integer(text_window(t)));
}

static void standard(int which)
{
    FILE *f;
    Text *t;
    int32_t a;
    switch (which) {
    case GET:
        t = reading("get");
        text_get(t);
        window(t);
        sp--;
        break;
    case PUT:
        f = writing("put");
        putc(get_word(TOP.i).i, f);
        sp--;
        break;
    case RST:           /* release: the heap goes back to where it was */
        np = TOP.i;
        sp--;
        break;
    case SAV:           /* mark: remember where the heap is */
        set_word(TOP.i, integer(np));
        sp--;
        break;
    case RLN:
        /* pint reads a line of input, not of prd, for readln(prd): a
         * mistake the book points out, kept here. */
        reading("readln");
        text_readln(&input);
        window(&input);
        sp--;
        break;
    case NEW:           /* the length is on top, the pointer's address below */
        a = np - TOP.i;
        if (a <= ep)
            trap(" store overflow");
        forget(a, np - 1);
        np = a;
        set_word(NEXT.i, integer(np));
        sp -= 2;
        break;
    case WLN:
        putc('\n', writing("writeln"));
        sp--;
        break;
    case WRS: {         /* address, width, length, file */
        f = writing("write");
        int32_t s = store[sp - 3].i, width = store[sp - 2].i, n = NEXT.i;
        if (width > n)
            write_spaces(f, width - n);
        else
            n = width;
        for (int32_t i = 0; i < n; i++)
            putc(get_word(s + i).i, f);
        sp -= 4;
        break;
    }
    case ELN:
        t = reading("eoln");
        TOP = integer(text_eoln(t));
        break;
    case WRI:           /* value, width, file */
        f = writing("write");
        write_integer(f, store[sp - 2].i, NEXT.i);
        sp -= 3;
        break;
    case WRR:
        f = writing("write");
        write_real(f, store[sp - 2].r, NEXT.i);
        sp -= 3;
        break;
    case WRC:
        f = writing("write");
        write_spaces(f, NEXT.i - 1);
        putc(store[sp - 2].i, f);
        sp -= 3;
        break;
    case RDI: case RDR: case RDC:   /* the variable's address, file */
        t = reading("read");
        a = NEXT.i;
        if (which == RDC)
            set_word(a, integer(text_read_char(t)));
        else if (which == RDI)
            set_word(a, integer((int32_t)text_read_number(t, 0)));
        else
            set_word(a, real(text_read_number(t, 1)));
        window(t);
        sp -= 2;
        break;
    case SIN: TOP.r = sin(TOP.r); break;
    case COS: TOP.r = cos(TOP.r); break;
    case EXP: TOP.r = exp(TOP.r); break;
    case LOG: TOP.r = log(TOP.r); break;
    case SQT: TOP.r = sqrt(TOP.r); break;
    case ATN: TOP.r = atan(TOP.r); break;
    }
}

/* ---------------------------------------------------------------- */
/* Comparing. The comparisons carry a type, in p: 0 address, 1 integer,
 * 2 real, 3 boolean, 4 set, 6 character, and 5 for a block of q words,
 * such as a string, reached through two addresses. */

static int compare(int which, Word x, Word y)
{
    int lt, eq;
    switch (p) {
    case 0:             /* addresses: only equal or not */
        if (which != EQU && which != NEQ)
            trap(" <,<=,>,>= for address");
        lt = 0;
        eq = x.i == y.i;
        break;
    case 2:
        lt = x.r < y.r;
        eq = x.r == y.r;
        break;
    case 4:             /* sets: >= is a superset, <= a subset */
        if (which == GRT || which == LES)
            trap(" set inclusion");
        eq = x.s == y.s;
        if (which == GEQ) return (x.s & y.s) == y.s;
        if (which == LEQ) return (x.s & y.s) == x.s;
        lt = 0;
        break;
    case 5: {           /* blocks: by their first word that differs */
        int32_t i = 0;
        while (i < q && get_word(x.i + i).i == get_word(y.i + i).i)
            i++;
        eq = i == q;
        lt = !eq && get_word(x.i + i).i < get_word(y.i + i).i;
        break;
    }
    default:            /* integers, booleans, characters */
        lt = x.i < y.i;
        eq = x.i == y.i;
        break;
    }
    switch (which) {
    case EQU: return eq;
    case NEQ: return !eq;
    case GEQ: return !lt;
    case GRT: return !lt && !eq;
    case LEQ: return lt || eq;
    default: return lt;
    }
}

/* Calls. A frame begins with a mark of five words:
 *
 *   mp+0  a function's result
 *   mp+1  the static link: the frame of the routine
 *         this one is declared in
 *   mp+2  the dynamic link: the caller's frame
 *   mp+3  the caller's ep
 *   mp+4  where to return
 *
 * then the arguments, then the variables. mst makes the
 * mark before the arguments are pushed. Its p says where
 * the static link is, counted from the caller: 0 is the
 * caller's frame itself, 1 the frame the caller's static
 * link points to, and so on. cup p q, after p words of
 * arguments, enters the routine at q. Its ent 1 makes room
 * for the variables, and ent 2 for the most the stack will
 * need above them: checked once, so that no push in the
 * routine needs checking. */
static void frame(void)
{
    switch (instr) {
    case MST:
        if (sp + 5 > MAXSTK)
            trap(" store overflow");
        set_word(sp + 2, integer(base(p)));
        set_word(sp + 3, integer(mp));
        set_word(sp + 4, integer(ep));
        sp += 5;
        break;
    case CUP:
        mp = sp - (p + 4);
        set_word(mp + 4, integer(pc));
        pc = q;
        break;
    case ENT:
        if (p == 1) {
            int32_t old = sp;
            sp = mp + q;
            if (sp > np)
                trap(" store overflow");
            if (mp > 0)
                forget(old + 1, sp);  /* no values yet */
        } else {
            ep = sp + q;
            if (ep > np)
                trap(" store overflow");
        }
        break;
    case RET:   /* p is 0 for a procedure, which leaves nothing */
        sp = p == 0 ? mp - 1 : mp;
        pc = store[at(mp + 4)].i;
        ep = store[at(mp + 3)].i;
        mp = store[at(mp + 2)].i;
        break;
    }
}

/* ---------------------------------------------------------------- */
/* Running. */

/* The name of an instruction, with its type letter if it has one. */
static const char *name_of(int o)
{
    static char name[8];
    static const int bases[] = {LDO, STR, SRO, STO, IND, INC, CHK, DEC, LOD};
    if (o == LCI)
        return "lci";
    if (o < NINSTR) {
        /* the typed forms for integers have the letter i */
        static const int typed_forms[] = {LOD, LDO, STR, SRO, STO, IND, INC, CHK, DEC};
        for (size_t k = 0; k < sizeof typed_forms / sizeof typed_forms[0]; k++)
            if (o == typed_forms[k]) {
                snprintf(name, sizeof name, "%si", names[o]);
                return name;
            }
        return names[o];
    }
    if (o < LDOT || o >= LODT + 5)
        return "?";
    snprintf(name, sizeof name, "%s%c", names[bases[(o - LDOT) / 5]],
             "arsbc"[(o - LDOT) % 5]);
    return name;
}

static void trace(void)
{
    fprintf(stderr, "%5d %-4s %2d %6d   sp %5d mp %5d", pc - 1, name_of(instr),
            p, q, sp, mp);
    if (sp >= 0)
        fprintf(stderr, "   top %d", store[sp].i);
    fputc('\n', stderr);
}

static void run(void)
{
    pc = 0; sp = -1; mp = 0; np = MAXSTK + 1; ep = 5;
    defined[INPUT] = 1;     /* input^: see at() */
    set_word(PRD, integer(text_window(&prd)));
    for (;;) {
        if (pc < 0 || pc > PCMAX || op[pc] == NONE) {
            pc++;
            instr = NONE;
            trap(" jump to no instruction");
        }
        instr = op[pc]; p = pp[pc]; q = qq[pc];
        pc++;
        if (tracing)
            trace();
        if (counting)
            counts[instr]++;
        switch (instr) {
        case LOD: case LODT: case LODT + 1: case LODT + 2: case LODT + 3: case LODT + 4:
            push(get_word(base(p) + q));
            break;
        case LDO: case LDOT: case LDOT + 1: case LDOT + 2: case LDOT + 3: case LDOT + 4:
            push(get_word(q));
            break;
        case STR: case STRT: case STRT + 1: case STRT + 2: case STRT + 3: case STRT + 4:
            copy_word(base(p) + q, sp--);
            break;
        case SRO: case SROT: case SROT + 1: case SROT + 2: case SROT + 3: case SROT + 4:
            copy_word(q, sp--);
            break;
        case LDA:
            push(integer(base(p) + q));
            break;
        case LAO: case LCA:
            push(integer(q));
            break;
        case STO: case STOT: case STOT + 1: case STOT + 2: case STOT + 3: case STOT + 4:
            copy_word(NEXT.i, sp);
            sp -= 2;
            break;
        case LDC:       /* p: 1 integer, 6 character, 3 boolean, 0 nil */
            push(integer(p == 0 ? MAXSTR : q));
            break;
        case LCI:       /* a constant the loader put aside */
            push(store[q]);
            break;
        case IND: case INDT: case INDT + 1: case INDT + 2: case INDT + 3: case INDT + 4:
            TOP = get_word(TOP.i + q);
            break;
        case INC: case INCT: case INCT + 1: case INCT + 2: case INCT + 3: case INCT + 4:
            TOP.i = wrap((int64_t)TOP.i + q);
            break;
        case DEC: case DECT: case DECT + 1: case DECT + 2: case DECT + 3: case DECT + 4:
            TOP.i = wrap((int64_t)TOP.i - q);
            break;
        case MST: case CUP: case ENT: case RET:
            frame();
            break;
        case CSP:
            standard(q);
            break;
        case IXA: {
            int32_t i = TOP.i;
            sp--;
            TOP.i = wrap((int64_t)q * i + TOP.i);
            break;
        }
        case EQU: case NEQ: case GEQ: case GRT: case LEQ: case LES:
            sp--;
            TOP = integer(compare(instr, TOP, store[sp + 1]));
            break;
        case UJP:
            pc = q;
            break;
        case FJP:
            if (!TOP.i)
                pc = q;
            sp--;
            break;
        case XJP:       /* into a table of ujp and ujc */
            pc = TOP.i + q;
            sp--;
            break;
        case CHKA:      /* a pointer: q is 1 if nil is not allowed */
            if (TOP.i < np || TOP.i > MAXSTR - q)
                trap(" bad pointer value");
            break;
        case CHK: case CHKT + 1: case CHKT + 2: case CHKT + 3: case CHKT + 4:
            if (TOP.i < store[q - 1].i || TOP.i > store[q].i)
                trap(" value out of range");
            break;
        case EOF_:
            if (TOP.i != INPUT)
                trap(" code in error");
            TOP = integer(text_eof(&input));
            break;
        case ADI: sp--; TOP.i = wrap((int64_t)TOP.i + store[sp + 1].i); break;
        case SBI: sp--; TOP.i = wrap((int64_t)TOP.i - store[sp + 1].i); break;
        case MPI: sp--; TOP.i = wrap((int64_t)TOP.i * store[sp + 1].i); break;
        case DVI: case MOD: {
            sp--;
            int32_t x = TOP.i, y = store[sp + 1].i;
            if (y == 0)
                trap(" division by zero");
            if (y == -1)    /* -x, which wraps for the smallest integer */
                TOP.i = instr == DVI ? wrap(-(int64_t)x) : 0;
            else
                TOP.i = instr == DVI ? x / y : x % y;
            break;
        }
        case ADR: sp--; TOP.r += store[sp + 1].r; break;
        case SBR: sp--; TOP.r -= store[sp + 1].r; break;
        case MPR: sp--; TOP.r *= store[sp + 1].r; break;
        case DVR: sp--; TOP.r /= store[sp + 1].r; break;
        case SGS:
            if (TOP.i < 0 || TOP.i > SETMAX)
                trap(" set element out of range");
            TOP = set((uint64_t)1 << TOP.i);
            break;
        case FLT: TOP = real(TOP.i); break;
        case FLO: NEXT = real(NEXT.i); break;
        case TRC:
            if (!(TOP.r > -2147483649.0 && TOP.r < 2147483648.0))
                trap(" real too large for an integer");
            TOP = integer((int32_t)TOP.r);
            break;
        case NGI: TOP.i = wrap(-(int64_t)TOP.i); break;
        case NGR: TOP.r = -TOP.r; break;
        case SQI: TOP.i = wrap((int64_t)TOP.i * TOP.i); break;
        case SQR: TOP.r *= TOP.r; break;
        case ABI: TOP.i = wrap(TOP.i < 0 ? -(int64_t)TOP.i : TOP.i); break;
        case ABR: TOP.r = fabs(TOP.r); break;
        case NOT: TOP.i = !TOP.i; break;
        case AND: sp--; TOP.i = TOP.i && store[sp + 1].i; break;
        case IOR: sp--; TOP.i = TOP.i || store[sp + 1].i; break;
        case DIF: sp--; TOP.s &= ~store[sp + 1].s; break;
        case INT: sp--; TOP.s &= store[sp + 1].s; break;
        case UNI: sp--; TOP.s |= store[sp + 1].s; break;
        case INN: {     /* is the integer below in the set on top? */
            sp--;
            int32_t i = TOP.i;
            TOP = integer(i >= 0 && i <= SETMAX && (store[sp + 1].s >> i & 1));
            break;
        }
        case ODD: TOP.i = TOP.i & 1; break;
        case MOV: {     /* q words from the address on top to the one below */
            int32_t to = NEXT.i, from = TOP.i;
            sp -= 2;
            for (int32_t i = 0; i < q; i++)
                copy_word(to + i, from + i);
            break;
        }
        case STP:
            return;
        case UJC:
            trap(" case - error");
            break;
        default:
            trap(" code in error");
        }
    }
}

/* ---------------------------------------------------------------- */
/* Loading. The code is text, in two segments, each ended by a line q.
 * The first is the program, placed from address 3; the second, placed
 * at 0, calls it. A line starting with i is a comment; l n defines
 * label n here, and l n=v gives it the value v; a line starting with a
 * space is an instruction.
 *
 * A label may be used before it is defined. Until it is, the uses are
 * kept in a chain through their own q fields, as pint keeps them: the
 * label holds the last use, and each use the one before it. */

static struct { int32_t value; int defined; } labels[MAXLABEL + 1];
static int32_t icp = MAXSTK + 1, rcp = OVERI + 1, scp = OVERR + 1,
               bcp = OVERS + 2, mcp = OVERB + 1;
static int line_number;
static char *cursor;            /* where the line is being read */

static void load_error(const char *message)
{
    fprintf(output, "\n%s, line %d\n", message, line_number);
    exit(2);
}

static void blanks(void)
{
    while (*cursor == ' ' || *cursor == '\t')
        cursor++;
}

static long number(void)
{
    blanks();
    char *end;
    long n = strtol(cursor, &end, 10);
    if (end == cursor)
        load_error(" number expected");
    cursor = end;
    return n;
}

static int32_t label_use(void)
{
    blanks();
    if (*cursor++ != 'l')
        load_error(" label expected");
    long x = number();
    if (x < 0 || x > MAXLABEL)
        load_error(" label out of range");
    if (labels[x].defined)
        return labels[x].value;
    int32_t chain = labels[x].value;
    labels[x].value = pc;
    return chain;
}

static void label_define(long x, int32_t value)
{
    if (x < 0 || x > MAXLABEL)
        load_error(" label out of range");
    if (labels[x].defined)
        load_error(" duplicated label");
    for (int32_t use = labels[x].value; use != -1; ) {
        int32_t next = qq[use];
        qq[use] = value;
        use = next;
    }
    labels[x].defined = 1;
    labels[x].value = value;
}

/* Put a constant in its table, unless it is there already, and give its
 * address. The table is full when its pointer reaches its end. */
static int32_t constant(Word w, int32_t first, int32_t *free, int32_t over,
                        const char *full)
{
    store[*free] = w;
    defined[*free] = 1;
    int32_t a = first;
    while (store[a].s != w.s)
        a++;
    if (a == *free && ++*free == over)
        load_error(full);
    return a;
}

static int typed(int base, int typed_base, char letter)
{
    const char *letters = "arsbc";
    if (letter == 'i')
        return base;
    const char *x = letter ? strchr(letters, letter) : NULL;
    if (!x)
        load_error(" illegal type");
    return typed_base + (int)(x - letters);
}

static void assemble(char *line)
{
    char name[4] = {line[1], line[2], line[3], 0};
    char letter = line[4];
    cursor = line[4] ? line + 5 : line + 4;
    int o = 0;
    while (o < NINSTR && strcmp(names[o], name) != 0)
        o++;
    if (o == NINSTR || o == LCI)
        load_error(" illegal instruction");
    p = 0;
    q = 0;
    switch (o) {
    case EQU: case NEQ: case GEQ: case GRT: case LEQ: case LES: {
        const char *x = strchr("airbsmc", letter);
        if (!letter || !x)
            load_error(" illegal type");
        p = (int)(x - "airbsmc");
        if (letter == 'm')
            q = (int32_t)number();
        break;
    }
    case LOD: case STR:
        o = typed(o, o == LOD ? LODT : STRT, letter);
        p = (int)number();
        q = (int32_t)number();
        break;
    case LDA:
        p = (int)number();
        q = (int32_t)number();
        break;
    case CUP: case ENT:
        p = (int)number();
        q = label_use();
        break;
    case MST:
        p = (int)number();
        break;
    case RET: {
        const char *x = strchr("pircba", letter);
        if (!letter || !x)
            load_error(" illegal type");
        p = (int)(x - "pircba");
        break;
    }
    case LAO: case IXA: case MOV:
        q = (int32_t)number();
        break;
    case LDO: case SRO: case IND: case INC: case DEC: {
        static const int bases[] = {[LDO] = LDOT, [SRO] = SROT, [IND] = INDT,
                                    [INC] = INCT, [DEC] = DECT};
        o = typed(o, bases[o], letter);
        q = (int32_t)number();
        break;
    }
    case STO:
        o = typed(o, STOT, letter);
        break;
    case UJP: case FJP: case XJP:
        cursor = line + 4;
        q = label_use();
        break;
    case CSP: {
        blanks();
        int s = 0;
        while (s < NSP && strncmp(spnames[s], cursor, 3) != 0)
            s++;
        if (s == NSP)
            load_error(" illegal standard procedure");
        q = s;
        break;
    }
    case LDC:
        switch (letter) {
        case 'i': {
            long i = number();
            p = 1;
            if (labs(i) >= LARGEINT) {
                o = LCI;
                q = constant(integer((int32_t)i), MAXSTK + 1, &icp, OVERI,
                             " integer table overflow");
            } else
                q = (int32_t)i;
            break;
        }
        case 'r': {
            blanks();
            char *end;
            double r = strtod(cursor, &end);
            if (end == cursor)
                load_error(" real expected");
            o = LCI;
            p = 2;
            q = constant(real(r), OVERI + 1, &rcp, OVERR, " real table overflow");
            break;
        }
        case 'n':
            break;
        case 'b':
            p = 3;
            q = (int32_t)number();
            break;
        case 'c':
            p = 6;
            blanks();
            if (cursor[0] != '\'' || !cursor[1] || cursor[2] != '\'')
                load_error(" illegal character");
            q = (unsigned char)cursor[1];
            break;
        case '(': {
            uint64_t s = 0;
            for (;;) {
                blanks();
                if (*cursor == ')')
                    break;
                long e = number();
                if (e < 0 || e > SETMAX)
                    load_error(" set element out of range");
                s |= (uint64_t)1 << e;
            }
            o = LCI;
            p = 4;
            q = constant(set(s), OVERR + 1, &scp, OVERS, " set table overflow");
            break;
        }
        default:
            load_error(" illegal type");
        }
        break;
    case CHK: {
        o = typed(o, CHKT, letter);
        long lb = number(), ub = number();
        if (o == CHKA)
            q = (int32_t)lb;
        else {
            /* the bounds go in the table as a pair */
            store[bcp - 1] = integer((int32_t)lb);
            store[bcp] = integer((int32_t)ub);
            defined[bcp - 1] = defined[bcp] = 1;
            q = OVERS;
            do q += 2; while (store[q - 1].i != lb || store[q].i != ub);
            if (q == bcp) {
                bcp += 2;
                if (bcp == OVERB)
                    load_error(" boundary table overflow");
            }
        }
        break;
    }
    case LCA:           /* the string: 16 characters after the quote */
        if (mcp + STRLEN >= OVERM)
            load_error(" multiple table overflow");
        mcp += STRLEN;
        q = mcp;
        if (letter != '\'' || strlen(line + 5) < STRLEN)
            load_error(" illegal string");
        for (int i = 0; i < STRLEN; i++)
            set_word(q + i, integer((unsigned char)line[5 + i]));
        break;
    case ORD: case CHR:  /* they change only the type: no code */
        return;
    default:            /* the rest have no operands */
        break;
    }
    if (pc > PCMAX)
        load_error(" program too large");
    op[pc] = (unsigned char)o;
    pp[pc] = (unsigned char)p;
    qq[pc] = q;
    pc++;
}

/* One segment, to the line q. */
static void segment(FILE *f)
{
    static char line[1024];
    for (;;) {
        if (!fgets(line, sizeof line, f))
            load_error(" unexpected end of code");
        line_number++;
        line[strcspn(line, "\r\n")] = 0;
        switch (line[0]) {
        case 'i':
            break;
        case 'l': {
            cursor = line + 1;
            long x = number();
            blanks();
            int32_t value = pc;
            if (*cursor == '=') {
                cursor++;
                value = (int32_t)number();
            }
            label_define(x, value);
            break;
        }
        case 'q':
            return;
        case ' ':
            assemble(line);
            break;
        default:
            load_error(" illegal line");
        }
    }
}

static void load(FILE *f)
{
    memset(op, NONE, sizeof op);
    for (int i = 0; i <= MAXLABEL; i++)
        labels[i].value = -1;
    pc = BEGINCODE;
    segment(f);
    pc = 0;
    segment(f);
    for (int i = 0; i <= MAXLABEL; i++)
        if (!labels[i].defined && labels[i].value != -1) {
            char message[64];
            snprintf(message, sizeof message, " label %d used, never defined", i);
            load_error(message);
        }
}

/* ---------------------------------------------------------------- */

static int by_count(const void *a, const void *b)
{
    long x = counts[*(const int *)a], y = counts[*(const int *)b];
    return x < y ? 1 : x > y ? -1 : *(const int *)a - *(const int *)b;
}

static void print_counts(void)
{
    int order[256];
    long total = 0;
    for (int i = 0; i < 256; i++) {
        order[i] = i;
        total += counts[i];
    }
    qsort(order, 256, sizeof order[0], by_count);
    fprintf(stderr, "%12ld instructions\n%12ld static links followed\n", total, links);
    for (int k = 0; k < 256 && counts[order[k]]; k++) {
        int i = order[k];
        fprintf(stderr, "%12ld %5.1f%%  %s\n", counts[i], 100.0 * counts[i] / total,
                name_of(i));
    }
}

int main(int argc, char **argv)
{
    int a = 1;
    for (; a < argc && argv[a][0] == '-' && argv[a][1]; a++) {
        for (char *o = argv[a] + 1; *o; o++) {
            if (*o == 't') tracing = 1;
            else if (*o == 'u') undefined_traps = 1;
            else if (*o == 's') counting = 1;
            else a = argc;
        }
    }
    if (a >= argc || argc - a > 2) {
        fprintf(stderr, "usage: p4 [-t] [-u] [-s] program.p4 [prr]\n");
        return 2;
    }
    output = stdout;
    FILE *code = fopen(argv[a], "r");
    if (!code) {
        perror(argv[a]);
        return 2;
    }
    prr = stdout;
    if (a + 1 < argc && !(prr = fopen(argv[a + 1], "w"))) {
        perror(argv[a + 1]);
        return 2;
    }
    load(code);
    /* What is left of the code file is the program's prd, as under pint. */
    text_open(&prd, code);
    text_open(&input, stdin);
    run();
    if (counting)
        print_counts();
    fflush(prr);
    return 0;
}
