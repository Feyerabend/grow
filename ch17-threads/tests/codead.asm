main:
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_1
        SETF
        CORO coroutine_start
        SWAP
        OVER
        SWAP
        RESUME
        DROP
        LOAD 0
        PUSH 1
        RESUME
        DUP
        PRINT
        DROP
        LOAD 0
        COSTATE
        PUSH 3
        EQ
        DUP
        PRINT
        DROP
        LOAD 0
        PUSH 2
        RESUME
        DUP
        PRINT
        SWAP
        DROP
        DROP
        HALT

; fun x -> ..., capturing: nothing
fun_1:
        LOAD 1
        PUSH 1
        ADD
        RET

; every coroutine starts here: local 0 is its function
coroutine_start:
        PUSH 0
        YIELD
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET
