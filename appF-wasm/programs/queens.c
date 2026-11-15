/* Wirth's eight queens, and the other sizes up to ten: recursion over
 * arrays. */
#include "io.h"

static int row[16], free_row[16], up[32], down[32], solutions, n;

static void try(int column)
{
    for (int r = 0; r < n; r++)
        if (free_row[r] && up[r + column] && down[r - column + n]) {
            row[column] = r;
            free_row[r] = up[r + column] = down[r - column + n] = 0;
            if (column == n - 1)
                solutions++;
            else
                try(column + 1);
            free_row[r] = up[r + column] = down[r - column + n] = 1;
        }
}

int main(void)
{
    for (n = 4; n <= 10; n++) {
        for (int i = 0; i < 32; i++)
            free_row[i % 16] = up[i] = down[i] = 1;
        solutions = 0;
        try(0);
        printi(n);
        prints(" queens: ");
        printi(solutions);
        newline();
    }
    return 0;
}
