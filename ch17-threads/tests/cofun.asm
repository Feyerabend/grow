main:
        PUSH 5
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
        SWAP
        DROP
        DROP
        HALT

; every coroutine starts here: local 0 is its function
coroutine_start:
        PUSH 0
        YIELD
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET
