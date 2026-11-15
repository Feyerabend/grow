# Programs in files, measured

`vm.c`, `tobin.py`, `FORMAT.md`, `badfiles.py`, `badfiles.txt`, the `Makefile` and `samples/`
are from `ch05-files` in the public repo, as they stand, but for one comment in `vm.c`, broken
over two lines to fit the printed page. `make test` runs the samples, and the broken files
`badfiles.py` writes into `tests/`.
`measure/damage.py` makes chapter 5's table: it changes one byte of a good program file at a
time and counts what the machine does with it.

    python3 measure/damage.py 1000 1

On an Apple M1 with Apple clang this took about a minute and a half; it depends on the
computer. The counts come from a fixed seed and do not.
