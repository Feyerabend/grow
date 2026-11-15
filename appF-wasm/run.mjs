// Run a program of programs/, compiled to WebAssembly, under Node.js, as
// wasm runs it: the module imports env.putchar, and main gives the exit
// status. The referee for the programs.
//
//     node run.mjs program.wasm

import { readFileSync, writeSync } from "node:fs";

let out = [];
const imports = { env: { putchar: (c) => { out.push(c & 255); } } };
const bytes = readFileSync(process.argv[2]);
const { instance } = await WebAssembly.instantiate(bytes, imports);
let status = 0;
try {
    status = instance.exports.main();
} catch (e) {
    writeSync(1, Buffer.from(out));
    writeSync(2, `${e.message}\n`);
    process.exit(1);
}
writeSync(1, Buffer.from(out));
process.exit(status);
