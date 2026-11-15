# Coroutines

The machine of `ch15-closures` in the public repo, with coroutines added, for the printed
book: chapter 16 tells it, and `SPEC.md` section 5a says what it does.

    make test

lambda/0 gains `coroutine`, `resume`, `yield` and `finished`, in `lambda.py`, with no change to
the machine. `samples/samefringe.lam` is the chapter's worked program, and `measure/fringe.py`
makes its table; `measure/cost.py` makes the table of round trips. The rest of the machine, its language and its other tests are as in chapter 15.
