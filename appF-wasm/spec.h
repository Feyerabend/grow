#ifndef SPEC_H
#define SPEC_H

typedef struct { long passed, failed, skipped; } Counts;

/* Run one script of wast2json's, adding to the counts. */
int spec_run(const char *script, int verbose, Counts *counts);

#endif
