# Traps, measured

`vm.c` is the machine of `ch04-traps` in the public repo, as it stands, with its `Makefile`,
`expected.txt` and `traps.txt`: `make test` runs the good program and each bad one, and
compares what they print with those two files. The measurements use
copies of it and of `../ch03-calls/vm.c` that read their program from a file (`measure/harness.py`).

    python3 measure/random_programs.py 2000 1
    python3 measure/cost.py

Both were run on an Apple M1 with 8 GB, macOS 27.2 and Apple clang 21. There the random
programs took about nine minutes. The script starts 4000 runs, half of them under
AddressSanitizer, and waits out a second for each program that never stops, so how long it
takes depends on the computer. The counts do not: the programs come from a fixed seed. The
times of `cost.py` depend on the computer too.
