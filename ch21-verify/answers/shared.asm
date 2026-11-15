; Exercise 21.5: code shared by two functions. f jumps into the main
; program's code, with as many values in its frame as the main program has
; there; that code prints and halts, inside f's frame.
main:   PUSH 1
        CALL f 1
end:    PRINT
        HALT
f:      JMP end
