main:
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_1
        SETF
        LOAD 0
        DUP
        PRINT
        SWAP
        DROP
        DROP
        HALT

; fun x -> ..., capturing: nothing
fun_1:
        LOAD 1
        RET
