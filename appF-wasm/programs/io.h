/* What the programs here have instead of a C library: one function the
 * host gives, to write a byte, and a few ways to print with it. They are
 * compiled with no library at all, so memset and memcpy, which clang may
 * call for loops that fill or copy, are here too. */

#ifndef IO_H
#define IO_H

__attribute__((import_module("env"), import_name("putchar")))
void put(int c);

typedef unsigned long size_t;

static __attribute__((unused)) void prints(const char *s) { while (*s) put(*s++); }

static __attribute__((unused)) void printu(unsigned long long x)
{
    char b[24];
    int n = 0;
    do b[n++] = (char)('0' + x % 10); while (x /= 10);
    while (n) put(b[--n]);
}

static __attribute__((unused)) void printi(long long x)
{
    if (x < 0) {
        put('-');
        printu(0ULL - (unsigned long long)x);
    } else
        printu((unsigned long long)x);
}

/* A double with d figures after the point, rounded half away from 0. */
static __attribute__((unused)) void printf64(double x, int d)
{
    if (x != x) { prints("nan"); return; }
    if (x < 0) { put('-'); x = -x; }
    double scale = 1;
    for (int i = 0; i < d; i++) scale *= 10;
    unsigned long long n = (unsigned long long)(x * scale + 0.5);
    unsigned long long whole = n / (unsigned long long)scale;
    unsigned long long part = n % (unsigned long long)scale;
    printu(whole);
    if (d) {
        put('.');
        char b[24];
        for (int i = d - 1; i >= 0; i--, part /= 10) b[i] = (char)('0' + part % 10);
        for (int i = 0; i < d; i++) put(b[i]);
    }
}

static __attribute__((unused)) void newline(void) { put('\n'); }

void *memset(void *p, int c, size_t n)
{
    unsigned char *q = p;
    while (n--) *q++ = (unsigned char)c;
    return p;
}

void *memcpy(void *to, const void *from, size_t n)
{
    unsigned char *t = to;
    const unsigned char *f = from;
    while (n--) *t++ = *f++;
    return to;
}

#endif
