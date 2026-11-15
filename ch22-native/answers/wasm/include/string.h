/* Exercise 22.4: the little of string.h that runtime.h uses. */
#ifndef STRING_H
#define STRING_H
typedef unsigned long size_t;
int strcmp(const char *a, const char *b);
void *memcpy(void *to, const void *from, size_t n);
void *memset(void *to, int c, size_t n);
#endif
