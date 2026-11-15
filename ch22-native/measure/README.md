# Measurements for the printed chapter

Run from the chapter's folder, after `make benchmarks`, on mains power
(on battery, macOS runs this computer in a low-power mode, and every
time comes out about 1.6 times longer):

    python3 measure/cost.py

`cost.py` times each benchmark, best of seven: on chapter 21's
interpreter; compiled by `vm2c.py -C`, with every check; and compiled
as `make` builds it, without the checks verification made. On the M1
(8 GB, macOS 27.2, Apple clang 21, `-O2`), on mains power, 12 November
2026, milliseconds:

                 interpreted  checked  native
    fib                   51       17      14
    loop                 544       34      35
    sieve                 54       16      13
    closures              72       35      35
    enkel-sieve          132        9       7
    basal-loop            33       10       8

`closures` does not verify, since it calls through `CALLI`, so its
checked and native programs are the same. Every time includes starting
the program: an empty program, `HALT` alone, takes 2.3 ms, compiled or
interpreted.

GCC 16.2, from Homebrew, was measured the same way on 14 November
2026, in a copy of the chapter built and tested with it:

    make CC=gcc-16 benchmarks
    CC=gcc-16 python3 measure/cost.py

Its native code took from 1.7 to 4.3 times as long as Clang's
(`loop` 118 ms against 35); the interpreter it built, about as long
(`loop` 571 ms against 544).

## Done by hand

The machine code for `loop`:

    cc -O2 -w -I. -S bench/loop.c -o loop.s

The loop is the block that ends in `b.ne`: 22 instructions for the 13
of one round. Ten store into `stack[]`, three load from it, three do
the arithmetic, five are the checks that are left (three tests of a tag,
and the test for stack overflow, which is a compare and a branch), and
one goes round again. With `vm2c.py -C` the loop is 23 instructions,
with two tests for overflow in place of one.
`sp`, `fp` and `start` are not in it.

`trap()` without `__attribute__((noreturn))`: line 109 of `runtime.h`
taken out, the benchmarks compiled again with `-O2`, best of seven.
No time changed by more than a millisecond.

`gc: 0.004 seconds collecting` is from `./bench/closures -s`.
