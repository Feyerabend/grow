# Appendix E: the Java Virtual Machine

A small Java Virtual Machine in C, written from *The Java Virtual
Machine Specification, Java SE 21 Edition*: chapter 4 for the class
file and its verification by type checking (4.10.1), chapter 6 for the
instructions. And a compiler from the book's own language, enkel/0, to
class files, which writes the stack maps the verifier checks. The
installed OpenJDK is the referee for both.

    make check
    build/jvm classes/Queens.class
    build/jvm -f classes/Sieve.class
    python3 enkelj.py ../ch10-enkel/samples/hanoi.p build
    build/jvm build/Hanoi.class
    java -cp build Hanoi

`-f` verifies a class and shows each stack map frame as the verifier
holds it; `-v` only verifies.

## What it does

- **Reads a class file** (`class.c`): the constant pool, fields,
  methods, the `Code` attribute with its `StackMapTable` and
  `LineNumberTable`, and `SourceFile`; with the checks of the format
  that come before verification (4.8). Class files of version 50.0 to
  65.0, Java SE 6 to 21.
- **Verifies every method before anything runs** (`verify.c`), by type
  checking, in one pass: the types at each place where paths meet are in
  the `StackMapTable`, written by the compiler, and the verifier checks
  each instruction against them. The rules are the specification's
  Prolog clauses, in C, for the part of the machine this one runs.
- **Runs one class** (`run.c`): static methods and static fields, `int`
  and `int[]`, `<clinit>` and `main`, and `System.out`'s `print`,
  `println` and `write` of an int, a char, a boolean or a string
  constant. The common instructions: constants, loads and stores, the
  arithmetic of int, the stack's own (`dup` and the rest, in their forms
  for single values), comparisons and branches, both switches,
  `iinc` and `wide`, static calls and returns, `newarray` of int,
  `iaload`, `iastore`, `arraylength`.
- **Traps as Java does**: division by zero, an index out of bounds, null,
  a negative length, and too deep a recursion are Java's exceptions,
  which end the program with Java's message and a trace of the calls,
  with the source's line numbers.

What it cannot check, it refuses, and says so: `long`, `float`,
`double`, objects (`new`, fields of instances), exception handlers, and
any assignment between two classes whose relation it would have to load
a class to know.

## The compiler

`enkelj.py` compiles enkel/0 (chapter 10, `../ch10-enkel/LANG.md`) to
a class file, with chapter 10's own scanner, parser and resolver, and a
new last stage: globals and `rval` as static int fields, arrays as
static `int[]` fields made in `<clinit>`, procedures as static methods,
`print` as `println(int)` and `emit` as `print(char)`. It writes the
bytecode, `max_stack`, `max_locals`, a `LineNumberTable` and the
`StackMapTable`. Every frame of an enkel/0 method is the same: a
statement leaves the stack empty, and every local is an int from the
start.

## What `make check` does

1. Eleven Java programs in `java/`, compiled by `javac --release 21` into
   `classes/` (kept, so that the check needs no Java), print on this
   machine what Java printed, in `tests/`: the output, the trace and the
   status. With Java, Java prints them again. A `NullPointerException`
   is compared without Java's helpful message
   (`-XX:-ShowCodeDetailsInExceptionMessages`).
2. Chapter 10's thirteen samples print the same on chapter 10's machine,
   on this one, and on Java; so do 300 of chapter 9's random
   expressions, and `tests/share.p`, which divides by zero.
3. `break.py` makes 23 class files, each broken in one way. Each is
   refused by this machine and by Java, but for two, where they are
   known to differ: a class file of version 49, which Java verifies by
   type inference and this machine refuses; and a method name the format
   forbids, which Java checks and this machine does not.
   `verifycmp.py` prints what each said, into `build/verify.txt`.
4. `mutate.py` changes random bytes in the classes' code and stack maps,
   1000 times. Whatever the verifier accepts runs on a build with
   AddressSanitizer and UBSan, and must not crash the machine.
5. The answers to the exercises, in `answers/`.

Without Java on the PATH, or with `make check JAVA=`, the real JVM is
left out, and everything else runs. `make expect` writes `tests/` again
from Java; `make classes` compiles `java/` again.

## Measured

`bench/time.py` times two enkel/0 programs and an empty one, compiled
once each way, on chapter 10's machine, on this one, and on Java with
and without its compiler to native code.

## What is here

- `jvm.h`, `class.c`, `verify.c`, `run.c`, `main.c`: the machine.
- `classfile.py`: reading and writing class files, for the scripts.
- `enkelj.py`: enkel/0 to class files.
- `java/`, `classes/`, `tests/`: the programs, javac's classes, what
  they print.
- `break.py`, `verifycmp.py`, `mutate.py`: the verifier put to the test.
- `bench/`: the programs measured, and `time.py`.
- `answers/`: the answers to the exercises.
