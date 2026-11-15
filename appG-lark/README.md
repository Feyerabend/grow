# Appendix G: Lark's CEK machine

The CEK machine of Lark, a small, purely functional language with
Hindley-Milner type inference and affine ownership, by Set Lonnert
(github.com/Feyerabend/stack, `lark/`, CC0), in C, made the book's own.
The machine is Felleisen and Friedman's, from "Control Operators, the
SECD-Machine, and the λ-Calculus" (1987): a state of a control, an
environment, and a continuation. It starts from Lark's `cek.c` of phase
9, and changes four things in it, each checked against Lark's own
machine.

    make check
    python3.13 emit.py lark/samples/04_queens.lark > queens.tree
    build/lark queens.tree
    LARK_STATS=1 build/lark queens.tree

## What changed, from Lark's machine

1. **A program is a file.** Lark compiled each program's typed tree
   into C data, and so into a binary of its own. Here Lark's front end
   writes the tree to a file (`emit.py`, its comment gives the format),
   and one machine reads and runs any program (`tree.c`).
2. **No nested run.** Lark's machine ran a function applied to one of
   several arguments to its end in a nested call of its own loop. Here
   its result goes to a frame that goes on with the other arguments, in
   the same loop, as the CEK machine does it.
3. **Numbers, not names.** Operators and built-in functions are numbers,
   given when the program is read, chosen by a switch; Lark's machine
   compared strings on every use. A variable is found by its depth in
   the environment, which `emit.py` works out from where the program
   binds its names; Lark's machine compared the name with each cell's.
   A top-level name is looked up once, and its slot kept.
4. **A garbage collector.** Lark's machine made everything in an arena
   that was never freed. Here a copying collector, after Cheney, keeps a
   heap of two spaces, starting at 1 MB, and collects between steps of
   the machine when half of one is used, growing the spaces if much
   survives. So a tail-recursive loop runs in a heap of constant size,
   as the CEK machine allows: Lark's test `04_tailrec`, a million tail
   calls, overflowed Lark's default arena of 512 KB, and here its heap
   never holds more than 524,360 bytes.

## What is here

- `lark/`: Lark's phase 9, copied from the author's repository on
  13 November 2026, as it is there: the front end, its CEK machine in
  Python (`src/cek.py`, the referee) and in C (`src/cek.c`, where this
  one began), its other backends, its tests and samples, and its
  generator of well-typed random programs (`tests/gen_prog.py`). Under
  CC0 (`lark/LICENSE`).
- `cek.c`, `cek.h`: the machine. `tree.c`, `tree.h`: reading a program.
  `main.c`: `lark program.tree`. `emit.py`: writing one.
- `fuzz.py`: random programs from Lark's generator, run on Lark's machine
  and on this one.
- `expected/`: what each of Lark's tests and samples prints on Lark's
  machine.
- `bench/`: three programs to measure (`fib`, `loop`, `sort`), and
  `answers.py`, which works out what they must print, in Python, apart
  from any Lark machine.

## What `make check` does

It needs a C compiler and Python 3.10 or later, which Lark's front end
needs.

1. Each of Lark's 25 numbered tests, its test of modules, its 16
   programs that must be refused, and its 9 samples prints what Lark's
   machine prints, with the same messages and status. They run on the
   machine built to check itself: at every variable, that the cell its
   depth reaches has the variable's name (`LARK_CHECK_DEPTH`); and a
   collection before every step (`LARK_COLLECT_ALWAYS`), so that a
   pointer the collector did not know of would be used at once after
   its object moved.
2. Each benchmark prints the answer `bench/answers.py` works out.
3. With Hypothesis (`make venv` makes `build/venv` with it and pytest):
   300 random well-typed programs print the same here and on Lark's
   machine.

## Checked further

- 3000 generated programs agree with the machine as it began, and 2000
  with it now; 1000 with depths checked; 500 with a collection before
  every step, under AddressSanitizer and UBSan, and all 50 programs the
  same way.
- A `+` broken on purpose was caught by the fuzzer within 300 programs.
- Lark's own test of its C machine passes in the copy, 41 of 41.

## Measured

On a MacBook Air (M1, 2020), on mains power, Apple clang 21 at `-O2`:
the user time of the fastest of five runs; and memory, as the most the
heap held, since the maximum resident set size macOS reports varied from
run to run by nearly a factor of two.

| | Lark's machine | changes 2 and 3 | and the collector |
|---|---|---|---|
| `fib` (fib 32) | 0.48 s, 430 MB | 0.35 s | 0.35 s, 0.5 MB |
| `loop` (10 million tail calls) | 0.94 s, 1220 MB | 0.63 s | 0.62 s, 0.5 MB |
| `sort` (100 merge sorts of 1000) | 0.70 s, 797 MB | 0.39 s | 0.40 s, 1.0 MB |

Lark's machine was given a 2 GB arena for this, and its memory is what
the arena held at the end, all of it kept. The middle column is this
machine with a heap of 2 GB, so that it never collects. The last
column's memory is the most the heap held between collections; it
collected 1078, 3054 and 1114 times.

The collector costs no time that shows here, but only because the test
between steps is marked as rarely true (`__builtin_expect`): without the
mark, `loop` took 0.77 seconds, though the collections themselves took
almost none of it.

`answers/` holds the worked answers to the appendix's exercises, which
`make check` runs too. Those that change the machine are patches,
applied to a copy; `answers/hint.sh` times, and is run by hand.
