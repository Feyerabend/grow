# An assembler, measured

`vm.c`, `asm.py`, `disasm.py`, `isa.py`, `vmfile.py`, the `Makefile`, `samples/` and `tests/`
are from `ch06-asm` in the public repo, as they stand, but for two lines broken to fit the
printed page, a comment in `vm.c` and an error message in `asm.py`, and one line added to
the `Makefile`, which removes the samples' disassembled copies once they are compared. `vm.c` is chapter 5's
machine; only its opening comment differs. `make test` assembles, runs and disassembles the
samples, and checks that `tests/errors.asm` gets each of its mistakes reported.

    python3 measure/forward.py     # labels used before and after they are defined, in the chapters
    python3 measure/onepass.py     # a one-pass assembler with holes, against asm.py
