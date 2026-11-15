# Jumps, measured

`vm.c` is the machine of `ch02-jumps` in the public repo, as it stands, with its `Makefile`
and `expected.txt`: `make test` runs it and compares what it prints with `expected.txt`. `measure/mix.py`
makes chapter 2's table: it runs the Fibonacci program in a copy of the machine that
counts each instruction, and sorts the counts into juggling, work and jumps.

    python3 measure/mix.py
