#!/usr/bin/env python3
"""
vrun.py, for the variants of answers/build.py: the first argument is the
folder that holds the variant's sim. With -t, the testbench of build.py
trace writes the stack after every instruction on stderr.

Run a .vm file on the CPU of cpu.v, in simulation, as if it were a
machine like the others: what the program prints goes to standard
output, a trap message to standard error, and the exit status is the
specification's. Then the conformance suite can test the hardware.

A damaged file is reported exactly as the machine reports it, before
any simulation starts.

    usage: vrun_more.py folder [-c] [-t] program.vm

-c prints the number of clock cycles the program took, on stderr.
"""

import os
import subprocess
import sys
import tempfile


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
FOLDER = sys.argv.pop(1) if len(sys.argv) > 1 else ""

import vmfile  # noqa: E402


def main():
    args = sys.argv[1:]
    cycles = "-c" in args
    tracing = "-t" in args
    args = [a for a in args if a not in ("-c", "-t")]
    if len(args) != 1:
        sys.exit("usage: vrun_more.py folder [-c] [-t] program.vm")
    path = args[0]
    try:
        code = vmfile.read(path)
    except OSError:
        print(f"{path}: cannot open", file=sys.stderr)
        sys.exit(2)
    except vmfile.FormatError as e:
        print(f"{path}: {e}", file=sys.stderr)
        sys.exit(2)
    with tempfile.TemporaryDirectory() as work:
        hexfile = os.path.join(work, "program.hex")
        with open(hexfile, "w") as f:
            for word in code:
                f.write(f"{word & 0xffffffff:08x}\n")
        p = subprocess.run(["vvp", "-n", os.path.join(FOLDER, "sim"),
                            f"+program={hexfile}", f"+length={len(code)}"]
                           + (["+trace"] if tracing else []),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sys.stdout.buffer.write(p.stdout)
    sys.stdout.buffer.flush()
    status = 3
    for line in p.stderr.decode("latin-1").splitlines():
        if line.startswith("status "):
            status = int(line.split()[1])
        elif line.startswith(("cycles ", "fused ")) and not cycles:
            continue
        else:
            print(line, file=sys.stderr)
    sys.exit(status)


if __name__ == "__main__":
    main()
