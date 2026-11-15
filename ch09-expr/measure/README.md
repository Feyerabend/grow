# A compiler for expressions, measured

`expr.py`, `fuzz.py`, `asm.py`, `isa.py`, `vmfile.py`, `vm.c`, `Makefile`, `samples/` and
`tests/` are from `ch09-expr` in the public repo, as they stand. Run `make vm` first.

    python3 measure/mistakes.py   # six wrong parsers against fuzz.py's random expressions
    python3 measure/limits.py     # how deep an expression can go; time in each stage

Measured on an Apple M1, 8 GB, macOS 27.2, Apple clang 21, Python 3.9.6.
