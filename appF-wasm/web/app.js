// The page: choose a program, run it both ways, and show what each
// printed, how it ended, and how long it took; and the broken module,
// refused by both. The work is in both.js; the modules and programs are
// in data.js.

"use strict";
(function () {
    const $ = (id) => document.getElementById(id);
    const bytes = (b64) => Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
    const appf = bytes(APPF), vm = bytes(VM);

    PROGRAMS.forEach(([name], k) => $("program").add(new Option(name, k)));

    function show(which, r, extra) {
        $("out-" + which).textContent = r.output;
        $("end-" + which).textContent = r.end || "ended normally";
        $("end-" + which).className = "end mono" + (r.end ? " trap" : "");
        $("time-" + which).textContent = `${r.ms.toFixed(1)} ms${extra || ""}`;
    }

    async function run() {
        const program = bytes(PROGRAMS[$("program").value][1]);
        const a = await Both.runNative(vm, program);
        const f = await Both.runOnF(appf, vm, program);
        show("native", a);
        show("f", f, `, ${f.steps.toLocaleString("en-GB")} WebAssembly instructions`);
        const same = a.output === f.output && a.end === f.end;
        $("verdict").textContent = same ? "The same, both ways." : "They differ.";
        $("verdict").className = same ? "same" : "differ";
    }

    async function refuse() {
        $("broken").textContent = Array.from(Both.BROKEN,
            (b) => b.toString(16).padStart(2, "0")).join(" ");
        const r = await Both.refuse(appf, Both.BROKEN);
        $("refuse-native").textContent = r.native;
        $("refuse-f").textContent = r.ours;
    }

    $("run").addEventListener("click", run);
    $("program").addEventListener("change", run);
    run();
    refuse();
})();
