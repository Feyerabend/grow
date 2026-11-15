# Measurements for the printed chapter

Run from the chapter's folder, after `make vm benchmarks`, on mains
power (on battery, macOS runs this computer in a low-power mode, and
every time comes out about 1.6 times longer):

    python3 measure/cost.py
    python3 measure/mutants.py [seeds]

`cost.py` times each benchmark, best of seven, with every check (`-C`)
and verified. On the M1 (8 GB, macOS 27.2, Apple clang 21, `-O2`), on
mains power, 12 November 2026, milliseconds:

                 checked  verified
    fib               53        51
    loop             552       541
    sieve             55        55
    enkel-sieve      128       132
    basal-loop        33        33

`mutants.py` takes each of the verifier's sixteen refusals out in turn
and tries the broken verifier against tests/verdicts.txt, the
conformance suite, and the fuzzer (three seeds of 600 programs by
default; it takes about forty minutes). Four refusals are noticed by
none of the three: a jump into the middle of an instruction, code
shared by two functions, a function called with different numbers of
arguments, and more values than the stack has room for.

`args.asm` shows that the third is a real hole: with that refusal taken
out, it is verified, and its second call reads past its frame and
prints 20 where the checked run traps.
