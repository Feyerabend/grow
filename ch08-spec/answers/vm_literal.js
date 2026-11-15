#!/usr/bin/env node
// Exercise 8.1: a third machine, in JavaScript, written from SPEC.md and
// ch05-files/FORMAT.md. Section numbers below are the specification's.
//
//     node vm.js program.vm

"use strict";
const fs = require("fs");

let out = "";                               // standard output, written out in order
function flush() {
    if (out.length) fs.writeSync(1, out);
    out = "";
}
function stop(status, message) {
    flush();
    if (message !== undefined) fs.writeSync(2, message + "\n");
    process.exit(status);
}

// 7. Program files, checked in the order the specification lists them.
function load(path) {
    let data;
    try {
        data = fs.readFileSync(path);
    } catch (e) {
        stop(2, `${path}: cannot open`);
    }
    if (data.length < 8) stop(2, `${path}: too short to be a program`);
    if (data[0] !== 0x53 || data[1] !== 0x56 || data[2] !== 0x4d)
        stop(2, `${path}: not a program (wrong magic number)`);
    if (data[3] !== 1) stop(2, `${path}: unknown format version`);
    const n = data.readInt32LE(4);
    if (n < 1 || n > 65536) stop(2, `${path}: bad code length`);
    if (data.length < 8 + 4 * n) stop(2, `${path}: code ends early`);
    if (data.length > 8 + 4 * n) stop(2, `${path}: extra bytes after the code`);
    const code = [];
    for (let i = 0; i < n; i++) code.push(data.readInt32LE(8 + 4 * i));
    return code;
}

function run(code) {
    // 2. The state of the machine.
    let pc = 0, fp = 0, start = 0;
    const stack = [], frames = [];

    const trap = (reason) => stop(1, `trap: ${reason} at ${start}`);
    const isAddress = (a) => a >= 0 && a < code.length;
    // 4. Basic operations.
    const operand = () => {
        if (!isAddress(pc)) trap("missing operand");
        return code[pc++];
    };
    const address = () => {
        const t = operand();
        if (!isAddress(t)) trap("jump out of program");
        return t;
    };
    const push = (v) => {
        if (stack.length === 256) trap("stack overflow");
        stack.push(v | 0);                      // 1. Values: wrapped to 32 bits
    };
    const pop = () => {
        if (stack.length === fp) trap("stack underflow");
        return stack.pop();
    };
    const local = (k) => {
        if (k < 0 || fp + k >= stack.length) trap("no such local");
        return fp + k;
    };

    // 3. Running.
    for (;;) {
        // Step 1 traps before step 2 sets start, so start is still that of
        // the instruction before: the specification does not say. Here it
        // is taken to be pc, the place the machine ran off to.
        if (!isAddress(pc)) trap("ran off the end of the program");
        start = pc;
        const op = code[pc++];
        let a, b, c, t, n, k;
        switch (op) {
        case 0: stop(0); break;                                     // HALT
        case 1: push(operand()); break;                             // PUSH
        case 2: b = pop(); a = pop(); push(a + b); break;           // ADD
        case 3: b = pop(); a = pop(); push(a - b); break;           // SUB
        case 4: b = pop(); a = pop(); push(Math.imul(a, b)); break; // MUL
        case 5: a = pop(); out += a + "\n"; break;                  // PRINT
        case 6: pc = address(); break;                              // JMP
        case 7: t = address(); a = pop(); if (a === 0) pc = t; break;   // JZ
        case 8: a = pop(); push(a); push(a); break;                 // DUP
        case 9: pop(); break;                                       // DROP
        case 10: b = pop(); a = pop(); push(b); push(a); break;     // SWAP
        case 11: b = pop(); a = pop(); push(a); push(b); push(a); break;   // OVER
        case 12: c = pop(); b = pop(); a = pop(); push(b); push(c); push(a); break;  // ROT
        case 13: b = pop(); a = pop(); push(a < b ? 1 : 0); break;  // LT
        case 14: b = pop(); a = pop(); push(a === b ? 1 : 0); break;    // EQ
        case 15: k = operand(); push(stack[local(k)]); break;       // LOAD
        case 16: k = operand(); a = pop(); stack[local(k)] = a; break;  // STORE
        case 17:                                                    // CALL
            t = address();
            n = operand();
            if (n < 0 || stack.length - fp < n) trap("not enough arguments");
            if (frames.length === 256) trap("too many nested calls");
            frames.push([pc, fp]);
            fp = stack.length - n;
            pc = t;
            break;
        case 18:                                                    // RET
            if (frames.length === 0) trap("return without call");
            a = pop();
            stack.length = fp;
            [pc, fp] = frames.pop();
            push(a);
            break;
        case 19:                                                    // DIV
            b = pop(); a = pop();
            if (b === 0) trap("division by zero");
            push(Math.trunc(a / b));
            break;
        case 20:                                                    // MOD
            b = pop(); a = pop();
            if (b === 0) trap("division by zero");
            push(a - Math.imul(b, Math.trunc(a / b) | 0));
            break;
        default:
            trap("unknown instruction");
        }
    }
}

if (process.argv.length !== 3) stop(2, "usage: node vm.js program.vm");
run(load(process.argv[2]));
