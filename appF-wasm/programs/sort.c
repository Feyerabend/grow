/* Function pointers, which become call_indirect: a sort with the
 * comparison passed in, three ways. And 64-bit arithmetic, for the
 * numbers to sort. */
#include "io.h"

typedef int (*order)(long long, long long);

static int up(long long a, long long b) { return a < b; }
static int down(long long a, long long b) { return a > b; }
static int by_last_digit(long long a, long long b)
{
    long long x = a < 0 ? -a : a, y = b < 0 ? -b : b;
    return x % 10 < y % 10 || (x % 10 == y % 10 && a < b);
}

static void sort(long long *v, int n, order before)
{
    for (int i = 1; i < n; i++) {
        long long x = v[i];
        int j = i - 1;
        while (j >= 0 && before(x, v[j])) {
            v[j + 1] = v[j];
            j--;
        }
        v[j + 1] = x;
    }
}

int main(void)
{
    long long v[12];
    unsigned long long seed = 88172645463325252ULL;
    static order orders[] = {up, down, by_last_digit};
    for (int k = 0; k < 3; k++) {
        for (int i = 0; i < 12; i++) {
            seed ^= seed << 13;     /* Marsaglia's xorshift */
            seed ^= seed >> 7;
            seed ^= seed << 17;
            v[i] = (long long)(seed % 2000001) - 1000000;
        }
        sort(v, 12, orders[k]);
        for (int i = 0; i < 12; i++) {
            printi(v[i]);
            put(i < 11 ? ' ' : '\n');
        }
    }
    return 0;
}
