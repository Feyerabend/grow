// Exercise 23.5: run a .vm file on the WebAssembly machine one vm_step() at
// a time, as the playground's Step button does, so that the suite can test
// stepping:
//
//     node step.mjs machine.js-folder [-g mark | -g copy] [-S] program.vm
//
// The first argument is the folder holding web/machine.js and web/vm.wasm.

import { readFileSync, writeSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { join } from "node:path";

const args = process.argv.slice(2);
const folder = args.shift();
const path = args.pop();
const { Machine, Trap } = await import(pathToFileURL(join(folder, "web", "machine.js")));
const copying = args.includes("copy");
const stress = args.includes("-S");

let out = [];
const flush = () => {
    if (out.length) writeSync(1, Buffer.from(out));
    out = [];
};
const machine = await Machine.create(readFileSync(join(folder, "web", "vm.wasm")), (c) => {
    out.push(c);
    if (out.length >= 4096) flush();
});
let file;
try {
    file = readFileSync(path);
} catch {
    writeSync(2, `${path}: cannot open\n`);
    process.exit(2);
}
const why = machine.load(new Uint8Array(file), { copying, stress });
if (why !== null) {
    writeSync(2, `${path}: ${why}\n`);
    process.exit(2);
}
try {
    while (machine.step())
        ;
} catch (e) {
    if (!(e instanceof Trap)) throw e;
    flush();
    writeSync(2, e.message + "\n");
    process.exit(1);
}
flush();
