; Exercise 13.3: what a block left unzeroed could hold. Block S holds 42;
; block X's field 0 refers to S; then both are let go. Under the stress
; option the collector runs before every NEW, so their places are free again,
; and the next two blocks, Z and Y, are made in them. If NEW did not zero
; its fields, Y's field 0 could still hold X's old reference, to S's place:
; a reference the program never gave Y, to whatever block is there now.
main:   PUSH 1
        NEW                     ; local 0: S
        LOAD 0
        PUSH 0
        PUSH 42
        SETF                    ; S.0 = 42
        PUSH 1
        NEW                     ; local 1: X
        LOAD 1
        PUSH 0
        LOAD 0
        SETF                    ; X.0 = S
        PUSH 0
        STORE 0                 ; let S go
        PUSH 0
        STORE 1                 ; and X
        PUSH 1
        NEW
        STORE 0                 ; local 0: Z
        LOAD 0
        PUSH 0
        PUSH 7
        SETF                    ; Z.0 = 7
        PUSH 1
        NEW
        STORE 1                 ; local 1: Y
        LOAD 1
        PUSH 0
        GETF                    ; Y.0: 0, or what was left there
        DUP
        LOAD 0
        EQ
        PRINT                   ; 1 if it is a reference to Z
        LOAD 1
        EQ
        PRINT                   ; 1 if it is a reference to Y
        HALT
