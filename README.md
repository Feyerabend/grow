# Growing a Machine: the code

*The companion code of* Growing a Machine, *by Set Lonnert.*

### What the book is about

A virtual machine, built from nothing, one chapter at a time. It begins
with a loop in C, under a hundred lines, that works a stack of numbers.
Each chapter after that is the whole machine again, the last chapter's
and one idea more, and the difference between the two is the lesson:
jumps, calls and frames, traps, programs in files, an assembler, a
tracer; a specification; compilers for two small languages; a heap, a
garbage collector, closures, coroutines and threads; and then the
machine made fast, verified, compiled to native code, run in a web
browser, and at last built as a circuit.

The question underneath is the one the preface asks: *how does it
actually work?* A virtual machine is not a black box but a sequence of
small, deliberate design choices, and the book makes each of them in
the open.

### Other roads to the same place

The book borrows from several well-known ways into this territory, and
differs from all of them, as its introduction says:

- **The textbooks of compilers**, from the Dragon Book of Aho, Sethi and
  Ullman (1986) on, study each stage of translation in depth, one stage
  at a time. They are thorough, but the stages are studied apart, and
  the machine that finally runs the code is somebody else's.
- **Books on virtual machines as such**, like Smith and Nair's *Virtual
  Machines* (2005), survey the whole field, from interpreters to
  hypervisors, and build none of it.
- **Nand2Tetris**, Nisan and Schocken's *The Elements of Computing
  Systems* (2005), is the nearest relative: it too builds one system in
  small steps, around a stack-based virtual machine. But it climbs up,
  from a logic gate to an operating system. This book begins with the
  software and climbs *down*, ending where Nand2Tetris begins, with the
  machine as a circuit.
- **Robert Nystrom's *Crafting Interpreters*** (2021) builds, in C, a
  bytecode machine with a stack, closures and a garbage collector, and
  shows its code as it grows. It follows one language from beginning to
  end; this book puts several languages, and several kinds of compiler,
  on one machine.
- **Further back**, Niklaus Wirth showed that a whole compiler and its
  machine can be small enough to read; Donald Knuth wrote *The Art of
  Computer Programming* for MIX, a computer that never existed; and
  *Structure and Interpretation of Computer Programs* (1985) ends by
  turning its interpreter into a register machine with a garbage
  collector.

### What this book does differently

Three habits:

1. **Every chapter is a whole machine.** Nothing is a fragment; each
   folder here runs on its own, and the difference from the folder
   before it is what the chapter teaches.
2. **The machine is written down.** From chapter 8 a specification says
   what it does, and one set of tests holds five quite different
   implementations to it: in C, in Python, as native code, in a web
   browser, and as a circuit.
3. **Everything is measured.** When a chapter makes the machine faster,
   it says by how much, on which computer and compiler, and also when
   the answer was disappointing.

The appendices then look at machines that are not ours, real ones, each
of which made some decision differently: Metcalfe's parsing machine of
1964, Pascal's p-code, CHIP-8, Wozniak's SWEET16, the Java Virtual
Machine, WebAssembly, Lark's CEK machine and Lua's register machine.

### Who it is for

The curious programmer, the systems enthusiast, and anyone who has
looked at a language runtime and wondered how it works. Its code is C
and Python; to run it, a C compiler, `make` and Python 3 are enough for
most of the book. It is best read with an editor open, a terminal ready,
and a willingness to break things to see how they break.

### The code

One folder for each chapter, each a working machine; the worked answers
to each chapter's exercises, in its `answers/`; and the machines of the
appendices that describe a machine of another kind. It holds only what
the book uses: no builds and no files made by running it. They are made
where they are needed, and `.gitignore` names them. `ISA.md` lists
the machine's instructions as far as chapter 15, codes 1 to 31, each
with the chapter where it first appears, and names the specifications
that settle them; `ch05-files/FORMAT.md` describes the format of its
files.

    make check

runs the tests of every chapter, the worked answers of every chapter,
and every appendix's machine and answers. Python 3 and a C compiler
are enough for most; chapter 23 also needs Clang with its `wasm32`
target and Node.js, and chapter 24 Icarus Verilog.
Appendix B runs its referees too if Free Pascal is installed; appendix
F, the specification's own tests if WABT is, and Node.js as referee if
it is. Appendix G needs Python 3.10 or later, and runs Lark's program
generator if Hypothesis is installed. Appendix H's answers need Lua 5.5,
and are passed over without it. The
answers of chapters 21 and 22 take about ten minutes each.

The folders keep the names they had while the book was written, which
do not always say the book's chapter number:

| Folder | Chapter |
|---|---|
| `ch01-stack` | 1, A stack machine |
| `ch02-jumps` | 2, Jumps |
| `ch03-calls` | 3, Calls and frames |
| `ch04-traps` | 4, Traps |
| `ch05-files` | 5, Programs in files |
| `ch06-asm` | 6, An assembler |
| `ch07-trace` | 7, Watching the machine run |
| `ch08-spec` | 8, A specification |
| `ch09-expr` | 9, A compiler for expressions |
| `ch10-enkel` | 10, enkel/0 |
| `ch11-basal` | 11, basal/0 |
| `ch12-parsing` | 12, Three ways to parse |
| `ch13-heap` | 13, A heap |
| `ch14-gc` | 14, Garbage collection |
| `ch15-closures` | 15, Closures |
| `ch16-coroutines` | 16, Coroutines |
| `ch17-threads` | 17, Threads |
| `ch18-dispatch` | 18, Dispatch |
| `ch19-registers` | 19, Registers |
| `ch20-optimise` | 20, Optimising |
| `ch21-verify` | 21, Verify once, then trust |
| `ch22-native` | 22, Native code |
| `ch23-wasm` | 23, The machine in a browser |
| `ch24-metal` | 24, The machine as hardware |
| `appA-metcalfe` | appendix A, The Metcalfe parsing machine |
| `appB-pcode` | appendix B, p-code, on Pascal-P4 |
| `appC-chip8` | appendix C, CHIP-8 |
| `appD-sweet16` | appendix D, SWEET16 |
| `appE-jvm` | appendix E, The Java Virtual Machine |
| `appF-wasm` | appendix F, WebAssembly 1.0 |
| `appG-lark` | appendix G, Lark's CEK machine |
| `appH-lua` | appendix H, Lua's virtual machine: the worked answers |

The code is free of every claim: see `UNLICENSE`.
