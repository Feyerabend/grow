/* What wasm.c needs of stdlib.h, for the page: memory, and an exit that
 * the page reports. The machine is made again for every run, so memory
 * is only ever taken, never given back (host.c). */
#ifndef WEB_STDLIB_H
#define WEB_STDLIB_H
#include <stddef.h>
void *malloc(size_t n);
void *calloc(size_t n, size_t size);
void *realloc(void *p, size_t n);
void free(void *p);
__attribute__((noreturn)) void exit(int status);
#endif
