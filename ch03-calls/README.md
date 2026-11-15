# Calls, measured

`vm.c` is the machine of `ch03-calls` in the public repo, as it stands, with its `Makefile`
and `expected.txt`: `make test` runs it and compares what it prints with `expected.txt`. `measure/calls.py`
makes chapter 3's tables: it writes programs with labels, turns them into the machine's
numbers, and runs them in a copy of the machine that counts instructions and the most
frames and stack places in use at once.

    python3 measure/calls.py
