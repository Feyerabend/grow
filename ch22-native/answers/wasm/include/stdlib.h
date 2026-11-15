/* Exercise 22.4: the little of stdlib.h that runtime.h uses. */
#ifndef STDLIB_H
#define STDLIB_H
__attribute__((noreturn)) void exit(int status);
int atexit(void (*f)(void));
#endif
