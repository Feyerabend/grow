#!/usr/bin/env python3
"""
Make the interpreter with exercise 22.3's JIT, from the chapter's vm.c and
loop.h (chapter 21's interpreter) and jit.h, in a folder of its own:

    python3 build.py folder
    cc -std=gnu99 -O2 -DJIT [-DJIT_MORE] folder/vm.c -o vm-jit

Only verified programs are translated; the others run as before. -J prints
how many instructions were translated, in how many runs.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)


def patch(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def main():
    folder = sys.argv[1]
    loop = open(os.path.join(CHAPTER, "loop.h")).read()
    loop = patch(loop, "    static void **thread;\n", """    static void **thread;
#ifdef JIT_PATHS
    static void **plain;                /* the labels, without the JIT's */
#endif
""")
    loop = patch(loop, "    thread[code_len] = &&L_RUNOFF;\n", """    thread[code_len] = &&L_RUNOFF;
#ifdef JIT_PATHS
    plain = malloc((code_len + 1) * sizeof (void *));
    if (plain == NULL) {
        fprintf(stderr, "out of memory for threaded code\\n");
        exit(2);
    }
    memcpy(plain, thread, (code_len + 1) * sizeof (void *));
    for (a = 0; a < code_len; a++)
        if (native[a])
            thread[a] = &&L_NATIVE;
#endif
""")
    loop = patch(loop, '#include "ops.h"\n', '''#include "ops.h"
#ifdef JIT_PATHS
/*
 * Run the machine code from here; it returns where it stopped, and that
 * instruction is run as the interpreter runs it, by its own label.
 */
L_NATIVE:
    pc = native[start](stack, &sp, fp);
    start = pc;
    goto *plain[pc++];
#endif
''')
    open(os.path.join(folder, "loop.h"), "w").write(loop)
    for f in ["ops.h"]:
        shutil.copy(os.path.join(CHAPTER, f), folder)
    shutil.copy(os.path.join(HERE, "jit.h"), folder)

    c = open(os.path.join(CHAPTER, "vm.c")).read()
    c = patch(c, "#define RUN run_verified\n", """#ifdef JIT
#include "jit.h"
#define JIT_PATHS
#endif
#define RUN run_verified
""")
    c = patch(c, "    verified = !checked && verify();\n", """    verified = !checked && verify();
#ifdef JIT
    if (verified)
        jit();
    if (show_jit)
        fprintf(stderr, "jit: %d instructions in %d runs, %d words of machine code\\n",
                jit_instructions, jit_runs, jit_words);
#endif
    (void) show_jit;
""")
    c = patch(c, "    int i, strict = 0, verbose = 0, checked = 0, verified;\n",
              "    int i, strict = 0, verbose = 0, checked = 0, verified, show_jit = 0;\n")
    c = patch(c, """        } else if (strcmp(argv[i], "-C") == 0) {
            checked = 1;""", """        } else if (strcmp(argv[i], "-C") == 0) {
            checked = 1;
        } else if (strcmp(argv[i], "-J") == 0) {
            show_jit = 1;""")
    open(os.path.join(folder, "vm.c"), "w").write(c)


main()
