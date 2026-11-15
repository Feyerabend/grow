; Exercise 6.5: one of each mistake asm.py checks for
start:  PUSH 1
        JZ later
        JMP nowhere
        LOAD -1
        PUSH x
        ADD 3
        PUSH 99999999999
        FOO
        .word
start:  HALT
later:  CALL start
        JMP nowhere
