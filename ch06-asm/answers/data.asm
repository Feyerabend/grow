; Exercise 6.3: a word of data in the middle of the code. The JMP goes round
; it, so the machine never runs it; but it is 1, the code of PUSH.
        JMP start
        .word 1
start:  PUSH 7
        PRINT
        HALT
