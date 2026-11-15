; Exercise 16.3: a round-robin scheduler. Three coroutines, workers 1, 2 and
; 3; worker k prints 10k + 1, ..., 10k + k, one number a turn, yielding after
; each, and then returns. The scheduler keeps them in a block, resumes each in
; turn, and drops one, setting its place to 0, as soon as it is dead.
main:   PUSH 3
        NEW                     ; local 0: the list of coroutines
        PUSH 0                  ; local 1: i
fill:   LOAD 1
        PUSH 3
        LT
        JZ filled
        LOAD 0
        LOAD 1
        CORO worker
        SETF                    ; list.i = a new worker
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP fill
filled: PUSH 3                  ; local 2: how many are alive
        PUSH 0
        STORE 1                 ; i = 0
turn:   LOAD 2
        JZ done
        LOAD 0
        LOAD 1
        GETF                    ; list.i
        DUP
        PUSH 0
        EQ
        JZ live
        DROP                    ; a place already emptied
        JMP step
live:   LOAD 1
        PUSH 1
        ADD                     ; its number, i + 1, which only its first turn reads
        RESUME
        DROP                    ; what it yielded, or returned
        LOAD 0
        LOAD 1
        GETF
        COSTATE
        PUSH 3
        EQ                      ; dead?
        JZ step
        LOAD 0
        LOAD 1
        PUSH 0
        SETF                    ; take it off the list
        LOAD 2
        PUSH 1
        SUB
        STORE 2
step:   LOAD 1
        PUSH 1
        ADD
        PUSH 3
        MOD
        STORE 1                 ; i = (i + 1) % 3
        JMP turn
done:   PUSH 0
        PRINT
        HALT

; worker: local 0 is its number k, the value its first turn was sent
worker: PUSH 1                  ; local 1: j
wloop:  LOAD 1
        LOAD 0
        PUSH 1
        ADD
        LT                      ; j < k + 1 ?
        JZ wdone
        LOAD 0
        PUSH 10
        MUL
        LOAD 1
        ADD
        PRINT                   ; 10k + j
        PUSH 0
        YIELD                   ; one turn is over
        DROP                    ; what the next turn sends
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP wloop
wdone:  PUSH 0
        RET                     ; the end of the worker: it is dead
