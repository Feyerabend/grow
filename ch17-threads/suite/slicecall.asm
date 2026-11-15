; Stopped under calls, with blocks, while collections move everything.
main:   PUSH 3
        SLICE
        CORO t
loop:   DUP
        COSTATE
        PUSH 3
        EQ
        JZ go
        HALT
go:     DUP
        PUSH 0
        RESUME
        DROP
        JMP loop
t:      PUSH 1
        CALL f 1
        PRINT
        PUSH 2
        CALL f 1
        PRINT
        PUSH 0
        RET
f:      PUSH 1
        NEW
        DUP
        PUSH 0
        LOAD 0
        SETF
        PUSH 0
        GETF
        PUSH 10
        ADD
        RET
