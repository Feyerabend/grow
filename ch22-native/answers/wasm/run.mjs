// Exercise 22.4: run a program that vm2c.py compiled to C and Clang to
// WebAssembly, under Node.js, as a command:
//
//     node run.mjs [-g mark | -g copy] [-S] program.wasm

import { readFileSync, writeSync } from "node:fs";

const args = process.argv.slice(2);
const path = args.pop();
const copying = args.includes("copy") ? 1 : 0;
const stress = args.includes("-S") ? 1 : 0;

const out = { 1: [], 2: [] };
const flush = () => {
    for (const fd of [1, 2]) {
        if (out[fd].length) writeSync(fd, Buffer.from(out[fd]));
        out[fd] = [];
    }
};
class Exit {
    constructor(status) { this.status = status; }
}
const env = {
    host_write: (fd, c) => {
        out[fd].push(c);
        if (out[fd].length >= 4096) flush();
    },
    host_exit: (status) => { throw new Exit(status); },
};
const { instance } = await WebAssembly.instantiate(readFileSync(path), { env });
let status = 0;
try {
    instance.exports.run(copying, stress);
} catch (e) {
    if (!(e instanceof Exit)) throw e;
    status = e.status;
}
flush();
process.exit(status);
