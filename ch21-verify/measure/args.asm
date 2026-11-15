; f is called first with two values, then with one. The second call's
; frame has no local 1, but a verifier that checks only the first call
; lets LOAD 1 through.
main:   PUSH 10
        PUSH 20
        CALL f 2
        PRINT
        PUSH 30
        CALL f 1
        PRINT
        HALT
f:      LOAD 1
        RET
