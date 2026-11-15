/*
 * wasm: run WebAssembly 1.0.
 *
 *     wasm -s script.json ...      run the specification's tests
 *     wasm program.wasm            run a program (see program.c)
 *
 * -v with -s prints every test that fails.
 */

#include "wasm.h"
#include "spec.h"

#include <stdio.h>
#include <string.h>

int run_program(int argc, char **argv);

int main(int argc, char **argv)
{
    if (argc >= 3 && strcmp(argv[1], "-s") == 0) {
        int verbose = 0, first = 2;
        if (strcmp(argv[2], "-v") == 0)
            verbose = 1, first = 3;
        Counts c = {0, 0, 0};
        for (int i = first; i < argc; i++)
            spec_run(argv[i], verbose, &c);
        printf("%ld passed, %ld failed, %ld skipped\n", c.passed, c.failed, c.skipped);
        return c.failed != 0;
    }
    if (argc >= 2)
        return run_program(argc - 1, argv + 1);
    fprintf(stderr, "usage: wasm -s [-v] script.json ...\n       wasm program.wasm\n");
    return 2;
}
