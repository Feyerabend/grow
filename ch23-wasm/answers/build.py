#!/usr/bin/env python3
"""
Make the variants of core.c for exercises 23.5 and 23.6, each in a folder
of its own with what it needs beside it:

    python3 build.py loop folder     exercise 5: vm_run() a loop of its own
    python3 build.py state folder    exercise 6: an explicit state
    python3 build.py web folder      exercises 1 and 3: the playground

loop: vm_run() gets its own loop, with the switch and ops.h in it, where
NEXT is "continue"; vm_step() keeps step(), for the debugger only. So the
instructions are in vm.wasm twice.

state: every variable of the machine moves into one struct machine, and
every function that reads or changes one is given a pointer to it, M, as
its first argument, as Lua 4.0 passes its lua_State: the vm_ functions
too. The struct is static, and vm_machine() gives its address to the
host, which passes it back on every call. host.c and web/machine.js are
changed to match, and copied beside it. The change is made by rewriting
the text of core.c and ops.h; the functions that touch no variable of the
machine, integer(), the wrapping arithmetic, same(), write_number() and
word32(), are left as they are.
"""

import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)


def patch(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def loop(folder):
    c = open(os.path.join(CHAPTER, "core.c")).read()
    c = patch(c, """EXPORT(vm_run) void vm_run(void) {
    while (step())
        ;
}""", """/*
 * Exercise 23.5: the run loop of its own, with the instructions in it.
 * HALT returns 0 from it; every other instruction goes round again.
 */
#undef NEXT
#define NEXT        continue

static int run_loop(void) {
    int op;

    if (halted)
        return 0;
    for (;;) {
        start = pc;
        if (pc < 0 || pc >= code_len)
            trap("ran off the end of the program");
        op = code[pc++];
        switch (op) {
#include "ops.h"
        }
    }
}

EXPORT(vm_run) void vm_run(void) {
    run_loop();
}""")
    open(os.path.join(folder, "core.c"), "w").write(c)
    shutil.copy(os.path.join(CHAPTER, "ops.h"), folder)
    shutil.copy(os.path.join(CHAPTER, "host.c"), folder)
    os.makedirs(os.path.join(folder, "web"), exist_ok=True)
    shutil.copy(os.path.join(CHAPTER, "web", "machine.js"), os.path.join(folder, "web"))
    shutil.copy(os.path.join(CHAPTER, "run.mjs"), folder)


def outside_strings(text, change):
    """change() applied to the text outside strings and comments."""
    parts = re.split(r'("(?:\\.|[^"\\\n])*"|/\*.*?\*/|//[^\n]*)', text, flags=re.S)
    return "".join(p if k % 2 else change(p) for k, p in enumerate(parts))


PURE = {"integer", "to_int", "wrap_add", "wrap_sub", "wrap_mul", "wrap_div", "wrap_mod",
        "same", "write_number", "word32", "host_write", "host_trap"}


def state(folder):
    c = open(os.path.join(CHAPTER, "core.c")).read()
    ops = open(os.path.join(CHAPTER, "ops.h")).read()
    lines = c.split("\n")
    # The machine's variables: every static at file scope that is not a
    # function, a constant, or the host's input buffer.
    fields, names, keep = [], [], []
    for line in lines:
        m = re.match(r"static ((?:struct \w+|unsigned char|int|long) \*?)(\w+)(\[[^\]]*\])?"
                     r"(?: = [^;]+)?;(.*)$", line)
        if m and m.group(2) != "input":
            fields.append("    %s%s%s;%s" % (m.group(1), m.group(2), m.group(3) or "",
                                            m.group(4)))
            names.append(m.group(2))
            continue
        keep.append(line)
    c = "\n".join(keep)
    # Functions with state: every function defined here but the pure ones.
    defs = re.findall(r"^(?:static|STEP|EXPORT\(\w+\)|__attribute__\(\(noreturn\)\) static)"
                      r"[^(\n]*?\b(\w+)\(", c, re.M)
    stateful = [f for f in defs if f not in PURE]

    def definitions(text):
        out = []
        for line in text.split("\n"):
            if re.match(r"^(static|STEP|EXPORT|__attribute__)", line):
                for f in stateful:
                    line = re.sub(r"\b%s\(void\)" % f, "%s(struct machine *M)" % f, line)
                    line = re.sub(r"\b%s\((?!struct machine)(?=[^)])" % f,
                                  "%s(struct machine *M, " % f, line)
                line = "\x00" + line            # a definition: no calls here to change
            out.append(line)
        return "\n".join(out)

    def calls(text):
        out = []
        for line in text.split("\n"):
            if line.startswith("\x00"):
                head = line[1:]
                # The body may follow on the same line, as in the one-line vm_ functions.
                if "{" in head:
                    sig, body = head.split("{", 1)
                    out.append(sig + "{" + calls_in(body))
                else:
                    out.append(head)
                continue
            out.append(calls_in(line))
        return "\n".join(out)

    def calls_in(text):
        def code_only(piece):
            for f in stateful:
                piece = re.sub(r"\b%s\(\)" % f, "%s(M)" % f, piece)
                piece = re.sub(r"\b%s\((?!M\b)" % f, "%s(M, " % f, piece)
            return piece
        return outside_strings(text, code_only)

    def variables(text):
        def code_only(piece):
            for n in names:
                piece = re.sub(r"(?<![.\w>])(?<!->)\b%s\b" % n, "M->%s" % n, piece)
            return piece
        return outside_strings(text, code_only)

    struct = ("/* Exercise 23.6: the whole machine, in one place. */\nstruct machine {\n"
              + "\n".join(fields) + "\n};\n\nstatic struct machine the_machine;\n")
    marker = "__attribute__((noreturn)) static void trap("
    i = c.index(marker)
    body = c[i:]
    body = variables(calls(definitions(body)))
    body = body.replace("M->M->", "M->")
    c = c[:i] + struct + "\n" + body
    c += """
/* Exercise 23.6: the machine the host is to pass to every vm_ function. */
EXPORT(vm_machine) struct machine *vm_machine(void) {
    the_machine.heap = the_machine.space_a;
    the_machine.free_list = -1;
    return &the_machine;
}
"""
    for f in ["vm_input", "vm_input_size"]:
        c = re.sub(r"(\b%s\(struct machine \*M\) \{\n)" % f, r"\1    (void) M;\n", c)
    ops = variables(calls_in(ops))
    open(os.path.join(folder, "core.c"), "w").write(c)
    open(os.path.join(folder, "ops.h"), "w").write(ops)

    h = open(os.path.join(CHAPTER, "host.c")).read()
    for f in ["vm_input", "vm_input_size", "vm_reset", "vm_run"]:
        h = h.replace("%s(void);" % f, "%s(void *M);" % f)
    h = patch(h, "const char *vm_load(int size);", "const char *vm_load(void *M, int size);")
    h = patch(h, "void vm_set_collector(int copying, int stressed);",
              "void vm_set_collector(void *M, int copying, int stressed);\nvoid *vm_machine(void);")
    h = patch(h, "    FILE *f;\n", "    FILE *f;\n    void *M = vm_machine();\n")
    for f in ["vm_input", "vm_input_size", "vm_reset", "vm_run"]:
        h = h.replace("%s()" % f, "%s(M)" % f)
    h = patch(h, "vm_load(size)", "vm_load(M, size)")
    h = patch(h, "vm_set_collector(copying, stressed)", "vm_set_collector(M, copying, stressed)")
    open(os.path.join(folder, "host.c"), "w").write(h)

    js = open(os.path.join(CHAPTER, "web", "machine.js")).read()
    js = patch(js, "        m.vm = instance.exports;\n",
               "        m.vm = instance.exports;\n        m.M = m.vm.vm_machine();\n")
    js = re.sub(r"\b(this\.vm|v)\.(vm_\w+)\(\)", r"\1.\2(this.M)", js)
    js = re.sub(r"\b(this\.vm|v)\.(vm_\w+)\((?!this\.M)", r"\1.\2(this.M, ", js)
    os.makedirs(os.path.join(folder, "web"), exist_ok=True)
    open(os.path.join(folder, "web", "machine.js"), "w").write(js)
    shutil.copy(os.path.join(CHAPTER, "run.mjs"), folder)


RUN_OLD = """// Run in slices, so that a program that never ends does not freeze
// the page, and Stop can be pressed.
function run() {
    running = true;
    enable();
    const slice = () => {
        if (!running) return;
        try {
            for (let i = 0; i < 200000; i++) {
                if (!machine.step()) {
                    running = false;
                    ready = false;
                    setStatus("Halted.");
                    show();
                    enable();
                    return;
                }
            }
            setStatus("Running...");
            requestAnimationFrame(slice);
        } catch (e) {
            trapped(e);
        }
    };
    slice();
}"""

RUN_NEW = """// Run in slices, so that a program that never ends does not freeze
// the page, and Stop can be pressed. Exercise 23.3: a slice is about
// SLICE_MS milliseconds of running, not 200,000 instructions, and the next
// starts as soon as the browser has done what it had waiting, by a message
// this page sends itself, not at the next frame. ?slices=frames in the
// address gives the old way, to compare; ?ms=n sets SLICE_MS.
const settings = new URLSearchParams(location.search);
const SLICE_MS = Number(settings.get("ms") || 10);
const BY_FRAMES = settings.get("slices") === "frames";
const channel = new MessageChannel();
let next = null;
channel.port1.onmessage = () => next();
function soon(f) {
    next = f;
    channel.port2.postMessage(0);
}

function halt() {
    running = false;
    ready = false;
    setStatus("Halted.");
    show();
    enable();
}

function run() {
    running = true;
    enable();
    let first = true;              // a breakpoint where Run starts does not stop it
    const watching = breaks.size > 0;
    const slice = () => {
        if (!running) return;
        try {
            if (BY_FRAMES) {
                for (let i = 0; i < 200000; i++)
                    if (!machine.step()) return halt();
                setStatus("Running...");
                requestAnimationFrame(slice);
                return;
            }
            const end = performance.now() + SLICE_MS;
            do {
                for (let i = 0; i < 1000; i++) {
                    // Exercise 23.1: stop before an instruction with a breakpoint.
                    if (watching && !first && breaks.has(machine.vm.vm_pc())) {
                        running = false;
                        setStatus(`Stopped at the breakpoint at ${machine.vm.vm_pc()}.`);
                        show();
                        enable();
                        return;
                    }
                    first = false;
                    if (!machine.step()) return halt();
                }
            } while (performance.now() < end);
            setStatus("Running...");
            soon(slice);
        } catch (e) {
            trapped(e);
        }
    };
    slice();
}"""

LISTING_OLD = """        div.append(addr, text[k].replace(/\\s*[;#].*$/, "").trimEnd() || text[k].trim());
        listing.append(div);"""

LISTING_NEW = """        div.append(addr, text[k].replace(/\\s*[;#].*$/, "").trimEnd() || text[k].trim());
        if (line.size > 0) {
            div.classList.toggle("break", breaks.has(line.address));
            div.onclick = () => {
                if (breaks.has(line.address)) breaks.delete(line.address);
                else breaks.add(line.address);
                div.classList.toggle("break", breaks.has(line.address));
            };
        }
        listing.append(div);"""

CSS = """#listing div.break .addr { color: var(--red); font-weight: 700; }
#listing div.break .addr::before { content: "\\25CF"; margin-right: .5ch; }
#listing div:has(.addr:not(:empty)) { cursor: pointer; }
#listing .here {"""


def web(folder):
    a = open(os.path.join(CHAPTER, "web", "app.js")).read()
    a = patch(a, "let running = false;\n", "let running = false;\n"
              "// Exercise 23.1: the addresses with a breakpoint. Click a line of the\n"
              "// listing to set one, and again to take it away.\n"
              "const breaks = new Set();\n"
              "let assembled = null;\n")
    a = patch(a, LISTING_OLD, LISTING_NEW)
    a = patch(a, "    const result = assemble(source.value);\n    lines = result.lines;\n",
              "    const result = assemble(source.value);\n    lines = result.lines;\n"
              "    if (source.value !== assembled) breaks.clear();     // its addresses have changed\n"
              "    assembled = source.value;\n")
    a = patch(a, RUN_OLD, RUN_NEW)
    h = open(os.path.join(CHAPTER, "web", "index.html")).read()
    h = patch(h, "#listing .here {", CSS)
    h = patch(h, "<p>The machine of chapter 23, compiled to WebAssembly, running in this page.</p>",
              "<p>The machine of chapter 23, compiled to WebAssembly, running in this page."
              " Click a line of the listing for a breakpoint.</p>")
    os.makedirs(folder, exist_ok=True)
    open(os.path.join(folder, "app.js"), "w").write(a)
    open(os.path.join(folder, "index.html"), "w").write(h)
    for f in ["asm.js", "machine.js", "vm.wasm"]:
        shutil.copy(os.path.join(CHAPTER, "web", f), folder)


def main():
    what, folder = sys.argv[1], sys.argv[2]
    os.makedirs(folder, exist_ok=True)
    {"loop": loop, "state": state, "web": web}[what](folder)


main()
