#!/usr/bin/env python3
"""
Make the variants of cpu.v and tb.v for chapter 24's exercises, each in a
folder of its own, compiled by Icarus Verilog to folder/sim:

    python3 build.py heap folder     exercise 1: NEW, GETF, SETF, LEN, tags
    python3 build.py pipe folder     exercise 2: fetch and execute overlapped
    python3 build.py div folder      exercise 3: DIV and MOD in 32 cycles
    python3 build.py trace folder    exercise 4: the stack after every instruction
    python3 build.py pair folder     exercise 5: LOAD and ADD in one cycle

Run a program on one with  python3 vrun_more.py folder [-c] program.vm.
Each is made by changing the text of cpu.v and tb.v, every change checked
to apply exactly once.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)


def patch(text, old, new, count=1):
    assert text.count(old) == count, (old, text.count(old))
    return text.replace(old, new)


def heap(cpu, tb):
    """Version 3: a value is 33 bits, the 33rd its tag, 1 for a reference.
    The heap is never collected, as in chapter 13, and is all 0 from reset,
    so NEW need not clear the fields of a block, since no place is used
    twice."""
    cpu = patch(cpu, "RET = 18, DIV = 19, MOD = 20, AND = 21, OR = 22, XOR = 23,\n"
                     "               LOADM = 24, STOREM = 25, EMIT = 26;",
                "RET = 18, DIV = 19, MOD = 20, AND = 21, OR = 22, XOR = 23,\n"
                "               LOADM = 24, STOREM = 25, EMIT = 26,\n"
                "               NEW = 27, GETF = 28, SETF = 29, LEN = 30;")
    cpu = patch(cpu, "               T_CHAR = 13;",
                "               T_CHAR = 13, T_NUMBER = 14, T_REFERENCE = 15, T_BOUNDS = 16,\n"
                "               T_SIZE = 17, T_MEMORY_FULL = 18;")
    cpu = patch(cpu, "output reg          [3:0] trap_reason,", "output reg          [4:0] trap_reason,")
    cpu = patch(cpu, "task automatic stop(input [3:0] reason);", "task automatic stop(input [4:0] reason);")
    cpu = patch(cpu, "localparam STACK_SIZE = 256, FRAMES = 256, MEMORY_SIZE = 4096;",
                "localparam STACK_SIZE = 256, FRAMES = 256, MEMORY_SIZE = 4096,\n"
                "               HEAP_SIZE = 65536, HEADER = 2;")
    # Values: 33 bits, tag on top.
    cpu = patch(cpu, "    reg signed [31:0] stack  [0:STACK_SIZE-1];",
                "    reg        [32:0] stack  [0:STACK_SIZE-1];   // bit 32: 1 for a reference")
    cpu = patch(cpu, "    reg signed [31:0] memory [0:MEMORY_SIZE-1];",
                "    reg        [32:0] memory [0:MEMORY_SIZE-1];\n"
                "    reg        [32:0] heap   [0:HEAP_SIZE-1];    // never collected\n"
                "    reg        [31:0] heap_used, blocks_made;")
    cpu = patch(cpu, """    wire signed [31:0] c = stack[sp - 1];
    wire signed [31:0] b = stack[sp - 2];
    wire signed [31:0] a = stack[sp - 3];""", """    wire        [32:0] c = stack[sp - 1];
    wire        [32:0] b = stack[sp - 2];
    wire        [32:0] a = stack[sp - 3];
    // Their numbers, and whether each is a reference.
    wire signed [31:0] cn = c[31:0], bn = b[31:0];
    wire c_ref = c[32], b_ref = b[32], a_ref = a[32];
    // A number as a value, and a reference.
    function automatic [32:0] number(input [31:0] n);
        number = {1'b0, n};
    endfunction
    function automatic [32:0] reference(input [31:0] n);
        reference = {1'b1, n};
    endfunction""")
    cpu = patch(cpu, """            for (i = 0; i < MEMORY_SIZE; i = i + 1)
                memory[i] <= 0;""", """            for (i = 0; i < MEMORY_SIZE; i = i + 1)
                memory[i] <= 0;
            for (i = 0; i < HEAP_SIZE; i = i + 1)
                heap[i] <= 0;
            heap_used <= 0;
            blocks_made <= 0;""")
    cpu = patch(cpu, """                    stack[sp] <= arg1;
                    sp <= sp + 1;
                    pc <= pc + 2;""", """                    stack[sp] <= number(arg1);
                    sp <= sp + 1;
                    pc <= pc + 2;""")
    cpu = patch(cpu, """                else if ((op == DIV || op == MOD) && c == 0)
                    stop(T_DIVZERO);
                else begin
                    case (op)
                    ADD: stack[sp - 2] <= b + c;
                    SUB: stack[sp - 2] <= b - c;
                    MUL: stack[sp - 2] <= b * c;
                    AND: stack[sp - 2] <= b & c;
                    OR:  stack[sp - 2] <= b | c;
                    XOR: stack[sp - 2] <= b ^ c;
                    LT:  stack[sp - 2] <= b < c;
                    EQ:  stack[sp - 2] <= b == c;
                    DIV: stack[sp - 2] <= b / c;
                    MOD: stack[sp - 2] <= b % c;
                    endcase""", """                else if (op != EQ && (b_ref || c_ref)) stop(T_NUMBER);
                else if ((op == DIV || op == MOD) && cn == 0) stop(T_DIVZERO);
                else begin
                    case (op)
                    ADD: stack[sp - 2] <= number(bn + cn);
                    SUB: stack[sp - 2] <= number(bn - cn);
                    MUL: stack[sp - 2] <= number(bn * cn);
                    AND: stack[sp - 2] <= number(bn & cn);
                    OR:  stack[sp - 2] <= number(bn | cn);
                    XOR: stack[sp - 2] <= number(bn ^ cn);
                    LT:  stack[sp - 2] <= number(bn < cn);
                    EQ:  stack[sp - 2] <= number(b == c);     // the tags too
                    DIV: stack[sp - 2] <= number(bn / cn);
                    MOD: stack[sp - 2] <= number(bn % cn);
                    endcase""")
    cpu = patch(cpu, """                if (room < 1) stop(T_UNDERFLOW);
                else begin
                    print_valid <= 1;
                    print_value <= c;""", """                if (room < 1) stop(T_UNDERFLOW);
                else if (c_ref) stop(T_NUMBER);
                else begin
                    print_valid <= 1;
                    print_value <= cn;""")
    cpu = patch(cpu, """                else if (c < 0 || c > 255) stop(T_CHAR);
                else begin
                    emit_valid <= 1;
                    emit_char <= c[7:0];""", """                else if (c_ref) stop(T_NUMBER);
                else if (cn < 0 || cn > 255) stop(T_CHAR);
                else begin
                    emit_valid <= 1;
                    emit_char <= c[7:0];""")
    cpu = patch(cpu, """                else if (c < 0 || c >= MEMORY_SIZE) stop(T_MEMORY);
                else begin
                    stack[sp - 1] <= memory[c];""", """                else if (c_ref) stop(T_NUMBER);
                else if (cn < 0 || cn >= MEMORY_SIZE) stop(T_MEMORY);
                else begin
                    stack[sp - 1] <= memory[cn];""")
    cpu = patch(cpu, """                else if (b < 0 || b >= MEMORY_SIZE) stop(T_MEMORY);
                else begin
                    memory[b] <= c;""", """                else if (b_ref) stop(T_NUMBER);
                else if (bn < 0 || bn >= MEMORY_SIZE) stop(T_MEMORY);
                else begin
                    memory[bn] <= c;""")
    cpu = patch(cpu, """            default:
                stop(T_UNKNOWN);""", """            // The heap, of chapter 13: a block of n fields is n + 2 places,
            // its length and its number, then the fields.
            NEW:
                if (room < 1) stop(T_UNDERFLOW);
                else if (c_ref) stop(T_NUMBER);
                else if (cn < 0) stop(T_SIZE);
                else if (cn > $signed(HEAP_SIZE - HEADER - heap_used)) stop(T_MEMORY_FULL);
                else begin
                    heap[heap_used] <= number(cn);
                    heap[heap_used + 1] <= number(blocks_made + 1);
                    blocks_made <= blocks_made + 1;
                    stack[sp - 1] <= reference(heap_used);
                    heap_used <= heap_used + HEADER + cn;
                    pc <= pc + 1;
                end
            GETF:                                   // v w -> v.w
                if (room < 2) stop(T_UNDERFLOW);
                else if (!b_ref) stop(T_REFERENCE);
                else if (c_ref) stop(T_NUMBER);
                else if (cn < 0 || cn >= $signed(heap[bn][31:0])) stop(T_BOUNDS);
                else begin
                    stack[sp - 2] <= heap[bn + HEADER + cn];
                    sp <= sp - 1;
                    pc <= pc + 1;
                end
            SETF:                                   // v w u -> ; v.w = u
                if (room < 3) stop(T_UNDERFLOW);
                else if (!a_ref) stop(T_REFERENCE);
                else if (b_ref) stop(T_NUMBER);
                else if (bn < 0 || bn >= $signed(heap[a[31:0]][31:0])) stop(T_BOUNDS);
                else begin
                    heap[a[31:0] + HEADER + bn] <= c;
                    sp <= sp - 3;
                    pc <= pc + 1;
                end
            LEN:
                if (room < 1) stop(T_UNDERFLOW);
                else if (!c_ref) stop(T_REFERENCE);
                else begin
                    stack[sp - 1] <= number(heap[cn][31:0]);
                    pc <= pc + 1;
                end
            default:
                stop(T_UNKNOWN);""")
    tb = patch(tb, "    wire [3:0] trap_reason;", "    wire [4:0] trap_reason;")
    tb = patch(tb, """                13: $fdisplay(STDERR, "trap: not a character at %0d", trap_at);""",
               """                13: $fdisplay(STDERR, "trap: not a character at %0d", trap_at);
                14: $fdisplay(STDERR, "trap: not a number at %0d", trap_at);
                15: $fdisplay(STDERR, "trap: not a reference at %0d", trap_at);
                16: $fdisplay(STDERR, "trap: index out of bounds at %0d", trap_at);
                17: $fdisplay(STDERR, "trap: bad size at %0d", trap_at);
                18: $fdisplay(STDERR, "trap: out of memory at %0d", trap_at);""")
    return cpu, tb


def pipe(cpu, tb):
    """Fetch and execute overlapped. The instruction to execute, its code and
    two words after it, is held in registers, fetched the cycle before. While
    it executes, the next one is fetched: from the address just after it, the
    only one known before it has run. If it jumps, calls or returns, that
    guess is wrong, and the next cycle executes nothing, a bubble, while the
    instruction at the new address is fetched."""
    cpu = patch(cpu, """    wire signed [31:0] op   = code[pc];
    wire signed [31:0] arg1 = code[pc + 1];
    wire signed [31:0] arg2 = code[pc + 2];""", """    // Exercise 24.2: the instruction at pc, fetched the cycle before; valid
    // is 0 in a bubble, when nothing has been fetched for pc yet.
    reg signed [31:0] op, arg1, arg2;
    reg valid;
    reg [31:0] npc;                             // where execution goes next
    // How many words the instruction takes, and so where the next begins.
    wire [31:0] size = (op == PUSH || op == JMP || op == JZ || op == LOAD || op == STORE) ? 2
                     : op == CALL ? 3 : 1;
    wire [31:0] seq = pc + size;""")
    cpu = patch(cpu, """            halted <= 0;
            trapped <= 0;""", """            halted <= 0;
            trapped <= 0;
            valid <= 0;""")
    cpu = patch(cpu, """        end else if (!halted && !trapped) begin
            if (pc >= code_len)
                stop(T_RUNOFF);
            else case (op)""", """        end else if (!halted && !trapped && !valid) begin
            // A bubble: fetch the instruction at pc.
            op <= code[pc];
            arg1 <= code[pc + 1];
            arg2 <= code[pc + 2];
            valid <= 1;
        end else if (!halted && !trapped) begin
            npc = pc;
            if (pc >= code_len)
                stop(T_RUNOFF);
            else case (op)""")
    # Inside the case, the new pc is worked out first, and used at the end.
    head, rest = cpu.split("            else case (op)", 1)
    body, tail = rest.split("            endcase\n        end\n    end", 1)
    body = re.sub(r"\bpc <= ", "npc = ", body)
    cpu = head + "            else case (op)" + body + """            endcase
            pc <= npc;
            if (npc == seq) begin
                // Straight on: the next instruction is the one fetched now.
                op <= code[seq];
                arg1 <= code[seq + 1];
                arg2 <= code[seq + 2];
            end else
                valid <= 0;                     // a jump: the next cycle is a bubble
        end
    end""" + tail
    return cpu, tb


def div(cpu, tb):
    """DIV and MOD by shifting and subtracting, one bit a cycle: 32 cycles
    more, on the magnitudes, the signs put back at the end, rounding toward
    zero as C does. The machine waits while the divider works."""
    cpu = patch(cpu, "    integer i;\n", """    integer i;

    // Exercise 24.3: a divider that takes 32 cycles.
    reg        dividing;
    reg  [5:0] bit_left;
    reg [31:0] quotient, remainder, divisor_m, dividend_m;
    reg        negative_q, negative_r;
    wire [32:0] trial = {remainder[30:0], dividend_m[bit_left - 1]} - {1'b0, divisor_m};
""")
    cpu = patch(cpu, """            halted <= 0;
            trapped <= 0;""", """            halted <= 0;
            trapped <= 0;
            dividing <= 0;""")
    cpu = patch(cpu, """        end else if (!halted && !trapped) begin""", """        end else if (dividing) begin
            if (bit_left != 0) begin
                // One bit of the quotient: shift the next bit of the dividend
                // into the remainder, and subtract the divisor if it fits.
                if (!trial[32]) begin
                    remainder <= trial[31:0];
                    quotient <= {quotient[30:0], 1'b1};
                end else begin
                    remainder <= {remainder[30:0], dividend_m[bit_left - 1]};
                    quotient <= {quotient[30:0], 1'b0};
                end
                bit_left <= bit_left - 1;
            end else begin
                if (op == DIV)
                    stack[sp - 2] <= negative_q ? -quotient : quotient;
                else
                    stack[sp - 2] <= negative_r ? -remainder : remainder;
                sp <= sp - 1;
                pc <= pc + 1;
                dividing <= 0;
            end
        end else if (!halted && !trapped) begin""")
    cpu = patch(cpu, """                    DIV: stack[sp - 2] <= b / c;
                    MOD: stack[sp - 2] <= b % c;
                    endcase
                    sp <= sp - 1;
                    pc <= pc + 1;""", """                    endcase
                    if (op == DIV || op == MOD) begin
                        dividing <= 1;
                        bit_left <= 32;
                        quotient <= 0;
                        remainder <= 0;
                        dividend_m <= b < 0 ? -b : b;
                        divisor_m <= c < 0 ? -c : c;
                        negative_q <= (b < 0) != (c < 0);
                        negative_r <= b < 0;
                    end else begin
                        sp <= sp - 1;
                        pc <= pc + 1;
                    end""")
    return cpu, tb


def trace(cpu, tb):
    """With +trace, after every instruction that ran, the testbench writes
    its number, its address and the stack, with | where each frame's locals
    begin, as the C machine's -t does, on standard error."""
    tb = patch(tb, "    reg [63:0] cycles = 0;\n", """    reg [63:0] cycles = 0;
    reg tracing = 0;
    reg [31:0] at = 0;                  // the address of the instruction running
    reg [63:0] steps = 0;
    integer i, f;
    reg first;
""")
    tb = patch(tb, """        if (!$value$plusargs("limit=%d", limit))""", """        tracing = $test$plusargs("trace");
        if (!$value$plusargs("limit=%d", limit))""")
    tb = patch(tb, """    always @(negedge clock) if (!reset) begin
        if (print_valid)""", """    always @(negedge clock) if (!reset) begin
        if (tracing && !trapped && cycles > 0) begin     // the first falling edge is before any
            steps = steps + 1;
            $fwrite(STDERR, "%0d %0d", steps, at);
            f = 1;
            for (i = 0; i <= machine.sp; i = i + 1) begin
                while (f <= machine.fsp && (f < machine.fsp ? machine.saved[f] : machine.fp) == i) begin
                    $fwrite(STDERR, " |");
                    f = f + 1;
                end
                if (i < machine.sp)
                    $fwrite(STDERR, " %0d", machine.stack[i]);
            end
            $fwrite(STDERR, "\\n");
        end
        at = machine.pc;
        if (print_valid)""")
    return cpu, tb


def pair(cpu, tb):
    """LOAD k and the ADD after it, in one cycle, as the NC4016 joined
    instructions: found while running, when the word after LOAD's operand is
    ADD. LOAD's checks are made, and if one fails it traps, as LOAD; ADD
    cannot fail after a LOAD that did not, since the frame then holds two
    values. Nothing is pushed: the local is added to the value on top. A
    jump to the ADD itself still runs it alone."""
    cpu = patch(cpu, "    integer i;\n", """    integer i;
    reg [63:0] fused = 0;                       // how many times, for -c
""")
    cpu = patch(cpu, """            LOAD:
                if (after < 1) stop(T_OPERAND);
                else if (arg1 < 0 || fp + arg1 >= sp) stop(T_LOCAL);
                else if (sp == STACK_SIZE) stop(T_OVERFLOW);
                else begin""", """            LOAD:
                if (after < 1) stop(T_OPERAND);
                else if (arg1 < 0 || fp + arg1 >= sp) stop(T_LOCAL);
                else if (sp == STACK_SIZE) stop(T_OVERFLOW);
                else if (after >= 2 && arg2 == ADD) begin
                    // Exercise 24.5: LOAD k, ADD as one.
                    stack[sp - 1] <= c + stack[fp + arg1];
                    pc <= pc + 3;
                    fused <= fused + 1;
                end else begin""")
    tb = patch(tb, """            $fdisplay(STDERR, "cycles %0d", cycles);
            $fdisplay(STDERR, "status 0");""", """            $fdisplay(STDERR, "cycles %0d", cycles);
            $fdisplay(STDERR, "fused %0d", machine.fused);
            $fdisplay(STDERR, "status 0");""")
    return cpu, tb


def main():
    what, folder = sys.argv[1], sys.argv[2]
    os.makedirs(folder, exist_ok=True)
    cpu = open(os.path.join(CHAPTER, "cpu.v")).read()
    tb = open(os.path.join(CHAPTER, "tb.v")).read()
    cpu, tb = {"heap": heap, "pipe": pipe, "div": div, "trace": trace, "pair": pair}[what](cpu, tb)
    open(os.path.join(folder, "cpu.v"), "w").write(cpu)
    open(os.path.join(folder, "tb.v"), "w").write(tb)
    subprocess.run(["iverilog", "-g2012", "-Wall", "-o", os.path.join(folder, "sim"),
                    os.path.join(folder, "tb.v"), os.path.join(folder, "cpu.v")], check=True)


if __name__ == "__main__":
    main()
