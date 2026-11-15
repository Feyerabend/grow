; Exercise 6.4: two instructions that can never be reached
        PUSH 1
        JMP over
        PUSH 2          ; after a JMP, with no label: dead
        PRINT
over:   PRINT
        HALT
        PUSH 3          ; after HALT: dead
