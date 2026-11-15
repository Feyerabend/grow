; The same, with a lock at memory 1: none is lost.
main:   PUSH 5
        SLICE
        CORO t
        CORO t
loop:   LOAD 0
        COSTATE
        PUSH 3
        EQ
        JZ a
other:  LOAD 1
        COSTATE
        PUSH 3
        EQ
        JZ b
        LOAD 0
        COSTATE
        PUSH 3
        EQ
        JZ a
        PUSH 0
        LOADM
        PRINT
        HALT
a:      LOAD 0
        PUSH 0
        RESUME
        DROP
        JMP other
b:      LOAD 1
        PUSH 0
        RESUME
        DROP
        JMP loop
t:      PUSH 20
next:   LOAD 1
        JZ done
lock:   PUSH 1
        TAS
        JZ got
        JMP lock
got:    PUSH 0
        LOADM
        PUSH 1
        ADD
        PUSH 0
        SWAP
        STOREM
        PUSH 1
        PUSH 0
        STOREM
        LOAD 1
        PUSH 1
        SUB
        STORE 1
        JMP next
done:   PUSH 0
        RET
