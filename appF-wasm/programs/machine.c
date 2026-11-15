/* A switch, which becomes br_table: a small stack machine, running a
 * program that counts down and sums. */
#include "io.h"

enum { PUSH, ADD, SUB, DUP, SWAP, JNZ, PRINT, OVER, DROP, HALT };

static const int program[] = {
    PUSH, 0, PUSH, 100,             /* sum, n */
    DUP, PRINT,                     /* 4: print n (a little of it) */
    SWAP, OVER, ADD, SWAP,          /* sum += n */
    PUSH, 1, SUB,                   /* n -= 1 */
    DUP, JNZ, 4,
    DROP, PRINT, HALT,
};

int main(void)
{
    int stack[64], sp = 0, pc = 0, printed = 0;
    for (;;) {
        switch (program[pc++]) {
        case PUSH: stack[sp++] = program[pc++]; break;
        case ADD: sp--; stack[sp - 1] += stack[sp]; break;
        case SUB: sp--; stack[sp - 1] -= stack[sp]; break;
        case DUP: stack[sp] = stack[sp - 1]; sp++; break;
        case SWAP: { int t = stack[sp - 1]; stack[sp - 1] = stack[sp - 2]; stack[sp - 2] = t; break; }
        case OVER: stack[sp] = stack[sp - 2]; sp++; break;
        case DROP: sp--; break;
        case JNZ: if (stack[--sp]) pc = program[pc]; else pc++; break;
        case PRINT:
            if (printed++ < 3 || stack[sp - 1] > 100) {
                printi(stack[sp - 1]);
                newline();
            }
            sp--;
            break;
        case HALT: return 0;
        default: return 1;
        }
    }
}
