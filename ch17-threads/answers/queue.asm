; Exercise 17.3: a semaphore made with TAS, and a queue of values between two
; threads. A producer puts 1 to 10 into a queue of four places; a consumer
; takes them out and prints them. Turns are of three instructions, so the two
; are stopped anywhere, in the middle of anything.
;
; Memory:  0  the lock, taken with TAS
;          1  the semaphore "items": how many values are in the queue
;          2  the semaphore "spaces": how many places are free, at first 4
;          3  head, where the next value is taken from
;          4  tail, where the next value is put
;          10 to 13  the queue
main:   PUSH 2
        PUSH 4
        STOREM                  ; spaces = 4
        PUSH 3
        SLICE
        CORO producer
        CORO consumer
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

; producer: local 1 is i, from 1 to 10
producer:
        PUSH 1
ploop:  LOAD 1
        PUSH 11
        LT
        JZ pdone
        PUSH 2
        CALL wait 1             ; a free place
        DROP
        CALL lock 0
        DROP
        PUSH 4
        LOADM
        PUSH 10
        ADD
        LOAD 1
        STOREM                  ; queue[tail] = i
        PUSH 4
        PUSH 4
        LOADM
        PUSH 1
        ADD
        PUSH 4
        MOD
        STOREM                  ; tail = (tail + 1) % 4
        CALL unlock 0
        DROP
        PUSH 1
        CALL signal 1           ; one more value
        DROP
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP ploop
pdone:  PUSH 0
        RET

; consumer: local 1 counts the values taken
consumer:
        PUSH 0
cloop:  LOAD 1
        PUSH 10
        LT
        JZ cdone
        PUSH 1
        CALL wait 1             ; a value
        DROP
        CALL lock 0
        DROP
        PUSH 3
        LOADM
        PUSH 10
        ADD
        LOADM                   ; queue[head]
        PUSH 3
        PUSH 3
        LOADM
        PUSH 1
        ADD
        PUSH 4
        MOD
        STOREM                  ; head = (head + 1) % 4
        CALL unlock 0
        DROP
        PUSH 2
        CALL signal 1           ; one more free place
        DROP
        PRINT
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP cloop
cdone:  PUSH 0
        RET

; lock: TAS until it was 0, giving up the turn each time it was not
lock:   PUSH 0
        TAS
        JZ locked
        PUSH 0
        YIELD
        DROP
        JMP lock
locked: PUSH 0
        RET

unlock: PUSH 0
        PUSH 0
        STOREM
        PUSH 0
        RET

; wait(s): when the count at address s is above 0, take one from it;
; until then, give up the turn and try again
wait:   CALL lock 0
        DROP
        PUSH 0
        LOAD 0
        LOADM
        LT                      ; 0 < count ?
        JZ none
        LOAD 0
        LOAD 0
        LOADM
        PUSH 1
        SUB
        STOREM
        CALL unlock 0
        DROP
        PUSH 0
        RET
none:   CALL unlock 0
        DROP
        PUSH 0
        YIELD
        DROP
        JMP wait

; signal(s): add one to the count at address s
signal: CALL lock 0
        DROP
        LOAD 0
        LOAD 0
        LOADM
        PUSH 1
        ADD
        STOREM
        CALL unlock 0
        DROP
        PUSH 0
        RET
