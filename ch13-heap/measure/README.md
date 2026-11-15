# Measurements for chapter 13

Run in `code/ch13-heap`, after `make test` (which makes `build/`).

- `python3 measure/mutants.py`: twelve one-line mistakes in `vm.c`'s heap
  and tags; for each, whether the suite (`conform.py`) or the traces against
  `vm.py` (`compare.py`) catch it.
- `python3 measure/tags.py`: two enkel/0 programs that do not use the heap,
  compiled by `../ch10-enkel/enkel.py`, run on chapter 10's `vm.c` (a value is
  an int), this chapter's (a tag and an int), and this chapter's with the tag
  checks taken out. Best of five, `cc -O2`.

Measured on an Apple M1, 8 GB, macOS 27.2, Apple clang 21, Python 3.9.6.

The same mistake as the first mutant, NEW not zeroing its fields, was also
tried on chapter 14's `vm.c` (the line `heap[b + HEADER + i] = integer(0);`
made empty), with chapter 14's suite: `-g mark`, `-g copy` and `-g copy -S`
pass all 66; `-g mark -S` fails `heap-fields`.
