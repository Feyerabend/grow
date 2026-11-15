; Exercise 20.1: a loop in the main program, with STORE k, LOAD k twice in
; every round, where -dup makes each into DUP, STORE k. 20 million rounds.
main:   PUSH 20000000   ; local 0: count
        PUSH 0          ; local 1: sum
loop:   LOAD 0
        PUSH 1
        SUB
        STORE 0
        LOAD 0
        JZ done
        LOAD 1
        LOAD 0
        XOR
        STORE 1
        LOAD 1
        PUSH 1
        AND
        JZ loop
        LOAD 1
        PUSH 3
        ADD
        STORE 1
        JMP loop
done:   LOAD 1
        PRINT
        HALT
