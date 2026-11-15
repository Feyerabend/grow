# Appendix F: WebAssembly 1.0

A WebAssembly machine in C, written from the specification: the
WebAssembly Core Specification, W3C Recommendation, 5 December 2019
(https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/). It decodes the
binary format, validates every function, instantiates the module, and
runs it.

    make check
    build/wasm programs/queens.wasm
    build/wasm -m programs/vm.wasm ../ch23-wasm/suite/arith.asm
    build/wasm -s build/suite/i32.json

The second line runs chapter 23's machine, the book's own, compiled to
WebAssembly, on this one. The last runs one file of the specification's
tests (`make check` makes `build/suite`, with WABT).

Copyright © 2019 W3C® (MIT, ERCIM, Keio, Beihang). This software
includes material derived from the WebAssembly Core Specification,
https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/, as the W3C's
document licence asks.

## What is here

- `wasm.c` and `wasm.h`: the machine, in four parts, as the
  specification has them: the binary format (its section 5), validation
  (3), instantiation (4.5) and execution (4.4). Validation follows the
  algorithm of the specification's appendix: a stack of the operands'
  types and a stack of control frames. It also records, for each
  `block`, `loop` and `if`, where its `else` and `end` are, so that a
  branch at run time needs no search.
- `spec.c`: runs the specification's tests, as WABT's `wast2json` turns
  them into binary modules and scripts of commands.
- `program.c`: runs a C program compiled to WebAssembly, and chapter
  23's machine as that chapter's `run.mjs` runs it.
- `suite/`: the specification's tests for the core, 73 `.wast` files, as
  they are in the specification's repository
  (github.com/WebAssembly/spec) at the tag `wg-1.0`, under the Apache
  License 2.0 (`suite/LICENSE`); downloaded 13 November 2026.
- `nan.py`: five of those files write two assertions about NaNs in 1.0's
  form, which WABT no longer reads; this writes them in today's.
- `programs/`: eight C programs, each for something different
  (recursion, memory, f64, f32, function pointers, a `switch`, bits,
  64-bit arithmetic), with each compiled by clang for WebAssembly 1.0
  (`-mcpu=mvp`) and what it prints; and `vm.wasm`, chapter 23's
  `core.c` compiled the same way.
- `run.mjs`: runs a program of `programs/` under Node.js, the referee.
- `web/`: a page, `web/index.html`, that opens straight from disk. It
  runs chapter 23's machine, `programs/vm.wasm`, on the five examples of
  that chapter's playground, two ways: on the browser's own WebAssembly
  engine, and on this machine, `wasm.c` compiled to WebAssembly 1.0 and
  running inside the same engine. It shows what each printed, how it
  ended and how long it took, and a module that both must refuse, with
  what each says. `web/host.c` is the host there, in place of `main.c`
  and `program.c`: it includes `wasm.c` as it stands, and the headers in
  `web/libc/` stand in for the C library. A jump back, `longjmp`, becomes
  a JavaScript exception, with the machine's message, and the page makes
  a new machine for every run. `web/data.js`, made by `web/data.py`,
  holds the two modules and the programs as base64.

## What `make check` does

With a C compiler and Python:

1. Each program prints what it should.
2. Chapter 23's machine passes the book's conformance suite, 71 tests,
   on this machine, with each of its collectors.

With WABT (`wast2json`, 1.0.42 here), also:

3. The specification's tests: 18840 of their 19270 commands pass, and
   none fails. The 430 left are modules written in the text format that
   must be refused, which test a reader of the text format, not this
   machine.

With Node.js (26 here), also:

4. Each program prints the same under Node; and the page's five
   programs print the same, and end the same, on Node's engine and on
   this machine compiled to WebAssembly inside it, and both refuse the
   broken module (`web/check.cjs`).

`make expect` compiles the programs and `vm.wasm` again, with clang, and
takes what they print from Node; and makes `web/data.js` again, which
also needs `wasm-ld`.

## What was found

- Chapter 23's own `web/vm.wasm` is refused here: clang 21, by default,
  uses `memory.copy` and `memory.fill`, from the proposal for bulk memory
  that came after 1.0. Compiled with `-mcpu=mvp`, it is 1.0 only.
- Breaking this machine on purpose, in seven ways, one at a time: six
  were caught by the specification's tests, by between 2 and 37 of
  them. The seventh, an `i32.add` wrong only when one operand is
  0x12345678, by none: the tests try chosen values.

## What it does not do

It is 1.0 and no more: no feature of a later proposal. It interprets
the bytes of each function as they are, decoding each instruction's
immediates every time it runs. It keeps the operands on one stack of
64-bit words, the types known from validation, not from the values.

## Speed

Chapter 23's conformance suite with the copying collector under stress,
where the collector runs at every step, is the heaviest thing here. On
a MacBook Air (M1, 2020), on mains power, one run of it takes 168
seconds of user time on this machine, compiled by Apple clang 21 at
`-O2`; under Node.js 26, which compiles WebAssembly to native code, 8.

`answers/` holds the worked answers to the appendix's exercises, which
`make check` runs too. Those that change the machine are patches,
applied to a copy.
