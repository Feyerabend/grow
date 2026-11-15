"""
chip8.js against chip8.py on random programs: each is a few dozen
random instructions, of every kind, with jumps and calls into the
program itself, and a jump back to its start at the end. Both machines
run each one with a trace, on the VIP and on CHIP-48, with keys; what
they print, on standard output and standard error, and how they end,
must be the same to the character.

    python3 fuzz.py [N] [SEED]
"""

import os
import random
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def program(rng):
    words = []
    size = rng.randint(4, 40)
    for _ in range(size):
        top = rng.randrange(16)
        x, y, n = rng.randrange(16), rng.randrange(16), rng.randrange(16)
        near = 0x200 + 2 * rng.randrange(size)          # an instruction of this program
        if top == 0:
            w = rng.choice([0x00E0, 0x00EE, 0x00E0, rng.randrange(0x1000)])
        elif top in (1, 2, 0xA, 0xB):
            w = top << 12 | (near if rng.random() < 0.9 else rng.randrange(0x1000))
        elif top in (3, 4, 6, 7, 0xC):
            w = top << 12 | x << 8 | rng.randrange(256)
        elif top in (5, 9):
            w = top << 12 | x << 8 | y << 4 | (0 if rng.random() < 0.9 else n)
        elif top == 8:
            w = 0x8000 | x << 8 | y << 4 | rng.choice([0, 1, 2, 3, 4, 5, 6, 7, 0xE, n])
        elif top == 0xD:
            w = 0xD000 | x << 8 | y << 4 | n
        elif top == 0xE:
            w = 0xE000 | x << 8 | rng.choice([0x9E, 0xA1, rng.randrange(256)])
        else:
            w = 0xF000 | x << 8 | rng.choice([0x07, 0x0A, 0x15, 0x18, 0x1E, 0x29,
                                               0x33, 0x55, 0x65, rng.randrange(256)])
        words.append(f"{w:04X}")
    words.append("1200")        # and round again, rather than off the end
    return "\n".join(words) + "\n"


def run(command):
    r = subprocess.run(command, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    work = tempfile.mkdtemp()
    path = os.path.join(work, "p.hex")
    endings = {}
    for k in range(n):
        with open(path, "w") as f:
            f.write(program(rng))
        options = ["-t", "-n", "400", "-s", str(rng.randrange(1000)),
                   "-m", rng.choice(["vip", "chip48"])]
        if rng.random() < 0.5:
            options += ["-k", "".join(rng.choice("0123456789ABCDEF") for _ in range(3))]
        py = run([sys.executable, os.path.join(HERE, "..", "chip8.py")] + options + [path])
        js = run(["node", os.path.join(HERE, "run.js")] + options + [path])
        if py != js:
            print(f"program {k} differs, {' '.join(options)}:")
            print(open(path).read())
            sys.exit(1)
        last = (py[1].strip().splitlines() or [""])[-1] if py[0] == 0 else py[2].strip()
        why = last.split(": ", 1)[-1].split(" at ")[0]
        if why.startswith("unknown instruction"):
            why = "unknown instruction"
        endings[why] = endings.get(why, 0) + 1
    print(f"{n} random programs: chip8.js and chip8.py agree")
    for why, count in sorted(endings.items(), key=lambda e: -e[1]):
        print(f"  {count:4}  {why}")


if __name__ == "__main__":
    main()
