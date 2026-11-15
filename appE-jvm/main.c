/*
 * jvm: load a class file, verify it, run it.
 *
 *     jvm Class.class        verify, then run main
 *     jvm -v Class.class     verify only, and say so
 *     jvm -f Class.class     verify, showing each stack map frame
 *
 * A class that cannot be loaded or verified is refused before any of it
 * runs, with status 1, as Java refuses it.
 */
#include <stdio.h>
#include <string.h>
#include "jvm.h"

int main(int argc, char **argv) {
    int verify_only = 0;
    if (argc == 3 && (!strcmp(argv[1], "-v") || !strcmp(argv[1], "-f"))) {
        verify_only = 1;
        verify_trace = argv[1][1] == 'f';
        argv++, argc--;
    }
    if (argc != 2) {
        fprintf(stderr, "usage: jvm [-v | -f] Class.class\n");
        return 2;
    }
    Class *c = load_class(argv[1]);
    if (!c || !verify_class(c)) {
        fprintf(stderr, "refused %s: %s\n", argv[1], jvm_error);
        return 1;
    }
    if (verify_only) {
        printf("verified %s\n", argv[1]);
        return 0;
    }
    return run_class(c);
}
