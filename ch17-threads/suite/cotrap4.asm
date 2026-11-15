; A coroutine cannot resume itself: it is running.
main:   PUSH 0
        CORO self
        STOREM
        PUSH 0
        PUSH 0
        LOADM
        PUSH 0
        RESUME
        HALT
self:   PUSH 0
        LOADM
        PUSH 0
        RESUME
        RET
