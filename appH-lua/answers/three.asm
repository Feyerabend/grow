; Exercise H.1: the paper's three statements, in a function f(a, t, i)
; whose locals 0, 1 and 2 are a, t and i:
;     a = a + i;  a = a + 1;  a = t[i]
; each followed by PRINT of a, so that each must be done. Called with
; a = 10, t a block of three whose field 1 holds 42, and i = 1, it
; prints 11, 12 and 42.

main:   PUSH 10         ; a
        PUSH 3
        NEW             ; t
        DUP
        PUSH 1
        PUSH 42
        SETF            ; t[1] := 42
        PUSH 1          ; i
        CALL f 3
        DROP
        HALT

f:      LOAD 0          ; a = a + i
        LOAD 2
        ADD
        STORE 0
        LOAD 0
        PRINT
        LOAD 0          ; a = a + 1
        PUSH 1
        ADD
        STORE 0
        LOAD 0
        PRINT
        LOAD 1          ; a = t[i]
        LOAD 2
        GETF
        STORE 0
        LOAD 0
        PRINT
        PUSH 0
        RET
