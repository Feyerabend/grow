// One WebAssembly module run two ways: on the engine of the browser, or
// of Node.js, and on appendix F's machine, wasm.c compiled to WebAssembly,
// running inside that engine. The module is chapter 23's machine,
// vm.wasm, and it runs a .vm program of the book's.
//
// A plain script, so that the page works opened from disk; under Node.js,
// check.cjs loads it with require.

(function (exports) {
    "use strict";

    const decoder = new TextDecoder();

    function cString(memory, address) {
        const bytes = new Uint8Array(memory.buffer);
        let end = address;
        while (bytes[end] !== 0) end++;
        return decoder.decode(bytes.subarray(address, end));
    }

    // The engine's own run, as chapter 23's machine.js does it.
    async function runNative(vmWasm, program) {
        const out = [];
        let vm;
        const imports = {
            env: {
                host_write: (c) => { out.push(c); },
                host_trap: (why, at) => { throw { trap: `trap: ${cString(vm.memory, why)} at ${at}` }; },
            },
        };
        const t0 = now();
        vm = (await WebAssembly.instantiate(vmWasm, imports)).instance.exports;
        const size = Math.min(program.length, vm.vm_input_size());
        new Uint8Array(vm.memory.buffer, vm.vm_input(), size).set(program.subarray(0, size));
        const refused = vm.vm_load(size);
        let end = null;
        if (refused !== 0) {
            end = cString(vm.memory, refused);
        } else {
            vm.vm_set_collector(0, 0);
            vm.vm_reset();
            try { vm.vm_run(); } catch (e) { if (!e || !e.trap) throw e; end = e.trap; }
        }
        return { output: decoder.decode(new Uint8Array(out)), end, ms: now() - t0 };
    }

    // A new instance of appendix F's machine. web_fail throws; after
    // that, the instance is not used again.
    async function appendixF(appfWasm, out) {
        let f;
        const imports = {
            env: {
                web_write: (c) => { out.push(c); },
                web_fail: (kind, message) => {
                    throw { kind: kind === 0 ? "refused" : "trap", message: cString(f.memory, message) };
                },
            },
        };
        f = (await WebAssembly.instantiate(appfWasm, imports)).instance.exports;
        return f;
    }

    function give(f, bytes) {
        const p = f.web_buffer(bytes.length);
        new Uint8Array(f.memory.buffer, p, bytes.length).set(bytes);
        return p;
    }

    // vm.wasm on appendix F's machine, running the same program.
    async function runOnF(appfWasm, vmWasm, program) {
        const out = [];
        const t0 = now();
        const f = await appendixF(appfWasm, out);
        let end = null;
        try {
            const why = f.web_load(give(f, vmWasm), vmWasm.length);
            if (why !== 0) throw { kind: "refused", message: cString(f.memory, why) };
            const refused = f.web_run_vm(give(f, program), program.length);
            if (refused !== 0) end = cString(f.memory, refused);
        } catch (e) {
            if (!e || !e.kind) throw e;
            if (e.kind === "refused") end = `refused: ${e.message}`;
            else end = e.message;
        }
        return { output: decoder.decode(new Uint8Array(out)), end, ms: now() - t0,
                 steps: f.web_steps() };
    }

    // What each says of a module it must refuse.
    async function refuse(appfWasm, module) {
        let native;
        try {
            await WebAssembly.compile(module);
            native = "accepted";
        } catch (e) {
            native = String(e.message || e);
        }
        const f = await appendixF(appfWasm, []);
        let ours;
        try {
            const why = f.web_load(give(f, module), module.length);
            ours = why === 0 ? "accepted" : cString(f.memory, why);
        } catch (e) {
            if (!e || !e.kind) throw e;
            ours = e.message;
        }
        return { native, ours };
    }

    // A module with one function, typed to return an i32, whose body
    // leaves an i64: (func (result i32) i64.const 0).
    const BROKEN = new Uint8Array([
        0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00,     // \0asm, version 1
        0x01, 0x05, 0x01, 0x60, 0x00, 0x01, 0x7f,           // type: () -> i32
        0x03, 0x02, 0x01, 0x00,                             // one function, of type 0
        0x0a, 0x06, 0x01, 0x04, 0x00, 0x42, 0x00, 0x0b,     // code: i64.const 0, end
    ]);

    function now() {
        return typeof performance !== "undefined" ? performance.now() : Date.now();
    }

    exports.runNative = runNative;
    exports.runOnF = runOnF;
    exports.refuse = refuse;
    exports.BROKEN = BROKEN;
})(typeof module !== "undefined" ? module.exports : (window.Both = {}));
