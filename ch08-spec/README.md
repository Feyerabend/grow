# A specification, measured

The machines, tools, `SPEC.md`, `suite/`, `samples/` and the `Makefile` are from `ch08-spec`
in the public repo, as they stand, but for two lines broken to fit the printed page: a
comment in `vm.c` and an error message in `asm.py`. `make test` runs both machines on the
conformance suite and the samples, and compares their traces.

    python3 measure/fuzz.py 1000 1          # both machines on random programs, and five mutants
    python3 measure/shrink.py 1 computing   # shrinking, with the generator shaped for the property

On an Apple M1, fuzz.py takes about three and a half minutes and shrink.py with `computing`
about two. Without `computing`, shrink.py also tries 2000 random programs for each mutant,
which takes about half an hour. The counts come from a fixed seed; the times depend on the
computer.
