; Exercise D.5: the copy loop on chapter 13's machine, as a function
; copy(from, to, count): locals 0, 1 and 2. "HELLO, " is put at memory
; 100, copied to 200, and printed from there.

main:   PUSH 100
        PUSH 72         ; H
        STOREM
        PUSH 101
        PUSH 69         ; E
        STOREM
        PUSH 102
        PUSH 76         ; L
        STOREM
        PUSH 103
        PUSH 76         ; L
        STOREM
        PUSH 104
        PUSH 79         ; O
        STOREM
        PUSH 105
        PUSH 44         ; ,
        STOREM
        PUSH 106
        PUSH 32         ; space
        STOREM
        PUSH 100
        PUSH 200
        PUSH 7
        CALL copy 3
        DROP
        PUSH 200        ; print memory 200 to 206
        LOADM
        EMIT
        PUSH 201
        LOADM
        EMIT
        PUSH 202
        LOADM
        EMIT
        PUSH 203
        LOADM
        EMIT
        PUSH 204
        LOADM
        EMIT
        PUSH 205
        LOADM
        EMIT
        PUSH 206
        LOADM
        EMIT
        PUSH 10
        EMIT
        HALT

copy:   LOAD 1          ; to, for STOREM
        LOAD 0
        LOADM           ; the value at from
        STOREM          ; to it
        LOAD 0          ; from + 1
        PUSH 1
        ADD
        STORE 0
        LOAD 1          ; to + 1
        PUSH 1
        ADD
        STORE 1
        LOAD 2          ; count - 1, kept, and tested
        PUSH 1
        SUB
        DUP
        STORE 2
        JZ done
        JMP copy
done:   PUSH 0
        RET
