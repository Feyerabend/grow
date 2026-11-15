; Exercise 14.2: fragmentation. 15000 blocks of one field, three places each,
; every other one kept, in a holder block of 7500 fields. Then a block of
; 20000 fields is asked for. The live data is the same for every collector:
; the holder and 7500 small blocks, 30002 places. What differs is where the
; free space is: in mark and sweep, mostly in 7500 gaps of three places, none
; of which can be merged, so the big block does not fit; a collector that
; moves blocks puts all the free space in one place.
main:   PUSH 7500
        NEW                     ; local 0: the holder
        PUSH 0                  ; local 1: i
make:   LOAD 1
        PUSH 15000
        LT
        JZ made
        PUSH 1
        NEW
        LOAD 1
        PUSH 2
        MOD
        JZ keep
        DROP                    ; an odd one: let it go
        JMP next
keep:   LOAD 0
        SWAP
        LOAD 1
        PUSH 2
        DIV
        SWAP                    ; holder i/2 block
        SETF
next:   LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP make
made:   PUSH 20000
        NEW
        LEN
        PRINT                   ; 20000, if there was room
        HALT
