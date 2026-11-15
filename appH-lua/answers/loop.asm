; Exercise H.3: the while loop of while.lua, i from 0 to a million,
; with i in local 0 of a function.

main:   PUSH 0
        CALL count 1
        PRINT
        HALT

count:  LOAD 0          ; while i < 1000000
        PUSH 1000000
        LT
        JZ done
        LOAD 0          ; i = i + 1
        PUSH 1
        ADD
        STORE 0
        JMP count
done:   LOAD 0
        RET
