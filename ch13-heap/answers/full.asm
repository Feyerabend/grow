; Exercise 13.5: fill the heap exactly. A block of 14 fields takes 16 places
; with its header of 2, so 65536 places hold 4096 of them, the last one
; exactly; then a block of 0 fields does not fit.
main:   PUSH 0                  ; local 0: how many made
loop:   LOAD 0
        PUSH 4096
        LT
        JZ full
        PUSH 14
        NEW
        DROP
        LOAD 0
        PUSH 1
        ADD
        STORE 0
        JMP loop
full:   LOAD 0
        PRINT                   ; 4096
        PUSH 0
        NEW                     ; out of memory
        HALT
