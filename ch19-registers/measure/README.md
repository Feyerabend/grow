# Measurements for the printed chapter

Run from the chapter's folder, after `make test` (which makes every
.vm and .rvm file):

    python3 measure/cost.py

It counts the instructions each program runs on the stack machine and
on the register machine (`-c`), times the three benchmarks, best of
seven runs, and gives each program's size: instructions, and words
without the address of origin each register instruction carries.

On the M1 (8 GB, macOS 27.2, Apple clang 21, `-O2`), 11 November 2026:

                 stack         naive      register   stack  naive  register
    fib     26,925,370    26,925,370    14,808,955   74 ms  76 ms     44 ms
    loop   260,000,007   260,000,007   100,000,005  550 ms 579 ms    244 ms
    sieve   33,826,936    33,826,406    17,152,655   76 ms  78 ms     53 ms

The samples run from 4% (basal-hurkle) to 48% (enkel-bits) fewer
instructions; register programs are 1.2 to 2.6 times as many words.
