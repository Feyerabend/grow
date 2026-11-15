; Exercise 20.1: DUP, STORE k in a function is wrong. Each call of f keeps
; two values, so the stack fills; at the deepest call it is full when
; STORE 1 runs. STORE 1, LOAD 1 never goes above that; DUP, STORE 1 does,
; and traps one call sooner, before that call's PRINT.
main:
        PUSH 99
        PUSH 1
        CALL f 1
        HALT
f:      PUSH 5
        LOAD 0
        STORE 1
        LOAD 1
        PRINT
        LOAD 1
        CALL f 1
        RET
