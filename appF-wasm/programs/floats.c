/* f32 beside f64, and the conversions between them and the integers:
 * Newton's square root in both widths, and a harmonic sum. */
#include "io.h"

static float sqrt32(float x)
{
    float r = x;
    for (int i = 0; i < 30; i++)
        r = (r + x / r) / 2;
    return r;
}

static double sqrt64(double x)
{
    double r = x;
    for (int i = 0; i < 60; i++)
        r = (r + x / r) / 2;
    return r;
}

int main(void)
{
    for (int i = 2; i <= 10; i += 4) {
        prints("sqrt ");
        printi(i);
        prints(": f32 ");
        printf64(sqrt32((float)i), 7);
        prints(", f64 ");
        printf64(sqrt64(i), 15);
        newline();
    }
    float h32 = 0;
    double h64 = 0;
    for (int k = 1; k <= 100000; k++) {
        h32 += 1.0f / (float)k;
        h64 += 1.0 / k;
    }
    prints("harmonic sum to 100000: f32 ");
    printf64(h32, 6);
    prints(", f64 ");
    printf64(h64, 12);
    newline();
    unsigned big = 4000000000u;
    prints("as float and back: ");
    printu((unsigned)(float)big);
    put(' ');
    printi((long long)(double)-9007199254740993LL);
    newline();
    return 0;
}
