# Measurements for chapter 14

Run in `code/ch14-gc`, after `make test`.

- `python3 measure/cost.py`: `samples/trees.asm` with its long-lived tree of
  depth 10, 11 and 12, under both collectors: collections and places freed or
  copied (from `./vm -s`), time collecting and the whole run, best of seven. It
  builds a copy of `vm.c` that prints the time collecting to a millionth of a
  second instead of a thousandth; nothing else is changed.

Measured on an Apple M1, 8 GB, macOS 27.2, Apple clang 21, Python 3.9.6:

    depth collector collections     places  collecting  whole run  share
       10 mark               28    1604848     1.81 ms      97 ms   1.9%
       10 copy               28     230160     0.50 ms      96 ms   0.5%
       11 mark               33    1621224     2.40 ms      97 ms   2.5%
       11 copy               33     541464     0.99 ms      97 ms   1.0%
       12 mark               49    1604848     4.40 ms     101 ms   4.4%
       12 copy               49    1606416     2.75 ms     100 ms   2.7%
