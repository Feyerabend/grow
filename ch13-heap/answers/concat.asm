; Exercise 13.1: concat(a, b), a new string holding a then b,
; and "hello, world" printed with it.
main:   PUSH 7
        NEW             ; local 0: "hello, "
        LOAD 0
        PUSH 0
        PUSH 104        ; h
        SETF
        LOAD 0
        PUSH 1
        PUSH 101        ; e
        SETF
        LOAD 0
        PUSH 2
        PUSH 108        ; l
        SETF
        LOAD 0
        PUSH 3
        PUSH 108        ; l
        SETF
        LOAD 0
        PUSH 4
        PUSH 111        ; o
        SETF
        LOAD 0
        PUSH 5
        PUSH 44         ; ,
        SETF
        LOAD 0
        PUSH 6
        PUSH 32         ; space
        SETF
        PUSH 5
        NEW             ; local 1: "world"
        LOAD 1
        PUSH 0
        PUSH 119        ; w
        SETF
        LOAD 1
        PUSH 1
        PUSH 111        ; o
        SETF
        LOAD 1
        PUSH 2
        PUSH 114        ; r
        SETF
        LOAD 1
        PUSH 3
        PUSH 108        ; l
        SETF
        LOAD 1
        PUSH 4
        PUSH 100        ; d
        SETF
        LOAD 0
        LOAD 1
        CALL concat 2   ; local 2: the two together
        DUP
        CALL print 1
        DROP
        LEN
        PRINT           ; 12
        HALT

; concat(a, b): a new block of len a + len b, a's characters, then b's
concat: LOAD 0
        LEN
        LOAD 1
        LEN
        ADD
        NEW             ; local 2: the new string
        LOAD 0
        LOAD 2
        PUSH 0
        CALL copy 3     ; a, to place 0
        DROP
        LOAD 1
        LOAD 2
        LOAD 0
        LEN
        CALL copy 3     ; b, to place len a
        DROP
        LOAD 2
        RET

; copy(from, to, at): every field of from into to, from place at on
copy:   PUSH 0          ; local 3: i
cloop:  LOAD 3
        LOAD 0
        LEN
        LT
        JZ cdone
        LOAD 1
        LOAD 2
        LOAD 3
        ADD             ; to, at + i
        LOAD 0
        LOAD 3
        GETF            ; from's field i
        SETF
        LOAD 3
        PUSH 1
        ADD
        STORE 3
        JMP cloop
cdone:  PUSH 0
        RET

; print(s): every character of s, then a newline
print:  PUSH 0
ploop:  LOAD 1
        LOAD 0
        LEN
        LT
        JZ pdone
        LOAD 0
        LOAD 1
        GETF
        EMIT
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP ploop
pdone:  PUSH 10
        EMIT
        PUSH 0
        RET
