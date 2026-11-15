"""
Exercise D.2: the copy loop for the 6502 alone, run on a simulator of
just the nine instructions it uses. The two pointers and the count are
each two bytes in the first page: SRC at 00, DST at 02, CNT at 04, low
byte first. The opcodes are from the 6502's instruction table at
masswerk.at/6502/6502_instruction_set.html.

    python3 copy6502.py
"""

LOOP = bytes.fromhex(
    "B1 00"     # loop: LDA (SRC),Y   A := the byte SRC points at (Y is 0)
    "91 02"     #       STA (DST),Y   the byte DST points at := A
    "E6 00"     #       INC SRC       SRC + 1, low byte
    "D0 02"     #       BNE +2        no carry: skip the next
    "E6 01"     #       INC SRC+1     the carry, into the high byte
    "E6 02"     #       INC DST
    "D0 02"     #       BNE +2
    "E6 03"     #       INC DST+1
    "A5 04"     #       LDA CNT       CNT - 1: if the low byte is 0,
    "D0 02"     #       BNE +2        the borrow comes from the high
    "C6 05"     #       DEC CNT+1
    "C6 04"     #       DEC CNT
    "A5 04"     #       LDA CNT       CNT = 0 only if both bytes are
    "05 05"     #       ORA CNT+1
    "D0 E2"     #       BNE loop      back 30 bytes
)
PROGRAM = bytes.fromhex("A0 00") + LOOP + bytes.fromhex("00")  # LDY #0 ... BRK
ORIGIN = 0x0800


def run(memory):
    """Run from ORIGIN to BRK; return the number of instructions."""
    pc, a, y, z, steps = ORIGIN, 0, 0, False, 0

    def zp_word(p):
        return memory[p] | memory[(p + 1) & 0xFF] << 8

    while True:
        op, b = memory[pc], memory[(pc + 1) & 0xFFFF]
        steps += 1
        pc += 2
        if op == 0x00:                          # BRK
            return steps
        elif op == 0xA0:                        # LDY #b
            y = b
            z = y == 0
        elif op == 0xB1:                        # LDA (b),Y
            a = memory[(zp_word(b) + y) & 0xFFFF]
            z = a == 0
        elif op == 0x91:                        # STA (b),Y
            memory[(zp_word(b) + y) & 0xFFFF] = a
        elif op in (0xE6, 0xC6):                # INC b, DEC b
            memory[b] = (memory[b] + (1 if op == 0xE6 else -1)) & 0xFF
            z = memory[b] == 0
        elif op == 0xA5:                        # LDA b
            a = memory[b]
            z = a == 0
        elif op == 0x05:                        # ORA b
            a |= memory[b]
            z = a == 0
        elif op == 0xD0:                        # BNE b
            if not z:
                pc += b - 256 if b > 127 else b
        else:
            raise ValueError(f"not in this simulator: {op:02X}")


def copy(data, src, dst):
    memory = bytearray(65536)
    memory[ORIGIN:ORIGIN + len(PROGRAM)] = PROGRAM
    memory[src:src + len(data)] = data
    for p, v in ((0, src), (2, dst), (4, len(data))):
        memory[p], memory[p + 1] = v & 0xFF, v >> 8
    steps = run(memory)
    return bytes(memory[dst:dst + len(data)]), steps


print(f"the loop is {len(LOOP)} bytes, and {len(PROGRAM)} with LDY and BRK")
out, steps = copy(b"HELLO, SWEET16", 0x0900, 0x0A00)
print(f"14 bytes: {out.decode()}, {steps} instructions")
data = bytes(i * 7 & 0xFF for i in range(300))
out, steps = copy(data, 0x09F0, 0x0BF8)  # both pointers cross pages
print(f"300 bytes across pages: {'the same' if out == data else 'wrong'}, {steps} instructions")
