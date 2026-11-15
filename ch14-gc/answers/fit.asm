; Exercise 14.1: where next fit pays. The allocator takes each block from the
; top of the first free chunk big enough, so the chunk it takes from stays
; first, and first fit usually finds room at once. To make it search, the
; small gaps must lie below the big chunk:
;
;   1. a big block of 20000 fields, which takes the top of the heap;
;   2. a holder of 7500 fields, and below it as many blocks of one field,
;      three places each, as fit, every other one kept in the holder;
;   3. the big block let go, and then 4000 blocks of two fields, four
;      places each, made and let go. The first needs a collection, which
;      frees the big block's space at the top, and the odd small blocks:
;      6338 gaps of three places, below it, too small for four.
;
; First fit then looks past every gap for every block; next fit starts at
; the chunk where it found room last.
main:   PUSH 20000
        NEW                     ; local 0: the big block
        PUSH 7500
        NEW                     ; local 1: the holder
        PUSH 0                  ; local 2: i
make:   LOAD 2
        PUSH 12677              ; as many as fit: 12677 * 3 = 38031 places
        LT
        JZ made
        PUSH 1
        NEW
        LOAD 2
        PUSH 2
        MOD
        JZ keep
        DROP
        JMP next
keep:   LOAD 1
        SWAP
        LOAD 2
        PUSH 2
        DIV
        SWAP
        SETF
next:   LOAD 2
        PUSH 1
        ADD
        STORE 2
        JMP make
made:   PUSH 0
        STORE 0                 ; let the big block go
        PUSH 0                  ; local 3: blocks of two fields made
more:   LOAD 3
        PUSH 4000
        LT
        JZ done
        PUSH 2
        NEW
        DROP
        LOAD 3
        PUSH 1
        ADD
        STORE 3
        JMP more
done:   LOAD 3
        PRINT                   ; 4000
        HALT
