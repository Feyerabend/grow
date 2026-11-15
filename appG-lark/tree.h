#ifndef TREE_H
#define TREE_H

#include "cek.h"

/* Read a program's typed tree from a file emit.py wrote. A file that is
 * not one stops the reading, with a message and status 2. */
LkProg tree_read(const char *path);

#endif
