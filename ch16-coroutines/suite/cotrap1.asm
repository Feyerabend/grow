; RESUME a coroutine that has ended.
main:   CORO end
        DUP
        PUSH 0
        RESUME
        DROP
        PUSH 0
        RESUME
        HALT
end:    RET
