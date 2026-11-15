/*
 * Chapter 1: a stack machine.
 *
 * The whole machine is three things: an array of code, a program
 * counter pointing into it, and a stack of integers. Each step reads
 * one instruction at pc and does what it says. That is all.
 *
 * The program is written directly into the C source below. Changing
 * the program means recompiling the machine, which we fix in chapter 5.
 */

#include <stdio.h>

enum {
    HALT,       /* stop the machine                          */
    PUSH,       /* PUSH n: push the number n                 */
    ADD,        /* pop b, pop a, push a + b                  */
    SUB,        /* pop b, pop a, push a - b                  */
    MUL,        /* pop b, pop a, push a * b                  */
    PRINT,      /* pop a, print it on a line of its own      */
    RSUB        /* pop b, pop a, push b - a                  */
};

#define STACK_SIZE 256

static int stack[STACK_SIZE];
static int sp = 0;              /* number of values on the stack */

static int deepest = 0;

static void push(int v) {
    stack[sp++] = v;
    if (sp > deepest)
        deepest = sp;
}

static int pop(void) {
    return stack[--sp];
}

static void run(const int *code) {
    int pc = 0;

    for (;;) {
        int op = code[pc++];
        int a, b;

        switch (op) {
        case HALT:
            return;
        case PUSH:
            push(code[pc++]);
            break;
        case ADD:
            b = pop();
            a = pop();
            push(a + b);
            break;
        case SUB:
            b = pop();
            a = pop();
            push(a - b);
            break;
        case MUL:
            b = pop();
            a = pop();
            push(a * b);
            break;
        case PRINT:
            printf("%d\n", pop());
            break;
        case RSUB:
            b = pop();
            a = pop();
            push(b - a);
            break;
        }
    }
}

/* 1 - (2 - (3 - (4 - 5))), innermost first */
static const int program[] = {
    PUSH, 4, PUSH, 5, SUB,      /* 4 - 5             */
    PUSH, 3, RSUB,              /* 3 - (4 - 5)       */
    PUSH, 2, RSUB,              /* 2 - (3 - (4 - 5)) */
    PUSH, 1, RSUB,              /* 1 - (...)         */
    PRINT,
    HALT
};

int main(void) {
    run(program);
    printf("deepest: %d\n", deepest);
    return 0;
}
