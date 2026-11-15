; Exercise 21.2: f calls itself until the stack is full. Each call prints
; its number, then pushes three values, then calls the next. Checked at
; every push, the deepest call prints, and traps as it fills its frame;
; checked at the CALL, for the most f's frame can hold, the trap is at the
; CALL, and that call's number is never printed.
main:   PUSH 1
        CALL f 1
        HALT
f:      LOAD 0
        PRINT
        PUSH 1
        PUSH 2
        PUSH 3
        LOAD 0
        PUSH 1
        ADD
        CALL f 1
        RET
