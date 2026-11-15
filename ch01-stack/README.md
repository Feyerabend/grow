# A stack machine, measured

`vm.c` is the machine of `ch01-stack` in the public repo, as it stands, with its `Makefile`
and `expected.txt`: `make test` runs it and compares what it prints with `expected.txt`. `measure/depth.py`
makes chapter 1's table of stack depths: it runs each expression, in the order written and
in the best order, in a copy of the machine with a counter of the deepest the stack goes.

    python3 measure/depth.py
