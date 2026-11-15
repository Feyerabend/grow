# Appendix B: p-code, on Pascal-P4

The P4 machine of Pascal-P4 (Zurich, 1976), in C: `p4.c`. It runs the
P4 code that P4's own compiler, pcom, makes, and runs pcom itself. The
book's appendix B describes it; this is the machine to run.

    make check
    build/p4 pascal/queens.p4
    build/p4 p4/pcom.p4 hello.p4 < pascal/hello.pas
    build/p4 hello.p4
    build/p4 -s p4/pcom.p4 /dev/null < build/self.p

The third line is pcom, as P4 code, compiling a program on this
machine: the listing comes to the terminal, and the code goes to
`hello.p4`, the file the compiler calls prr. `-t` traces every
instruction; `-s` counts them, and the static links followed; `-u`
stops at a variable used before it has a value. The last line is pcom
compiling itself (`make check` makes `build/self.p`).

## What is here

- `p4.c`: the machine.
- `p4/pcom.p` and `p4/pint.p`: Pascal-P4's compiler and its assembler
  and interpreter, by Urs Ammann, Kesav Nori and Christian Jacobi (pcom)
  and Kathleen Jensen, Niklaus Wirth and Christian Jacobi (pint), as
  they are on Steven Pemberton's page
  (homepages.cwi.nl/~steven/pascal/), which calls them public domain;
  the files themselves carry no notice. They are kept as downloaded, on
  13 November 2026 (SHA-256 `5d3892ac…` and `09fe91c6…`).
- `p4/adapt.py`: the changes made to them before they are compiled, each
  explained there: for Free Pascal, for ASCII, and for pcom compiling
  itself.
- `p4/pcom.p4`: pcom compiled by itself, on pint. With it, this machine
  compiles Pascal without any other compiler.
- `pascal/`: 18 programs, each with the P4 code pcom makes of it and
  what pint prints when it runs; `traps/`, 4 programs that break a rule
  at run time; `errors/`, 5 that pcom refuses, with its listing. Thirteen
  of the programs, the traps, and four of the errors are copied from
  the public repository's appendix, with their comments in `(* *)`,
  since P4 knows no other, and `chars` fitted to P4's limits; `reals`,
  `sets`, `heap`, `text`, `strings` and `errors/limits` are new here,
  for what the others do not reach.
- `lastdigit.py`: compares outputs that may differ in the last figure of
  a real.

## What `make check` does

Without Free Pascal, with this machine alone:

1. pcom, as P4 code, compiles itself, and makes `p4/pcom.p4` again, to
   the character.
2. It compiles each program to the P4 code kept beside it, and that code
   prints what pint printed. They run with `-u`, so none of them uses a
   variable before it has a value.
3. Each trap stops with a message, kept beside it.
4. pcom refuses each program in `errors/` with the listing kept.

With Free Pascal (`fpc`, 3.2.2 here), also:

5. pcom and pint, compiled by Free Pascal, are the referees: pcom
   compiles itself and every program to the same code (but for the
   widths of the numbers in it), pint prints the same, and pint stops
   each trap that it catches with the same message and registers.
6. Each program, compiled by Free Pascal itself, prints the same.

`make expect` makes the kept code, listings and output again, from the
referees.

## Where this machine differs from pint

It keeps pint's opcodes, store, layout and limits, and prints its
messages, so that a trap shows the same line of registers. It differs
where pint leaves a thing to chance, or to Free Pascal:

- It stops at an address outside the store, a jump to no instruction, a
  label used and never defined, a division by zero (pint stops there
  only by Free Pascal's runtime error 200), a set element outside 0 to
  58, and, with `-u`, a variable used before it has a value.
- It does not dump the store after a message, and it ends with status 1
  where pint ends as if the program had finished.
- It reads the first character of input only when the program first
  looks at it, so that a program that reads nothing does not wait for a
  keyboard.
- At the end of the input, `input^` is 0. Under Free Pascal it holds a
  character left from before, which one depending on how the end was
  reached.
- Reals are written in Free Pascal's form, but Free Pascal's digits are
  not always correctly rounded, and this machine's are. Of 76000 numbers
  written by both, 22 differ, each by one in the last figure (see
  `write_real`).

## P4's limits

What P4 cannot compile, found while fitting the programs to it: a
`write` of a boolean, a string of more than 16 characters, an integer
constant above 32767, a range such as `[3..6]` in a set, `round`,
`write(x:w:d)`, and comments in braces. Its loader keeps at most three
large integers (above 26143) and three reals.

## Two findings

`p4/adapt.py` has the detail. pcom's `char` runs from 0 to 63, the
CDC 6000's six-bit characters, so in ASCII every capital letter fails
its range check. And Pemberton's pcom defines `mark` and `release` as
procedures that do nothing, for compilers that have neither; `-u`
finds pcom passing to `release` a variable that `mark` never set, and
without them pcom compiling itself needs about 22300 words of stack and
heap, where pint has 13650. With P4's own `mark` and `release` it fits.

## Beyond the suite

2500 programs made by changing the suite's programs at random, a few
characters each, were compiled by pcom on this machine and on pint. For
every one where pcom came to an end, the code and the listing were the
same. Where pcom did not, it does not under Free Pascal either: on some
programs cut short, it writes `*** eof encountered` without end. Of the 323 that compiled and were run, every difference
was one already listed: pint stopped by Free Pascal's runtime error 106
(a number to read and none there) or 200 (a division by zero) where
this machine stops with its own message, or the last figure of a real.

## Speed

pcom compiling itself is 13520025 P4 instructions. On a MacBook Air
(M1, 2020), on mains power, it takes this machine, compiled by Apple
clang 21 at `-O2`, 0.076 seconds; pint, compiled by Free Pascal 3.2.2,
0.213 seconds, or 0.108 at `-O3`. Each is the time of 20 runs divided
by 20, the best of two or three such sets; the sets of this machine and
of pint at Free Pascal's default were within 0.01 seconds of each
other, those at `-O3` 2.16 and 2.33 seconds.

`answers/` holds the worked answers to the appendix's exercises, which
`make check` runs too. Those that change a machine are patches, applied
to a copy; the mended pint is built only if Free Pascal is installed.
