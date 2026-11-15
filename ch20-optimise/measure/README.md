# Measurements for the printed chapter

Run from the chapter's folder, after `make all benchmarks`:

    python3 measure/cost.py

It counts the instructions dispatched (`-c`) and times each benchmark,
best of seven runs, on threaded code without and with superinstructions,
each on the program as written and as optimised by `opt.py`. Then a
build made from a copy of `vm.c` (the switch build, with a counter at
the fetch) counts which instruction follows which, over the six
benchmarks and the sixteen samples: once over every pair run, and once
as the mean of each program's shares.

On the M1 (8 GB, macOS 27.2, Apple clang 21, `-O2`), 11 November 2026,
milliseconds:

                 plain  optimised  super  both
    fib             52         52     43    44
    loop           545        544    425   425
    sieve           55         55     39    38
    closures        72         72     69    68
    enkel-sieve    131        130     95    95
    basal-loop      33         29     28    23

The eight pairs of super.h are 34.8% of every pair run, and 24.3% of
the mean; JZ LOAD and JMP LOAD, at 6.0% and 5.4%, are not among them.
