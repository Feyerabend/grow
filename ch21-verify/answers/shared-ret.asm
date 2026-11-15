; Exercise 21.5: code shared the other way: the main program jumps into f,
; which ends in RET. The verifier follows the main program to its end
; before it looks at any function, so this code is the main program's, and
; its RET is refused as a RET outside a function.
main:   PUSH 1
        CALL f 1
        PRINT
        PUSH 5
        JMP body
f:
body:   RET
