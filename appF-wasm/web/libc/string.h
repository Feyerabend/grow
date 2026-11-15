/* What wasm.c needs of string.h, for the page (host.c). */
#ifndef WEB_STRING_H
#define WEB_STRING_H
#include <stddef.h>
void *memcpy(void *to, const void *from, size_t n);
void *memmove(void *to, const void *from, size_t n);
void *memset(void *p, int c, size_t n);
int memcmp(const void *a, const void *b, size_t n);
size_t strlen(const char *s);
int strcmp(const char *a, const char *b);
#endif
