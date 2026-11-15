; Exercise 17.4: the deadly embrace, and a scheduler that sees it. Thread 1
; takes lock A, then lock B; thread 2 takes B, then A. In turns of 5 both get
; their first lock before either asks for its second, and then each waits
; for ever for the other's.
;
; To see it, the scheduler must know two things that TAS does not record:
; who holds each lock, and which lock each thread is waiting for. So a
; thread that takes a lock writes its number beside it, and a thread that
; must wait yields the address of the lock it wants. The scheduler stops when
; every thread still running waits for a lock held by another that waits too.
;
; Memory:  1  lock A    11  who holds A, 0 if no one
;          2  lock B    12  who holds B
;          20, 21  what threads 1 and 2 wait for, 0 if nothing
main:   PUSH 5
        SLICE
        CORO one                ; local 0
        CORO two                ; local 1
loop:   LOAD 0
        PUSH 20
        CALL turn 2
        DROP
        LOAD 1
        PUSH 21
        CALL turn 2
        DROP
        LOAD 0
        COSTATE
        PUSH 3
        EQ
        LOAD 1
        COSTATE
        PUSH 3
        EQ
        MUL
        JZ check
        PUSH 0
        PRINT                   ; both ended: 0
        HALT
check:  CALL stuck 0
        JZ loop
        PUSH -1
        PRINT                   ; a deadly embrace: -1
        HALT

; turn(c, w): one turn for coroutine c, if it is not dead; what it yields is
; stored at w: the address of a lock it waits for, or 0
turn:   LOAD 0
        COSTATE
        PUSH 3
        EQ
        JZ go
        PUSH 0
        RET
go:     LOAD 1
        LOAD 0
        PUSH 0
        RESUME
        STOREM
        PUSH 0
        RET

; stuck(): 1 if thread 1 waits for a lock that thread 2 holds, and thread 2
; for one that thread 1 holds
stuck:  PUSH 20
        LOADM
        JZ no                   ; thread 1 waits for nothing
        PUSH 21
        LOADM
        JZ no
        PUSH 20
        LOADM
        PUSH 10
        ADD
        LOADM
        PUSH 2
        EQ                      ; what 1 wants is held by 2
        PUSH 21
        LOADM
        PUSH 10
        ADD
        LOADM
        PUSH 1
        EQ                      ; and what 2 wants is held by 1
        MUL
        RET
no:     PUSH 0
        RET

one:    PUSH 1
        PUSH 1
        CALL lock 2             ; A, as thread 1
        DROP
        PUSH 2
        PUSH 1
        CALL lock 2             ; then B
        DROP
        PUSH 2
        CALL unlock 1
        DROP
        PUSH 1
        CALL unlock 1
        DROP
        PUSH 0
        RET

two:    PUSH 2
        PUSH 2
        CALL lock 2             ; B, as thread 2
        DROP
        PUSH 1
        PUSH 2
        CALL lock 2             ; then A
        DROP
        PUSH 1
        CALL unlock 1
        DROP
        PUSH 2
        CALL unlock 1
        DROP
        PUSH 0
        RET

; lock(l, me): take lock l, then write me beside it; while it is taken,
; yield l, the lock waited for
lock:   LOAD 0
        TAS
        JZ got
        LOAD 0
        YIELD
        DROP
        JMP lock
got:    LOAD 0
        PUSH 10
        ADD
        LOAD 1
        STOREM                  ; who holds it
        PUSH 0
        RET

unlock: LOAD 0
        PUSH 10
        ADD
        PUSH 0
        STOREM
        LOAD 0
        PUSH 0
        STOREM
        PUSH 0
        RET
