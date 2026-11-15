/*
 * lark: run a Lark program, given as the typed tree emit.py writes.
 *
 *     python3 emit.py program.lark > program.tree
 *     lark program.tree
 */

#include "cek.h"
#include "tree.h"

#include <stdio.h>

int main(int argc, char **argv)
{
    if (argc != 2) {
        fputs("usage: lark program.tree\n", stderr);
        return 2;
    }
    LkProg program = tree_read(argv[1]);
    cek_run(&program);
    return 0;
}
