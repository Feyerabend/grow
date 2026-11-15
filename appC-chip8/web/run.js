/*
 * chip8.js from the command line, as chip8.py runs: the same options,
 * the same screen printed, the same last line. web/check.sh holds the
 * two to each other on every sample and answer.
 *
 *     node run.js [-t] [-n steps] [-s seed] [-k keys] [-m vip | -m chip48] program.hex
 */
"use strict";
const fs = require("fs");
const { Machine, Chip8Error, load, describe, hex } = require("./chip8.js");

function main(args) {
    let trace = false, limit = 100000, seed = 1, chip48 = false, keys = [];
    const files = [];
    while (args.length) {
        const a = args.shift();
        if (a === "-t") trace = true;
        else if (a === "-n" && args.length) limit = parseInt(args.shift(), 10);
        else if (a === "-s" && args.length) seed = parseInt(args.shift(), 10);
        else if (a === "-k" && args.length) keys = [...args.shift()].map((k) => parseInt(k, 16));
        else if (a === "-m" && ["vip", "chip48"].includes(args[0])) chip48 = args.shift() === "chip48";
        else files.push(a);
    }
    if (files.length !== 1) {
        console.error("usage: run.js [-t] [-n steps] [-s seed] [-k keys] [-m vip | -m chip48] program.hex");
        process.exit(1);
    }
    try {
        const machine = new Machine(load(fs.readFileSync(files[0], "utf8")).data, { seed, chip48 });
        machine.keys = keys;
        let why = `it ran ${limit} instructions`;
        while (machine.steps < limit) {
            if (trace) {
                const w = machine.word(machine.pc);
                const registers = machine.v.map((r) => hex(r, 2)).join(" ");
                console.log(`  ${hex(machine.pc, 3)}  ${hex(w, 4)}  ${describe(w).padEnd(28)} ` +
                            `I=${hex(machine.i, 3)}  ${registers}`);
            }
            const reason = machine.step();
            if (reason) {
                why = reason;
                break;
            }
        }
        console.log(machine.picture());
        console.log(`stopped after ${machine.steps} instructions: ${why}`);
    } catch (e) {
        if (!(e instanceof Chip8Error)) throw e;
        console.error(`chip8: ${e.message}`);
        process.exit(1);
    }
}

main(process.argv.slice(2));
