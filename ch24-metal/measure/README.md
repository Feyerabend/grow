# Measurements for the printed chapter

Run from the chapter's folder, after `make test`, on mains power:

    python3 measure/cycles.py

`cycles.py` runs each program in `samples/` on the simulated CPU with
`vrun.py -c`, counts the instructions chapter 18's C machine executes
for the same program (a copy of `../ch18-dispatch/vm.c` with a counter
at the fetch), and times the simulation, best of three, start included.
On the M1 (8 GB, macOS 27.2, Icarus Verilog 13.0, Python 3.9.6), on
mains power, 12 November 2026:

                                cycles  instructions  seconds   cycles/s
    basal-countdown                454           453     0.05       8344
    basal-extremes                 670           669     0.06      11932
    basal-hurkle                  2783          2782     0.07      42267
    basal-table                   5949          5948     0.08      75193
    enkel-bits                     418           417     0.05       7626
    enkel-bubble-sort             2264          2263     0.06      35922
    enkel-gcd-negative-num         148           147     0.05       2799
    enkel-hanoi                    803           802     0.06      14282
    enkel-recursive-factorial      198           197     0.05       3764
    enkel-sieve                   9142          9141     0.09     101073
    fib                         218911        218910     1.12     196085

Every program takes one cycle per instruction and one more, the cycle
in which the CPU sees that it has stopped. Only `fib` runs long enough
for the rate to mean much: about 200,000 cycles a second.

## Done by hand

`arith.asm`, run with `vrun.py`: `-2147483648 / -1` gives
`-2147483648`, `-7 / 2` gives `-3`, `-7 % 2` gives `-1`, `7 % -2`
gives `1`, `2147483647 + 1` gives `-2147483648`, and
`-2147483648 % -1` gives `0`.

Yosys was not installed, so `cpu.v` was not synthesised; the 50 MHz in
the chapter is arithmetic.
