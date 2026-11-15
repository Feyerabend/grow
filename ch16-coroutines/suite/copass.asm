; Two coroutines taking turns, each with a block of its own, which must
; live through collections while it waits.
main:   CORO worker
        CORO worker
        PUSH 0          ; local 2: the turn
turn:   LOAD 2
        PUSH 3
        LT
        JZ done
        LOAD 0
        LOAD 2
        RESUME
        PRINT
        LOAD 1
        LOAD 2
        PUSH 100
        ADD
        RESUME
        PRINT
        LOAD 2
        PUSH 1
        ADD
        STORE 2
        JMP turn
done:   HALT
worker: PUSH 1          ; local 1: its block, kept across YIELD
        NEW
next:   LOAD 1
        PUSH 0
        LOAD 0
        SETF            ; keep what was sent
        LOAD 1
        PUSH 0
        GETF
        YIELD           ; give it back; what is sent next comes up here
        STORE 0
        JMP next
