/*
 * CHIP-8, as chip8.py runs it: the same machine, instruction for
 * instruction, in JavaScript, for the page in index.html and for
 * run.js, which make check holds to chip8.py.
 *
 * The rules are chip8.py's. Instructions are two bytes, the program at
 * 0x200, the font at 0x050. The timers count down once every ten
 * instructions. A run stops when the program jumps to itself, or waits
 * for a key that has not been given, or does what the VIP could not:
 * a return with no call, a seventeenth nested call, an unknown
 * instruction. On the page, keys are pressed by hand: a key held down
 * answers EX9E and EXA1, and one pressed is queued for FX0A. From
 * run.js, as from chip8.py, keys come only from -k, and none is held.
 *
 * A plain script, not a module, so that the page works opened from
 * disk: in a browser it defines CHIP8; in Node it is module.exports.
 */
(function (root) {
    "use strict";

    const FONT = [
        0xF0, 0x90, 0x90, 0x90, 0xF0, 0x20, 0x60, 0x20, 0x20, 0x70,
        0xF0, 0x10, 0xF0, 0x80, 0xF0, 0xF0, 0x10, 0xF0, 0x10, 0xF0,
        0x90, 0x90, 0xF0, 0x10, 0x10, 0xF0, 0x80, 0xF0, 0x10, 0xF0,
        0xF0, 0x80, 0xF0, 0x90, 0xF0, 0xF0, 0x10, 0x20, 0x40, 0x40,
        0xF0, 0x90, 0xF0, 0x90, 0xF0, 0xF0, 0x90, 0xF0, 0x10, 0xF0,
        0xF0, 0x90, 0xF0, 0x90, 0x90, 0xE0, 0x90, 0xE0, 0x90, 0xE0,
        0xF0, 0x80, 0x80, 0x80, 0xF0, 0xE0, 0x90, 0x90, 0x90, 0xE0,
        0xF0, 0x80, 0xF0, 0x80, 0xF0, 0xF0, 0x80, 0xF0, 0x80, 0x80,
    ];
    const FONT_AT = 0x050;
    const START = 0x200;
    const WIDTH = 64, HEIGHT = 32;

    class Chip8Error extends Error {}

    const hex = (n, digits) => n.toString(16).toUpperCase().padStart(digits, "0");

    /* The bytes of a program written as hexadecimal words, one or more
     * to a line; anything after ";" is a comment. Also, for the page,
     * the line each instruction came from. */
    function load(text) {
        const data = [];
        const lines = [];
        text.split("\n").forEach((line, k) => {
            for (const word of line.split(";")[0].split(/\s+/).filter((w) => w)) {
                if (word.length !== 4)
                    throw new Chip8Error(`line ${k + 1}: '${word}' is not four hexadecimal digits`);
                if (!/^[0-9A-Fa-f]{4}$/.test(word))
                    throw new Chip8Error(`line ${k + 1}: '${word}' is not hexadecimal`);
                const value = parseInt(word, 16);
                lines.push(k);
                data.push(value >> 8, value & 0xFF);
            }
        });
        if (START + data.length > 4096)
            throw new Chip8Error("program too big");
        return { data, lines };
    }

    /* What an instruction does, in words, as chip8.py's trace says it. */
    function describe(w) {
        const x = (w >> 8) & 0xF, y = (w >> 4) & 0xF;
        const nn = w & 0xFF, nnn = w & 0xFFF, top = w >> 12;
        const X = `V${hex(x, 1)}`, Y = `V${hex(y, 1)}`;
        if (w === 0x00E0) return "clear the screen";
        if (w === 0x00EE) return "return";
        if (top === 0x1) return `jump ${hex(nnn, 3)}`;
        if (top === 0x2) return `call ${hex(nnn, 3)}`;
        if (top === 0x3) return `skip if ${X} = ${nn}`;
        if (top === 0x4) return `skip if ${X} != ${nn}`;
        if (top === 0x5 && (w & 0xF) === 0) return `skip if ${X} = ${Y}`;
        if (top === 0x6) return `${X} := ${nn}`;
        if (top === 0x7) return `${X} += ${nn}`;
        if (top === 0x8) {
            const how = {0: `${X} := ${Y}`, 1: `${X} |= ${Y}`, 2: `${X} &= ${Y}`,
                         3: `${X} ^= ${Y}`, 4: `${X} += ${Y}`, 5: `${X} -= ${Y}`,
                         6: `${X} := ${Y} >> 1`, 7: `${X} := ${Y} - ${X}`,
                         0xE: `${X} := ${Y} << 1`}[w & 0xF];
            if (how) return how;
        }
        if (top === 0x9 && (w & 0xF) === 0) return `skip if ${X} != ${Y}`;
        if (top === 0xA) return `I := ${hex(nnn, 3)}`;
        if (top === 0xB) return `jump ${hex(nnn, 3)} + V0, or + ${X} on CHIP-48`;
        if (top === 0xC) return `${X} := random & ${nn}`;
        if (top === 0xD) return `draw ${w & 0xF} rows at ${X}, ${Y}`;
        if (top === 0xE && nn === 0x9E) return `skip if key ${X} is down`;
        if (top === 0xE && nn === 0xA1) return `skip if key ${X} is up`;
        if (top === 0xF) {
            const what = {0x07: `${X} := delay`, 0x0A: `${X} := wait for a key`,
                          0x15: `delay := ${X}`, 0x18: `sound := ${X}`,
                          0x1E: `I += ${X}`, 0x29: `I := digit ${X}`,
                          0x33: `decimal digits of ${X} at I`,
                          0x55: `store V0 to ${X} at I`,
                          0x65: `load V0 to ${X} from I`}[nn];
            if (what) return what;
        }
        return "unknown";
    }

    class Machine {
        constructor(program, { seed = 1, chip48 = false } = {}) {
            this.chip48 = chip48;
            this.keys = [];                 // queued for FX0A
            this.down = new Array(16).fill(false);  // held, for EX9E and EXA1
            this.memory = new Uint8Array(4096);
            this.memory.set(FONT, FONT_AT);
            this.memory.set(program, START);
            this.v = new Array(16).fill(0);
            this.i = 0;
            this.pc = START;
            this.stack = [];
            this.delay = 0;
            this.sound = 0;
            this.screen = Array.from({ length: HEIGHT }, () => new Array(WIDTH).fill(0));
            this.seed = seed;
            this.steps = 0;
        }

        random() {
            // chip8.py's own small generator, so that runs can be repeated.
            // Its multiplication needs more than a double's 53 bits: BigInt.
            this.seed = Number((BigInt(this.seed) * 1103515245n + 12345n) & 0x7FFFFFFFn);
            return (this.seed >> 16) & 0xFF;
        }

        /* XOR a sprite onto the screen; VF says whether it hit something. */
        draw(x, y, rows) {
            x %= WIDTH;
            y %= HEIGHT;
            this.v[0xF] = 0;
            for (let r = 0; r < rows; r++) {
                if (y + r >= HEIGHT) break;
                const bits = this.memory[(this.i + r) & 0xFFF];
                for (let c = 0; c < 8; c++) {
                    if (x + c >= WIDTH) break;
                    if (bits & (0x80 >> c)) {
                        if (this.screen[y + r][x + c]) this.v[0xF] = 1;
                        this.screen[y + r][x + c] ^= 1;
                    }
                }
            }
        }

        word(at) {
            return this.memory[at] << 8 | this.memory[at + 1];
        }

        /* Run one instruction. Return a reason to stop, or null; throw
         * a Chip8Error for what the VIP could not do. */
        step() {
            const pc = this.pc;
            if (pc > 4094) throw new Chip8Error(`no instruction at ${hex(pc, 3)}`);
            const w = this.word(pc);
            const x = (w >> 8) & 0xF, y = (w >> 4) & 0xF;
            const nn = w & 0xFF, nnn = w & 0xFFF, top = w >> 12, low = w & 0xF;
            const v = this.v;
            this.pc += 2;
            this.steps += 1;
            if (this.steps % 10 === 0) {
                this.delay = Math.max(0, this.delay - 1);
                this.sound = Math.max(0, this.sound - 1);
            }
            let source, total, borrow;
            if (w === 0x00E0) {
                this.screen = Array.from({ length: HEIGHT }, () => new Array(WIDTH).fill(0));
            } else if (w === 0x00EE) {
                if (!this.stack.length) throw new Chip8Error(`return with no call at ${hex(pc, 3)}`);
                this.pc = this.stack.pop();
            } else if (top === 0x1) {
                if (nnn === pc) return "the program jumped to itself";
                this.pc = nnn;
            } else if (top === 0x2) {
                if (this.stack.length === 16) throw new Chip8Error(`too many calls at ${hex(pc, 3)}`);
                this.stack.push(this.pc);
                this.pc = nnn;
            } else if (top === 0x3) {
                if (v[x] === nn) this.pc += 2;
            } else if (top === 0x4) {
                if (v[x] !== nn) this.pc += 2;
            } else if (top === 0x5 && low === 0) {
                if (v[x] === v[y]) this.pc += 2;
            } else if (top === 0x6) {
                v[x] = nn;
            } else if (top === 0x7) {
                v[x] = (v[x] + nn) & 0xFF;
            } else if (top === 0x8 && low === 0) {
                v[x] = v[y];
            } else if (top === 0x8 && low >= 1 && low <= 3) {
                v[x] = low === 1 ? v[x] | v[y] : low === 2 ? v[x] & v[y] : v[x] ^ v[y];
                if (!this.chip48) v[0xF] = 0;     // the VIP's interpreter leaves VF at 0
            } else if (top === 0x8 && low === 4) {
                total = v[x] + v[y];
                v[x] = total & 0xFF;
                v[0xF] = total > 0xFF ? 1 : 0;
            } else if (top === 0x8 && low === 5) {
                borrow = v[x] < v[y];
                v[x] = (v[x] - v[y]) & 0xFF;
                v[0xF] = borrow ? 0 : 1;
            } else if (top === 0x8 && low === 6) {
                source = this.chip48 ? v[x] : v[y];
                v[x] = source >> 1;
                v[0xF] = source & 1;
            } else if (top === 0x8 && low === 7) {
                borrow = v[y] < v[x];
                v[x] = (v[y] - v[x]) & 0xFF;
                v[0xF] = borrow ? 0 : 1;
            } else if (top === 0x8 && low === 0xE) {
                source = this.chip48 ? v[x] : v[y];
                v[x] = (source << 1) & 0xFF;
                v[0xF] = source >> 7;
            } else if (top === 0x9 && low === 0) {
                if (v[x] !== v[y]) this.pc += 2;
            } else if (top === 0xA) {
                this.i = nnn;
            } else if (top === 0xB) {
                this.pc = (nnn + (this.chip48 ? v[x] : v[0])) & 0xFFF;
            } else if (top === 0xC) {
                v[x] = this.random() & nn;
            } else if (top === 0xD) {
                this.draw(v[x], v[y], low);
            } else if (top === 0xE && nn === 0x9E) {
                if (this.down[v[x] & 0xF]) this.pc += 2;
            } else if (top === 0xE && nn === 0xA1) {
                if (!this.down[v[x] & 0xF]) this.pc += 2;
            } else if (top === 0xF && nn === 0x07) {
                v[x] = this.delay;
            } else if (top === 0xF && nn === 0x0A) {
                if (!this.keys.length) {
                    this.pc = pc;
                    return "the program waits for a key";
                }
                v[x] = this.keys.shift();
            } else if (top === 0xF && nn === 0x15) {
                this.delay = v[x];
            } else if (top === 0xF && nn === 0x18) {
                this.sound = v[x];
            } else if (top === 0xF && nn === 0x1E) {
                this.i = (this.i + v[x]) & 0xFFF;
            } else if (top === 0xF && nn === 0x29) {
                this.i = FONT_AT + 5 * (v[x] & 0xF);
            } else if (top === 0xF && nn === 0x33) {
                const digits = [Math.floor(v[x] / 100), Math.floor(v[x] / 10) % 10, v[x] % 10];
                digits.forEach((d, k) => { this.memory[(this.i + k) & 0xFFF] = d; });
            } else if (top === 0xF && nn === 0x55) {
                for (let k = 0; k <= x; k++) this.memory[(this.i + k) & 0xFFF] = v[k];
                this.i = (this.i + x + (this.chip48 ? 0 : 1)) & 0xFFF;
            } else if (top === 0xF && nn === 0x65) {
                for (let k = 0; k <= x; k++) v[k] = this.memory[(this.i + k) & 0xFFF];
                this.i = (this.i + x + (this.chip48 ? 0 : 1)) & 0xFFF;
            } else {
                throw new Chip8Error(`unknown instruction ${hex(w, 4)} at ${hex(pc, 3)}`);
            }
            return null;
        }

        picture() {
            return this.screen.map((row) => row.map((p) => (p ? "#" : ".")).join("")).join("\n");
        }
    }

    const api = { Machine, Chip8Error, load, describe, hex, FONT_AT, START, WIDTH, HEIGHT };
    if (typeof module !== "undefined" && module.exports) module.exports = api;
    else root.CHIP8 = api;
})(this);
