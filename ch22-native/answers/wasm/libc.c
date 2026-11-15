/*
 * Exercise 22.4: a C library just big enough for runtime.h and a program
 * compiled by vm2c.py, in WebAssembly. Output goes to the host one byte at
 * a time, by host_write(fd, c); exit() runs what atexit() was given and
 * then calls host_exit(status), which does not return. printf knows %d,
 * %ld, %lld, %s, %c, %% and, roughly, %.3f, which is all runtime.h asks of
 * it. run() is what the host calls: main, with no options.
 */

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define IMPORT(name) __attribute__((import_module("env"), import_name(#name)))
#define EXPORT(name) __attribute__((export_name(#name)))

IMPORT(host_write) void host_write(int fd, int c);
IMPORT(host_exit) __attribute__((noreturn)) void host_exit(int status);

static FILE files[3] = { { 0 }, { 1 }, { 2 } };
FILE *stdout = &files[1], *stderr = &files[2];

static void put(int fd, int c) { host_write(fd, c); }

static void put_s(int fd, const char *s) {
    while (*s)
        put(fd, *s++);
}

static void put_n(int fd, long long n) {
    char digits[24];
    int k = 0;
    unsigned long long u = n < 0 ? 0ull - (unsigned long long) n : (unsigned long long) n;
    if (n < 0)
        put(fd, '-');
    do {
        digits[k++] = (char) ('0' + u % 10);
        u /= 10;
    } while (u);
    while (k)
        put(fd, digits[--k]);
}

static int format(int fd, const char *f, va_list ap) {
    for (; *f; f++) {
        if (*f != '%') {
            put(fd, *f);
            continue;
        }
        f++;
        if (*f == 'd')
            put_n(fd, va_arg(ap, int));
        else if (f[0] == 'l' && f[1] == 'd')
            put_n(fd, va_arg(ap, long)), f++;
        else if (f[0] == 'l' && f[1] == 'l' && f[2] == 'd')
            put_n(fd, va_arg(ap, long long)), f += 2;
        else if (*f == 's')
            put_s(fd, va_arg(ap, const char *));
        else if (*f == 'c')
            put(fd, va_arg(ap, int));
        else if (f[0] == '.' && f[1] == '3' && f[2] == 'f') {
            double x = va_arg(ap, double);
            long long whole = (long long) x, thousandths = (long long) ((x - whole) * 1000);
            put_n(fd, whole);
            put(fd, '.');
            put(fd, (int) ('0' + thousandths / 100 % 10));
            put(fd, (int) ('0' + thousandths / 10 % 10));
            put(fd, (int) ('0' + thousandths % 10));
            f += 2;
        } else
            put(fd, *f);
    }
    return 0;
}

int printf(const char *f, ...) {
    va_list ap;
    va_start(ap, f);
    format(1, f, ap);
    va_end(ap);
    return 0;
}

int fprintf(FILE *file, const char *f, ...) {
    va_list ap;
    va_start(ap, f);
    format(file->fd, f, ap);
    va_end(ap);
    return 0;
}

int putchar(int c) {
    put(1, c);
    return c;
}

int fflush(FILE *f) {
    (void) f;
    return 0;
}

static void (*at_exit[8])(void);
static int n_at_exit = 0;

int atexit(void (*f)(void)) {
    if (n_at_exit == 8)
        return -1;
    at_exit[n_at_exit++] = f;
    return 0;
}

void exit(int status) {
    while (n_at_exit > 0)
        at_exit[--n_at_exit]();
    host_exit(status);
}

clock_t clock(void) { return 0; }

int strcmp(const char *a, const char *b) {
    while (*a && *a == *b)
        a++, b++;
    return (unsigned char) *a - (unsigned char) *b;
}

void *memcpy(void *to, const void *from, size_t n) {
    char *t = to;
    const char *f = from;
    while (n--)
        *t++ = *f++;
    return to;
}

void *memset(void *to, int c, size_t n) {
    char *t = to;
    while (n--)
        *t++ = (char) c;
    return to;
}

int main(int argc, char *argv[]);

EXPORT(run) void run_program(int copying, int stress) {
    char *argv[5] = { "program", 0, 0, 0, 0 };
    int argc = 1;
    if (copying) {
        argv[argc++] = "-g";
        argv[argc++] = "copy";
    }
    if (stress)
        argv[argc++] = "-S";
    exit(main(argc, argv));
}
