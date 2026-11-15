/*
 * The page: a program typed or chosen, the machine of chip8.js running
 * it, and what can be seen of it. The machine is chip8.py's; what the
 * page adds is time, keys and sound. It runs some instructions each
 * time the screen is redrawn, sixty times a second, and stops where
 * run.js would stop, but for a key: when the program waits for one, it
 * waits, and goes on when one is pressed.
 */
"use strict";
(function () {
    const { Machine, Chip8Error, load, describe, hex } = CHIP8;
    const $ = (id) => document.getElementById(id);

    // The VIP's keypad, as it was laid out, and the keyboard keys for it.
    const PAD = ["1", "2", "3", "C", "4", "5", "6", "D", "7", "8", "9", "E", "A", "0", "B", "F"];
    const KEYBOARD = "1234qwerasdfzxcv";

    let machine = null, program = null, running = false, waiting = false, stopped = null;
    let warnings = new Map();       // address -> what may be wrong there
    let previous = new Array(16).fill(0);

    /* ---- the program ---- */

    function fill() {
        const select = $("sample");
        SAMPLES.forEach((s, k) => {
            const option = document.createElement("option");
            option.value = k;
            option.textContent = s.name;
            select.appendChild(option);
        });
        const own = document.createElement("option");
        own.value = "own";
        own.textContent = "your own";
        select.appendChild(own);
        select.addEventListener("change", () => {
            if (select.value === "own") return;
            choose(SAMPLES[select.value]);
            start();
        });
        $("code").addEventListener("input", () => { select.value = "own"; $("title").textContent = ""; });
    }

    function choose(sample) {
        $("code").value = sample.text;
        $("title").textContent = sample.title;
        // quirks.hex and shift.hex show the difference: start on the VIP.
        $("kind").value = "vip";
    }

    /* What may be wrong, found before running: a word that would trap if
     * it ran, and a jump or call that leaves the program. Only warnings:
     * a CHIP-8 program keeps its data, its sprites, among its
     * instructions, and may jump to code it writes itself, so nothing
     * can be refused before it runs, as appendix C's fifth answer says. */
    function check(data) {
        const found = new Map(), end = 0x200 + data.length;
        for (let at = 0x200; at + 1 < end; at += 2) {
            const w = data[at - 0x200] << 8 | data[at - 0x200 + 1];
            const top = w >> 12, target = w & 0xFFF;
            if (describe(w) === "unknown")
                found.set(at, "not an instruction: traps if it runs, unless it is data");
            else if ((top === 0x1 || top === 0x2) && (target < 0x200 || target >= end))
                found.set(at, `${top === 0x1 ? "jumps" : "calls"} outside the program, to ${hex(target, 3)}`);
            else if ((top === 0x1 || top === 0x2) && target % 2 !== 0)
                found.set(at, `${top === 0x1 ? "jumps" : "calls"} into the middle of a word, at ${hex(target, 3)}`);
        }
        return found;
    }

    /* Read the program and make a new machine for it. */
    function start() {
        pause();
        try {
            program = load($("code").value);
        } catch (e) {
            if (!(e instanceof Chip8Error)) throw e;
            machine = null;
            say(e.message, true);
            draw();
            return;
        }
        machine = new Machine(program.data, {
            seed: parseInt($("seed").value, 10) || 0,
            chip48: $("kind").value === "chip48",
        });
        previous = machine.v.slice();
        waiting = false;
        stopped = null;
        warnings = check(program.data);
        const loaded = `loaded: ${program.data.length} bytes, from 200 to ${hex(0x200 + program.data.length - 1, 3)}`;
        const n = warnings.size;
        say(n ? `${loaded}; ${n} word${n === 1 ? "" : "s"} marked ! in the listing below` : loaded);
        show();
    }

    /* ---- running ---- */

    function say(text, bad) {
        $("status").textContent = text;
        $("status").className = bad ? "bad" : "";
    }

    /* Run n instructions, or fewer if the machine stops or waits. */
    function run(n) {
        if (!machine || stopped) return;
        previous = machine.v.slice();
        try {
            for (let k = 0; k < n; k++) {
                const before = [machine.steps, machine.delay, machine.sound];
                const reason = machine.step();
                if (reason === "the program waits for a key") {
                    // chip8.py counts the wait as an instruction, and ends
                    // there; here FX0A runs again when a key comes, so the
                    // wait is taken back, and the count stays chip8.py's.
                    [machine.steps, machine.delay, machine.sound] = before;
                    waiting = true;
                    say("waiting for a key");
                    return;
                }
                if (reason) {
                    // A jump to itself does jump: chip8.py stops before
                    // setting pc, and the page shows where it is.
                    if (reason === "the program jumped to itself") machine.pc -= 2;
                    stopped = reason;
                    pause();
                    say(`stopped after ${machine.steps} instructions: ${reason}`);
                    return;
                }
            }
        } catch (e) {
            if (!(e instanceof Chip8Error)) throw e;
            stopped = e.message;
            pause();
            say(`trap after ${machine.steps} instructions: ${e.message}`, true);
        }
    }

    function frame() {
        if (!running) return;
        if (!waiting) {
            run(parseInt($("speed").value, 10));
            if (running && !waiting) say(`running: ${machine.steps} instructions`);
        }
        show();
        requestAnimationFrame(frame);
    }

    function go() {
        if (!machine) start();
        if (!machine) return;
        if (stopped) start();
        running = true;
        $("run").textContent = "Pause";
        requestAnimationFrame(frame);
    }

    function pause() {
        running = false;
        $("run").textContent = "Run";
        beep(false);
    }

    /* ---- keys ---- */

    function press(k, down) {
        if (machine) {
            machine.down[k] = down;
            if (down && waiting) {
                machine.keys.push(k);
                waiting = false;
                if (!running) {
                    run(1);
                    show();
                }
            }
        }
        $("keypad").children[PAD.indexOf(hex(k, 1))].classList.toggle("down", down);
    }

    function keypad() {
        PAD.forEach((label, k) => {
            const button = document.createElement("button");
            const value = parseInt(label, 16);
            button.innerHTML = `${label}<small>${KEYBOARD[k].toUpperCase()}</small>`;
            button.setAttribute("aria-label", `key ${label}`);
            button.addEventListener("pointerdown", (e) => { e.preventDefault(); press(value, true); });
            for (const up of ["pointerup", "pointerleave"])
                button.addEventListener(up, () => { if (button.classList.contains("down")) press(value, false); });
            $("keypad").appendChild(button);
        });
        const typing = () => ["TEXTAREA", "INPUT", "SELECT"].includes(document.activeElement.tagName);
        for (const [type, down] of [["keydown", true], ["keyup", false]]) {
            document.addEventListener(type, (e) => {
                if (typing() || e.metaKey || e.ctrlKey || e.altKey) return;
                const at = KEYBOARD.indexOf(e.key.toLowerCase());
                if (at < 0 || (down && e.repeat)) return;
                e.preventDefault();
                press(parseInt(PAD[at], 16), down);
            });
        }
    }

    /* ---- sound: a tone while the sound timer is above 0 ---- */

    let audio = null, tone = null;
    function beep(on) {
        if (on && !tone) {
            audio = audio || new (window.AudioContext || window.webkitAudioContext)();
            tone = audio.createOscillator();
            const gain = audio.createGain();
            gain.gain.value = 0.04;
            tone.type = "square";
            tone.frequency.value = 440;
            tone.connect(gain).connect(audio.destination);
            tone.start();
        } else if (!on && tone) {
            tone.stop();
            tone = null;
        }
    }

    /* ---- what can be seen ---- */

    function draw() {
        const canvas = $("screen"), g = canvas.getContext("2d");
        const style = getComputedStyle(document.documentElement);
        g.fillStyle = style.getPropertyValue("--screen");
        g.fillRect(0, 0, 64, 32);
        if (!machine) return;
        g.fillStyle = style.getPropertyValue("--pixel");
        machine.screen.forEach((row, y) => row.forEach((p, x) => { if (p) g.fillRect(x, y, 1, 1); }));
    }

    function registers() {
        const m = machine;
        $("regs").innerHTML = m.v.map((r, k) =>
            `<div class="${r !== previous[k] ? "changed" : ""}"><span>V${hex(k, 1)}</span> <b>${hex(r, 2)}</b></div>`
        ).join("");
        const stack = m.stack.length ? m.stack.map((a) => hex(a, 3)).join(" ") : "empty";
        $("more").innerHTML = [
            `<span><span style="color:var(--muted)">pc</span> ${hex(m.pc, 3)}</span>`,
            `<span><span style="color:var(--muted)">I</span> ${hex(m.i, 3)}</span>`,
            `<span><span style="color:var(--muted)">delay</span> ${m.delay}</span>`,
            `<span><span style="color:var(--muted)">sound</span> ${m.sound}</span>`,
            `<span><span style="color:var(--muted)">steps</span> ${m.steps}</span>`,
            `<span><span style="color:var(--muted)">stack</span> ${stack}</span>`,
        ].join("");
    }

    /* The instructions around pc, each with the line of the program it came from. */
    function listing() {
        const m = machine, rows = [];
        const source = $("code").value.split("\n");
        const first = Math.max(0x200, m.pc - 8);
        for (let at = first; at < first + 24 && at < 4095; at += 2) {
            const w = m.word(at);
            const k = (at - 0x200) / 2;
            const inProgram = k >= 0 && k < program.lines.length;
            let comment = "";
            if (inProgram) {
                const line = source[program.lines[k]] || "";
                const semicolon = line.indexOf(";");
                comment = semicolon >= 0 ? line.slice(semicolon + 1).trim() : "";
                // The samples begin a comment with the address: it is in the first column.
                if (comment.toUpperCase().startsWith(hex(at, 3))) comment = comment.slice(3).trim();
            }
            const text = inProgram ? describe(w) : "";
            const warning = warnings.get(at);
            const mark = warning ? `<span class="warn" title="${escape(warning)}">!</span>` : "";
            rows.push(`<tr class="${at === m.pc ? "here" : ""}"><td>${mark}${hex(at, 3)}</td><td>${hex(w, 4)}</td>` +
                      `<td>${escape(warning ? warning : text)}</td><td class="src">${escape(comment)}</td></tr>`);
        }
        $("listing").innerHTML = rows.join("");
    }

    function escape(s) {
        return s.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
    }

    function show() {
        draw();
        if (!machine) {
            $("regs").innerHTML = "";
            $("more").innerHTML = "";
            $("listing").innerHTML = "";
            return;
        }
        registers();
        listing();
        beep(running && machine.sound > 0);
    }

    /* ---- wiring ---- */

    function speed() {
        $("speedText").textContent = `${$("speed").value} a frame`;
    }

    fill();
    keypad();
    speed();
    $("speed").addEventListener("input", speed);
    $("load").addEventListener("click", start);
    $("reset").addEventListener("click", start);
    $("kind").addEventListener("change", start);
    $("seed").addEventListener("change", start);
    $("run").addEventListener("click", () => (running ? pause() : go()));
    $("step").addEventListener("click", () => {
        pause();
        if (!machine || stopped) start();
        if (machine && !waiting) run(1);
        show();
    });
    matchMedia("(prefers-color-scheme: dark)").addEventListener("change", draw);
    choose(SAMPLES[0]);
    start();
})();
