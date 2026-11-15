# Appendix D: SWEET16

Steve Wozniak's 16-bit machine of 1977, in one Python program,
`sweet16.py`, with an assembler for it. The book's appendix D describes
it, from Wozniak's article in BYTE; this is the machine to run.

    make check
    python3 sweet16.py -m 0900:090F samples/copy.s16
    python3 sweet16.py -t samples/copy.s16

When the program ends with `RTN`, the machine shows the registers, and
with `-m` the memory between two addresses, in hexadecimal. With `-t`, it
shows every instruction.

The samples:

- `copy.s16`: Wozniak's copying loop, as a subroutine called twice.
- `fib.s16`: Fibonacci numbers as 16-bit words, stopping when the carry
  says one has grown past 16 bits.

One difference from Wozniak's machine: this one keeps the prior result,
the register the last instruction changed, and the carry, apart, where
his kept both in the high byte of `R14`, the register's number times two
with the carry in its lowest bit. The branches test the same things.

`answers/` holds the worked answers to the appendix's exercises, which
`make check` runs too. The last runs on chapter 13's machine, in
`../ch13-heap`, and the second on a small 6502 simulator of its own.
