main:
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_1
        SETF
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_2
        SETF
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_3
        SETF
        DUP
        PUSH 1
        OVER
        SETF
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_4
        SETF
        DUP
        PUSH 1
        LOAD 2
        SETF
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_5
        SETF
        DUP
        PUSH 1
        OVER
        SETF
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_6
        SETF
        DUP
        PUSH 1
        LOAD 3
        SETF
        DUP
        PUSH 2
        LOAD 4
        SETF
        LOAD 1
        LOAD 1
        LOAD 0
        PUSH 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        LOAD 0
        PUSH 3
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 4
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        LOAD 0
        PUSH 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        LOAD 0
        PUSH 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        LOAD 0
        PUSH 3
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 4
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        LOAD 0
        PUSH 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        LOAD 0
        PUSH 9
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        LOAD 0
        PUSH 3
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 4
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        LOAD 0
        PUSH 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 5
        LOAD 6
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 7
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        DROP
        LOAD 5
        LOAD 6
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 8
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        DROP
        LOAD 5
        LOAD 6
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 9
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        SWAP
        DROP
        SWAP
        DROP
        SWAP
        DROP
        SWAP
        DROP
        SWAP
        DROP
        SWAP
        DROP
        SWAP
        DROP
        SWAP
        DROP
        SWAP
        DROP
        SWAP
        DROP
        DROP
        HALT

; fun x -> ..., capturing: nothing
fun_1:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_7
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun a -> ..., capturing: nothing
fun_2:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_8
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun t -> ..., capturing: walk
fun_3:
        LOAD 1
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_9
        SETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_10
        SETF
        DUP
        PUSH 1
        LOAD 0
        PUSH 1
        GETF
        SETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun t -> ..., capturing: walk
fun_4:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_11
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        DUP
        PUSH 2
        LOAD 0
        PUSH 1
        GETF
        SETF
        CORO coroutine_start
        SWAP
        OVER
        SWAP
        RESUME
        DROP
        RET

; fun a -> ..., capturing: same
fun_5:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_12
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        DUP
        PUSH 2
        LOAD 0
        PUSH 1
        GETF
        SETF
        RET

; fun s -> ..., capturing: leaves same
fun_6:
        PUSH 4
        NEW
        DUP
        PUSH 0
        PUSH fun_13
        SETF
        DUP
        PUSH 1
        LOAD 0
        PUSH 1
        GETF
        SETF
        DUP
        PUSH 2
        LOAD 1
        SETF
        DUP
        PUSH 3
        LOAD 0
        PUSH 2
        GETF
        SETF
        RET

; fun l -> ..., capturing: x
fun_7:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_14
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        DUP
        PUSH 2
        LOAD 0
        PUSH 1
        GETF
        SETF
        RET

; fun b -> ..., capturing: a
fun_8:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_15
        SETF
        DUP
        PUSH 1
        LOAD 0
        PUSH 1
        GETF
        SETF
        DUP
        PUSH 2
        LOAD 1
        SETF
        RET

; fun x -> ..., capturing: nothing
fun_9:
        LOAD 1
        DUP
        PRINT
        DROP
        LOAD 1
        YIELD
        RET

; fun a -> ..., capturing: walk
fun_10:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_16
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        DUP
        PUSH 2
        LOAD 0
        PUSH 1
        GETF
        SETF
        RET

; fun ignored -> ..., capturing: t walk
fun_11:
        LOAD 0
        PUSH 2
        GETF
        LOAD 0
        PUSH 1
        GETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun b -> ..., capturing: a same
fun_12:
        LOAD 0
        PUSH 1
        GETF
        PUSH 0
        RESUME
        LOAD 1
        PUSH 0
        RESUME
        LOAD 0
        PUSH 1
        GETF
        COSTATE
        PUSH 3
        EQ
        JZ L17
        LOAD 1
        COSTATE
        PUSH 3
        EQ
        JMP L18
L17:
        LOAD 1
        COSTATE
        PUSH 3
        EQ
        JZ L19
        PUSH 0
        JMP L20
L19:
        LOAD 2
        LOAD 3
        EQ
        JZ L21
        LOAD 0
        PUSH 2
        GETF
        LOAD 0
        PUSH 1
        GETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        JMP L22
L21:
        PUSH 0
L22:
L20:
L18:
        SWAP
        DROP
        SWAP
        DROP
        RET

; fun t -> ..., capturing: leaves s same
fun_13:
        LOAD 0
        PUSH 3
        GETF
        LOAD 0
        PUSH 1
        GETF
        LOAD 0
        PUSH 2
        GETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun n -> ..., capturing: l x
fun_14:
        LOAD 0
        PUSH 1
        GETF
        LOAD 0
        PUSH 2
        GETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun l -> ..., capturing: a b
fun_15:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_23
        SETF
        DUP
        PUSH 1
        LOAD 0
        PUSH 1
        GETF
        SETF
        DUP
        PUSH 2
        LOAD 0
        PUSH 2
        GETF
        SETF
        RET

; fun b -> ..., capturing: a walk
fun_16:
        LOAD 0
        PUSH 2
        GETF
        LOAD 0
        PUSH 1
        GETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        DROP
        LOAD 0
        PUSH 2
        GETF
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun n -> ..., capturing: a b
fun_23:
        LOAD 1
        LOAD 0
        PUSH 1
        GETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 2
        GETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; every coroutine starts here: local 0 is its function
coroutine_start:
        PUSH 0
        YIELD
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET
