// Exercise 23.3: what slicing costs, measured under Node.js with the
// playground's machine.js and vm.wasm, running a program as the page's
// run() does, one vm_step() at a time from JavaScript:
//
//   vm_run       the whole program in one call, no stepping, no slices
//   steps        one vm_step() at a time, never giving control back
//   200k/frame   200,000 steps, then wait for the next frame, as the page
//                did; a frame is modelled as a wait until 1/60 s after
//                the last frame began
//   ms=n         steps for n ms, checking the clock every 1000, then give
//                control back by a message to itself, as the page now does
//
//     node slices.mjs program.vm
//
// Prints the best of three of each, in milliseconds.

import { readFileSync } from "node:fs";
import { Machine } from "../web/machine.js";

const file = new Uint8Array(readFileSync(process.argv[2]));
const machine = await Machine.create(readFileSync(new URL("../web/vm.wasm", import.meta.url)), () => {});
const channel = new MessageChannel();
let next = null;
channel.port1.onmessage = () => next();
const soon = (f) => { next = f; channel.port2.postMessage(0); };

function plain() {
    machine.run();
}
function steps() {
    while (machine.step())
        ;
}
function frames() {
    return new Promise((done) => {
        let frame = performance.now();
        const slice = () => {
            for (let i = 0; i < 200000; i++)
                if (!machine.step()) return done();
            frame += 1000 / 60;
            setTimeout(slice, Math.max(0, frame - performance.now()));
        };
        slice();
    });
}
function timed(ms) {
    return () => new Promise((done) => {
        const slice = () => {
            const end = performance.now() + ms;
            do {
                for (let i = 0; i < 1000; i++)
                    if (!machine.step()) return done();
            } while (performance.now() < end);
            soon(slice);
        };
        slice();
    });
}

const ways = [["vm_run", plain], ["steps", steps], ["200k/frame", frames],
              ["ms=2", timed(2)], ["ms=10", timed(10)], ["ms=50", timed(50)]];
const cells = [];
for (const [name, way] of ways) {
    let best = Infinity;
    for (let k = 0; k < 3; k++) {
        machine.load(file);
        const t0 = performance.now();
        await way();
        best = Math.min(best, performance.now() - t0);
    }
    cells.push(`${name} ${Math.round(best)}`);
}
console.log(cells.join(", "));
channel.port1.close();
