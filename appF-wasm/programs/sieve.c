/* Memory: the sieve of Eratosthenes, in bytes, below 100000. */
#include "io.h"

#define N 100000
static unsigned char composite[N];

int main(void)
{
    int count = 0, last = 0;
    for (int i = 2; i < N; i++) {
        if (composite[i])
            continue;
        count++;
        last = i;
        for (int j = 2 * i; j < N; j += i)
            composite[j] = 1;
    }
    prints("primes below 100000: ");
    printi(count);
    prints(", the last ");
    printi(last);
    newline();
    return 0;
}
