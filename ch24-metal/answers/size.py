#!/usr/bin/env python3
"""
Exercise 24.3: how big the divider is, by Yosys, for an iCE40.

cpu.v cannot be synthesised as it stands and say anything. Its code
memory is filled by the testbench, from outside, so to Yosys the program
is a constant, every instruction falls away, and what is left is 68
cells. Its memories, 64K words of code and 4096 of data cleared at
reset, a stack read at three places at once, would be flip-flops on an
iCE40, far more than the chip has. So it is measured two ways:

  units   the divider alone, beside an adder and a multiplier, each
          32 bits: b / c and b % c in one cycle, as cpu.v has them, and
          the 32-cycle divider of build.py div, as a module of its own
  cpu     the CPU itself, given a port to write its code and memories of
          16 words, so that it fits: as it is, and with build.py's
          32-cycle divider in place of / and %

For each, the iCE40's cells (LUT4, carry, flip-flops) and the length of
the longest path, in cells, carries among them, from Yosys's ltp -noff:
a flip-flop ends a path, so for the 32-cycle divider it is one cycle's.

    python3 size.py [units|cpu]     (both if not given; cpu takes minutes)

Needs Yosys on the PATH.
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from build import div, patch  # noqa: E402

UNITS = {
    "add": """module add(input signed [31:0] b, c, output signed [31:0] s);
    assign s = b + c;
endmodule""",
    "mul": """module mul(input signed [31:0] b, c, output signed [31:0] p);
    assign p = b * c;
endmodule""",
    "div, one cycle": """module divide(input signed [31:0] b, c, output signed [31:0] q, r);
    assign q = b / c;
    assign r = b % c;
endmodule""",
    # The divider of build.py div, the same lines, on its own: start
    # loads it, and 32 cycles later done is 1, with both results.
    "div, 32 cycles": """module divide32(input clock, input start, input signed [31:0] b, c,
                output reg done, output signed [31:0] q, r);
    reg  [5:0] bit_left;
    reg [31:0] quotient, remainder, divisor_m, dividend_m;
    reg        negative_q, negative_r, dividing;
    wire [32:0] trial = {remainder[30:0], dividend_m[bit_left - 1]} - {1'b0, divisor_m};
    assign q = negative_q ? -quotient : quotient;
    assign r = negative_r ? -remainder : remainder;
    always @(posedge clock) begin
        done <= 0;
        if (start) begin
            dividing <= 1;
            bit_left <= 32;
            quotient <= 0;
            remainder <= 0;
            dividend_m <= b < 0 ? -b : b;
            divisor_m <= c < 0 ? -c : c;
            negative_q <= (b < 0) != (c < 0);
            negative_r <= b < 0;
        end else if (dividing) begin
            if (bit_left != 0) begin
                if (!trial[32]) begin
                    remainder <= trial[31:0];
                    quotient <= {quotient[30:0], 1'b1};
                end else begin
                    remainder <= {remainder[30:0], dividend_m[bit_left - 1]};
                    quotient <= {quotient[30:0], 1'b0};
                end
                bit_left <= bit_left - 1;
            end else begin
                dividing <= 0;
                done <= 1;
            end
        end
    end
endmodule""",
}


def fit(cpu):
    """cpu.v with a port to write its code, and memories of 16 words."""
    cpu = patch(cpu, "    input  wire        [31:0] code_len,\n",
                "    input  wire        [31:0] code_len,\n"
                "    input  wire               code_write,\n"
                "    input  wire         [3:0] code_address,\n"
                "    input  wire signed [31:0] code_word,\n")
    cpu = patch(cpu, "    always @(posedge clock) begin\n",
                "    always @(posedge clock) begin\n"
                "        if (code_write) code[code_address] <= code_word;\n")
    cpu = patch(cpu, "localparam STACK_SIZE = 256, FRAMES = 256, MEMORY_SIZE = 4096;",
                "localparam STACK_SIZE = 16, FRAMES = 16, MEMORY_SIZE = 16;")
    return cpu.replace("parameter CODE_SIZE = 65536", "parameter CODE_SIZE = 16")


def synthesise(verilog, top, work):
    source = os.path.join(work, top + ".v")
    open(source, "w").write(verilog)
    stat, ltp = os.path.join(work, top + ".stat"), os.path.join(work, top + ".ltp")
    subprocess.run(["yosys", "-q", "-p",
                    f"read_verilog -sv {source}; synth_ice40 -top {top}; "
                    f"tee -q -o {stat} stat; tee -q -o {ltp} ltp -noff"],
                   check=True, capture_output=True)
    text = open(stat).read()

    def count(cell):
        m = re.search(r"^\s*(\d+)\s+" + cell + r"\s*$", text, re.M)
        return int(m.group(1)) if m else 0
    flops = sum(int(n) for n in re.findall(r"^\s*(\d+)\s+SB_DFF\w*\s*$", text, re.M))
    levels = re.search(r"Longest topological path in \S+ \(length=(\d+)\)", open(ltp).read())
    return count("SB_LUT4"), count("SB_CARRY"), flops, int(levels.group(1)) if levels else 0


def report(rows):
    print(f"{'':16} {'LUT4':>6} {'carry':>6} {'flops':>6} {'levels':>7}")
    for name, (lut, carry, flops, levels) in rows:
        print(f"{name:16} {lut:6} {carry:6} {flops:6} {levels:7}")


def main():
    which = sys.argv[1:] or ["units", "cpu"]
    with tempfile.TemporaryDirectory() as work:
        if "units" in which:
            rows = []
            for name, verilog in UNITS.items():
                top = re.match(r"module (\w+)", verilog).group(1)
                rows.append((name, synthesise(verilog, top, work)))
            report(rows)
        if "cpu" in which:
            cpu = open(os.path.join(CHAPTER, "cpu.v")).read()
            tb = open(os.path.join(CHAPTER, "tb.v")).read()
            rows = [("cpu, / and %", synthesise(fit(cpu), "cpu", work)),
                    ("cpu, 32 cycles", synthesise(fit(div(cpu, tb)[0]), "cpu", work))]
            if "units" in which:
                print()
            report(rows)


if __name__ == "__main__":
    main()
