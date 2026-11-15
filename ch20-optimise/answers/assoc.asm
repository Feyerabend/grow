; Exercise 20.4: x * 2 * 3, with x in a local so that it is not a constant,
; for x near the ends of the 32-bit numbers, where x * 2 wraps; and for a
; reference, where the first MUL traps.
main:   PUSH 1073741824     ; local 0: 2^30
        PUSH -1431655766    ; local 1
        PUSH 715827883      ; local 2
        PUSH 1
        NEW                 ; local 3: a reference
        LOAD 0
        PUSH 2
        MUL
        PUSH 3
        MUL
        PRINT
        LOAD 1
        PUSH 2
        MUL
        PUSH 3
        MUL
        PRINT
        LOAD 2
        PUSH 2
        MUL
        PUSH 3
        MUL
        PRINT
        LOAD 3
        PUSH 2
        MUL
        PUSH 3
        MUL
        PRINT
        HALT
