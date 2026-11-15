# Watching the machine run, measured

`vm.c`, the tools, the `Makefile`, `samples/` and `tests/` are from `ch07-trace` in the public
repo, as they stand, but for two lines broken to fit the printed page: a comment in `vm.c`
and an error message in `asm.py`. `make test` runs the samples, plain and traced, and
compares a trace, two debugger sessions and a replay with the files in `tests/`.
`measure/tracecost.py` times a loop of about 210,000 steps run plainly, traced, and traced
with standard error buffered, and gives the trace's size.

    python3 measure/tracecost.py

On an Apple M1 it takes about half a minute; the times depend on the computer and its disk.
