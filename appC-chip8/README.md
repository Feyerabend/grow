# Appendix C: CHIP-8

The virtual machine of RCA's COSMAC VIP, in one Python program,
`chip8.py`. The book's appendix C describes it; this is the machine to
run. It does what the VIP's interpreter did, or, with `-m chip48`, what
CHIP-48 did on the HP-48 calculator: the four differences are listed at
the top of `chip8.py`.

    make check
    python3 chip8.py samples/answer.hex
    python3 chip8.py -m chip48 samples/quirks.hex
    python3 chip8.py -t samples/collide.hex

It has no window and no keyboard. It runs until the program jumps to
itself, the usual way a CHIP-8 program ends, or waits for a key with
none left to give it, or has run as many instructions as it may (`-n`),
and then prints the screen. `-k` gives it keys, as hexadecimal digits,
taken one at a time by `FX0A`. `-t`
shows every instruction, in words, with `I` and the registers; `-s`
seeds the random numbers of `CXKK`, so that a run can be repeated.

The samples:

- `answer.hex`: six times seven, by adding, drawn in decimal.
- `collide.hex`: two blocks drawn overlapping, and `VF` saying they met.
- `quirks.hex`: the four differences, each leaving a digit: 1 0 0 1 on
  the VIP, 3 5 8 2 on CHIP-48.

Its timers count down once every ten instructions, standing in for 60 a
second; CHIP-48's 64 a second, and its waiting to draw once a frame, do
not show here, since this machine does not keep time.

`answers/` holds the worked answers to the appendix's exercises, which
`make check` runs too.

## In a browser

`web/index.html` is the same machine, in JavaScript, with a window and a
keyboard. Open it from disk; it needs no server and nothing from the
network. Choose a sample or an answer, or type a program, and run it,
or step it one instruction at a time: the screen, the registers, the
timers and the stack are shown, and the instructions round `pc`, each
beside the line of the program it came from. The sixteen keys are on
the page, and on the keyboard as `1 2 3 4`, `Q W E R`, `A S D F` and
`Z X C V`, in the VIP's layout. A key held down answers `EX9E` and
`EXA1`; a run that reaches `FX0A` waits, and goes on when a key is
pressed. While the sound timer is above 0, the page sounds a tone.
At loading, the page marks with `!` in its listing each word that would
trap if it ran, and each jump or call that leaves the program or lands
in the middle of a word. They are warnings, and the program runs: a
CHIP-8 program keeps its sprites among its instructions, as
`collide.hex` does, and may jump to code it writes itself, so nothing
can be refused before it runs.
Its colours are after the VIP in its case, the VP-711, which came "with a
nice blue plastic shell" (oldcomputers.net), its keys a membrane pad, and
its picture white on black on a television; the shade of blue is a
guess.

- `chip8.js`: the machine, rule for rule `chip8.py`'s, the same in the
  browser and in Node.
- `app.js`: the page: time, keys, sound and what is shown.
- `samples.js`: the samples and answers, for a page that cannot fetch
  files. Made by `samples.py`; make it again when a `.hex` changes.
- `run.js`: `chip8.js` with `chip8.py`'s command line, for Node.
- `fuzz.py`: random programs, on both machines.

With Node.js installed, `make check` runs `web/check.sh`: through
`run.js`, the page's machine must print every sample's and answer's
`.out` file, as `chip8.py` does, and the two must print the same on 200
random programs, traces and traps included. The page runs ten
instructions each time it draws the screen, sixty times a second, so
that the timers, which count down once every ten instructions as in
`chip8.py`, run at the VIP's 60 a second; the speed can be changed.
