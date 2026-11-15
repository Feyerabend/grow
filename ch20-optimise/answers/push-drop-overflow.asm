; The chapter's own rules have the same trouble, the other way round.
; Each call of f keeps two values more, so the stack fills; at the deepest
; call it is full when PUSH 0 runs, which traps. The optimiser removes
; PUSH 0, DROP, since in f's frame there is room; then PRINT runs and
; prints one number more, and the trap comes later.
main:
        PUSH 0
        CALL f 1
        HALT
f:      LOAD 0
        PUSH 1
        ADD
        STORE 0
        PUSH 7
        LOAD 0
        LOAD 0
        PUSH 0
        DROP
        PRINT
        CALL f 1
        RET
