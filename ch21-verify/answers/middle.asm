; Exercise 21.5: a jump into the middle of an instruction. The verifier
; follows JZ's two ways in turn, the fall through first; there JMP 1 goes
; into the middle of PUSH 0. The other way, to bad, pops from an empty
; frame. Run, JZ is given 0 and goes to bad.
main:   PUSH 0
        JZ bad
        JMP 1
bad:    DROP
        PRINT
        HALT
