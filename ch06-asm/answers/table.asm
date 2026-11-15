; Exercise 6.1: the multiplication table for 7, labels throughout.
; main keeps i as local 0, from 1 to 10.
main:   PUSH 1
loop:   LOAD 0
        PUSH 11
        LT
        JZ end
        LOAD 0
        PUSH 7
        MUL
        PRINT
        LOAD 0
        PUSH 1
        ADD
        STORE 0
        JMP loop
end:    HALT
