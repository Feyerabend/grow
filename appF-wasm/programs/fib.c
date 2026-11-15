/* Recursion: calls, and the frames they make. */
#include "io.h"

static int fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }

int main(void)
{
    for (int i = 0; i <= 30; i += 5) {
        prints("fib(");
        printi(i);
        prints(") = ");
        printi(fib(i));
        newline();
    }
    return 0;
}
