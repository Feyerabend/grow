// The page's check, under Node.js: every program of the page, run on
// chapter 23's machine by the engine itself and by appendix F's machine
// inside it, must print the same and end the same; and the broken module
// must be refused by both.
//
//     node web/check.cjs

const B = require("./both.js");
const { APPF, VM, PROGRAMS } = require("./data.js");

const bytes = (b64) => Uint8Array.from(Buffer.from(b64, "base64"));

(async () => {
    const appf = bytes(APPF), vm = bytes(VM);
    for (const [name, program] of PROGRAMS) {
        const p = bytes(program);
        const a = await B.runNative(vm, p);
        const f = await B.runOnF(appf, vm, p);
        if (a.output !== f.output || a.end !== f.end) {
            console.log(`${name}: the two differ`);
            console.log(`  engine:      ${JSON.stringify(a.output)} ${a.end}`);
            console.log(`  appendix F:  ${JSON.stringify(f.output)} ${f.end}`);
            process.exit(1);
        }
    }
    const r = await B.refuse(appf, B.BROKEN);
    if (r.native === "accepted" || r.ours === "accepted") {
        console.log(`the broken module was accepted: ${JSON.stringify(r)}`);
        process.exit(1);
    }
    console.log(`page: ${PROGRAMS.length} programs the same both ways; the broken module refused by both`);
})().catch((e) => { console.error(e); process.exit(1); });
