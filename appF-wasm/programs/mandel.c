/* f64: the Mandelbrot set, as characters. */
#include "io.h"

int main(void)
{
    const char *shades = " .:-=+*#%@";
    for (int y = -12; y <= 12; y++) {
        for (int x = -39; x <= 20; x++) {
            double cr = x / 20.0, ci = y / 10.0, zr = 0, zi = 0;
            int i = 0;
            while (i < 99 && zr * zr + zi * zi < 4) {
                double t = zr * zr - zi * zi + cr;
                zi = 2 * zr * zi + ci;
                zr = t;
                i++;
            }
            put(shades[i % 10]);
        }
        newline();
    }
    return 0;
}
