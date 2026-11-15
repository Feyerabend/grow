; LT on a reference, followed by JZ: the stack machine traps at the LT,
; with "not a number", and the fused JGE must say the same.
main:   PUSH 1
        NEW
        PUSH 2
        LT
        JZ there
        PUSH 1
        PRINT
there:  HALT
