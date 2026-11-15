#!/usr/bin/env python3
"""
Make vm_more.c: chapter 7's vm.c with the additions of exercises 7.1 to 7.4.

  w addr      in the debugger, a watchpoint: c stops after the instruction
              at addr changes the top of the stack
  b name      in the debugger, a breakpoint at a label, from program.sym
  vm -p       run, and then print the ten addresses run most often
  vm -T       trace, with standard error buffered

    usage: python3 build.py > vm_more.c
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "..", "vm.c")).read()


def change(old, new, count=1):
    global s
    assert s.count(old) == count, old
    s = s.replace(old, new)


# 7.1 and 7.2: the debugger's new commands, and the symbols it reads.
change("static char breakpoint[65536];\n",
       """static char breakpoint[65536];
static char watch[65536];

/* Labels from program.sym, as the assembler can write them: "name address". */
#define MAX_SYMBOLS 1024
static char symbol_name[MAX_SYMBOLS][64];
static int symbol_at[MAX_SYMBOLS];
static int symbols = 0;

static void read_symbols(const char *program) {
    char path[1024], name[64];
    int at;
    FILE *f;
    size_t n = strlen(program);

    if (n < 3 || n + 2 > sizeof path || strcmp(program + n - 3, ".vm") != 0)
        return;
    memcpy(path, program, n - 3);
    strcpy(path + n - 3, ".sym");
    if ((f = fopen(path, "r")) == NULL)
        return;
    while (symbols < MAX_SYMBOLS && fscanf(f, "%63s %d", name, &at) == 2) {
        strcpy(symbol_name[symbols], name);
        symbol_at[symbols++] = at;
    }
    fclose(f);
}

/* An address written as a number or as a label; -1 if it is neither. */
static int address_of(const char *word) {
    char *end;
    long n = strtol(word, &end, 10);
    int i;

    if (*word != '\\0' && *end == '\\0')
        return (int) n;
    for (i = 0; i < symbols; i++)
        if (strcmp(symbol_name[i], word) == 0)
            return symbol_at[i];
    return -1;
}

/* The top of the stack, and whether there is one. */
static int top(int *value) {
    if (sp == 0)
        return 0;
    *value = stack[sp - 1];
    return 1;
}
""")
change("""    char line[256], cmd[16];
    int n, arg;
""", """    char line[256], cmd[16], word[64];
    int n, arg;
""")
change("""        n = sscanf(line, "%15s %d", cmd, &arg);
        if (n < 1)
            continue;
""", """        n = sscanf(line, "%15s %63s", cmd, word);
        if (n < 1)
            continue;
        if (n == 2) {
            arg = address_of(word);
            if (arg < 0 && (strcmp(cmd, "b") == 0 || strcmp(cmd, "d") == 0 || strcmp(cmd, "w") == 0)) {
                printf("no label %s\\n", word);
                continue;
            }
        }
""")
change("""        } else if (strcmp(cmd, "c") == 0) {
            if (step())
                while (!breakpoint[pc] && step())
                    ;
            where();""", """        } else if (strcmp(cmd, "c") == 0) {
            for (;;) {
                int at = pc, had, before = 0, has, after = 0;

                had = top(&before);
                if (!step())
                    break;
                has = top(&after);
                if (watch[at] && (had != has || before != after)) {
                    printf("watch %d: top of stack ", at);
                    if (had) printf("%d", before); else printf("(none)");
                    printf(" -> ");
                    if (has) printf("%d", after); else printf("(none)");
                    printf("\\n");
                    break;
                }
                if (breakpoint[pc])
                    break;
            }
            where();
        } else if (strcmp(cmd, "w") == 0 && n == 2) {
            if (arg < 0 || arg >= code_len)
                printf("no address %d in the program\\n", arg);
            else
                watch[arg] = 1;""")
change('printf("commands: s [n], c, b addr, d addr, p, l [n], q\\n");',
       'printf("commands: s [n], c, b addr, d addr, w addr, p, l [n], q\\n");')

# 7.3: the profiler.
change("static void run(void) {\n    while (step())\n        ;\n}",
       """static void run(void) {
    while (step())
        ;
}

static long executed[65536];

/* Run, counting each address, then print the ten run most often. */
static void profile(void) {
    int i, k, best[10], nbest = 0;

    do
        executed[pc >= 0 && pc < 65536 ? pc : 0]++;
    while (step());
    for (k = 0; k < 10; k++) {
        int found = -1;
        for (i = 0; i < code_len; i++) {
            int taken = 0, j;
            for (j = 0; j < nbest; j++)
                taken |= best[j] == i;
            if (!taken && executed[i] > 0 && (found < 0 || executed[i] > executed[found]))
                found = i;
        }
        if (found < 0)
            break;
        best[nbest++] = found;
        fprintf(stderr, "%10ld  %5d  ", executed[found], found);
        show_instruction(stderr, found);
        fprintf(stderr, "\\n");
    }
}""")

# 7.4: -T, the trace with stderr buffered; and -p; and the symbols for -d.
change("""    } else if (argc == 3 && strcmp(argv[1], "-d") == 0) {
        load(argv[2]);
        debug();""", """    } else if (argc == 3 && strcmp(argv[1], "-d") == 0) {
        load(argv[2]);
        read_symbols(argv[2]);
        debug();
    } else if (argc == 3 && strcmp(argv[1], "-T") == 0) {
        static char buffer[1 << 16];
        setvbuf(stderr, buffer, _IOFBF, sizeof buffer);
        load(argv[2]);
        trace();
    } else if (argc == 3 && strcmp(argv[1], "-p") == 0) {
        load(argv[2]);
        profile();""")
print(s, end="")
