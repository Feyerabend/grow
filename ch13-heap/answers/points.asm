; Exercise 13.2: points as blocks of two fields, x and y, and add(p, q),
; which returns their sum as a new point.
main:   PUSH 3
        PUSH 4
        CALL point 2    ; local 0: (3, 4)
        PUSH 10
        PUSH -1
        CALL point 2    ; local 1: (10, -1)
        LOAD 0
        LOAD 1
        CALL add 2      ; local 2: the sum
        LOAD 2
        PUSH 0
        GETF
        PRINT           ; 13
        LOAD 2
        PUSH 1
        GETF
        PRINT           ; 3
        LOAD 0
        PUSH 0
        GETF
        PRINT           ; 3: p is unchanged
        LOAD 2
        LOAD 0
        EQ
        PRINT           ; 0: the sum is a block of its own
        HALT

; point(x, y): a new block holding x and y
point:  PUSH 2
        NEW
        DUP
        PUSH 0
        LOAD 0
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; add(p, q): point(p.x + q.x, p.y + q.y)
add:    LOAD 0
        PUSH 0
        GETF
        LOAD 1
        PUSH 0
        GETF
        ADD
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        PUSH 1
        GETF
        ADD
        CALL point 2
        RET
