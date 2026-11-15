/* Exercise 22.4: the little of stdio.h that runtime.h uses, for WebAssembly. */
#ifndef STDIO_H
#define STDIO_H
typedef struct { int fd; } FILE;
extern FILE *stdout, *stderr;
int printf(const char *format, ...);
int fprintf(FILE *f, const char *format, ...);
int putchar(int c);
int fflush(FILE *f);
#endif
