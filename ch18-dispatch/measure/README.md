# Measurements for the printed chapter

Run from the chapter's folder, after `make all benchmarks`:

    python3 measure/bench.py

It times the three builds on the four benchmarks, best of seven runs,
and builds a fourth machine from a copy of `vm.c` (the switch build,
with a counter at the fetch) to count the instructions each benchmark
executes and which instruction follows which. It also compiles each
build to assembly and counts its indirect jumps (`br xN` on arm64,
`jmp *` on x86-64).

On the M1 (8 GB, macOS 27.2, Apple clang 21, `-O2`), 11 November 2026:

                  executed     switch     goto   threaded
    fib         26,925,370      75 ms    60 ms      51 ms
    loop       260,000,007     561 ms   549 ms     551 ms
    sieve       23,636,044      55 ms    53 ms      54 ms
    closures    26,477,794      81 ms    73 ms      71 ms
    jumps                           1        2         31

    after LT, in all four: JZ, 4,483,377 times

The first two runs that day gave every time 1.6 times longer, with
the same ratios; four runs since agree with the table above. The cause
was most likely the battery: macOS runs this computer in a low-power
mode on battery, and in chapter 21 the same factor came and went with
the power cable.
