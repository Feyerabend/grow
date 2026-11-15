# Measurements for chapter 15

Run in `code/ch15-closures`, after `make test`.

- `python3 measure/cost.py`: fib, gcd and ack in lambda/0 and in enkel/0
  (compiled by `../ch10-enkel/enkel.py`), on this chapter's machine:
  instructions executed (lines of `./vm -t`) and blocks and places made
  (`./vm -s`). Then, by bisection, how deep lambda/0 recursion goes before the
  stack of 256 values runs out.
- `python3 measure/share.py`: two Python closures sharing one changing
  variable; the docstring gives the same in JavaScript, run with node v26.

Measured on an Apple M1, 8 GB, macOS 27.2, Apple clang 21, Python 3.9.6:

    call                         lambda/0  enkel/0  blocks  places
    fib 20                         361214   394037       1       4
    gcd 1836311903 1134903170        1769      545      46     229
    ack 2 3                          1976      765      45     224
    sum n recurses to n = 83; at 84: trap: stack overflow at 54
    a list folds up to 82 elements; at 83: trap: stack overflow at 103
