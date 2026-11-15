; A generator: each RESUME gives the next value, and the value sent in
; comes back from YIELD. Locals of a frame survive; so do calls under it.
main:   CORO gen
        DUP
        COSTATE
        PRINT           ; 0
        DUP
        PUSH 10
        RESUME
        PRINT           ; 11
        DUP
        COSTATE
        PRINT           ; 1
        DUP
        PUSH 20
        RESUME
        PRINT           ; 12
        DUP
        PUSH 30
        RESUME
        PRINT           ; 40
        DUP
        COSTATE
        PRINT           ; 3
        DROP
        HALT
gen:    LOAD 0          ; local 0: the first value sent
        PRINT           ; 10
        PUSH 11
        CALL inner 1    ; yields from under a call
        PRINT           ; 20
        PUSH 12
        YIELD
        PRINT           ; 30
        PUSH 40
        RET
inner:  LOAD 0
        YIELD
        RET
