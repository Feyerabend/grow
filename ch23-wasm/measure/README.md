# Measurements for the printed chapter

Run from the chapter's folder, after `make`, on mains power (on battery,
macOS runs this computer in a low-power mode, and every time comes out
about 1.6 times longer):

    python3 measure/cost.py

`cost.py` runs chapter 22's benchmarks, copied to `measure/bench`, and
`empty.asm`, `HALT` alone, best of seven, on: the core with its C host,
as `make` builds it, with `step()` forced inline into `vm_run()`; the
same with `step()` kept out of line, so that every instruction is a
call, as in the first version of `core.c`; the core as WebAssembly,
built in a temporary folder as the Makefile builds it, and the same with
`step()` forced inline there too, both run by `run.mjs` under Node.js;
and the native code of chapter 22, if `../ch22-native` is there. On the
M1 (8 GB, macOS 27.2, Apple clang 21, Homebrew LLD 23, Node.js 26.12.1,
`-O2`), on mains power, 12 November 2026, milliseconds:

                 C host  stepping   wasm  wasm inl.  native
    empty             2         3    113        109       3
    fib              70       169    258        263      14
    loop            545      1242   1301       1287      35
    sieve            56       117    226        221      14
    closures         80       182    260        267      36
    enkel-sieve     131       257    345        351       7
    basal-loop       33        79    173        173       7

## Done by hand

- `node -e ""`, best of eleven: 107 ms. Node.js starting is most of the
  115 ms an empty program takes as WebAssembly.
- `web/vm.wasm` as the public repository keeps it (11,709 bytes, built
  with another Clang, before the change to the run loop) against one
  built here from the same source (11,427 bytes), under `run.mjs`, best
  of seven: fib 249 and 255 ms, loop 1197 and 1283, sieve 212 and 222.
  With the change, built here: 11,443 bytes; with `step()` forced
  inline in WebAssembly too, 18,308.
- `clang --target=wasm32 -O2 -S core.c`: `vm_run` is a loop around
  `call step` (before the change, `call vm_step`), and the switch is a
  `br_table`. In the C build, `vm_run` has no call to `step` left.
- A computed `goto` with two labels, compiled for `wasm32`, became a
  table of small numbers and a comparison with them.
- The playground, `web/playground.html`, served over HTTP and run in a
  browser: the Fibonacci example printed 0 to 34, and the trap example
  marked `DIV` at address 10 in the listing.
