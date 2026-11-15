// Made by samples.py from samples/*.hex and answers/*.hex: do not edit.
const SAMPLES = [
 {
  "name": "samples/answer.hex",
  "title": "Six times seven, by adding, shown in decimal on the screen.",
  "text": "; Six times seven, by adding, shown in decimal on the screen.\n; CHIP-8 has no multiplication, and no way to print a number: the\n; program splits it into decimal digits, and draws each digit with\n; the machine's own font.\n\n6000    ; 200  V0 := 0\n6107    ; 202  V1 := 7              count seven times\n7006    ; 204  V0 += 6              loop:\n71FF    ; 206  V1 += 255            that is, V1 -= 1\n3100    ; 208  skip if V1 = 0\n1204    ; 20A  jump to the loop\nA300    ; 20C  I := 300\nF033    ; 20E  the digits of V0 at 300, 301, 302\nF265    ; 210  V0, V1, V2 := the three digits\n6314    ; 212  V3 := 20             x\n640C    ; 214  V4 := 12             y\nF029    ; 216  I := the font's picture of digit V0\nD345    ; 218  draw it: 5 rows at V3, V4\n7305    ; 21A  V3 += 5\nF129    ; 21C  the same for V1\nD345    ; 21E\n7305    ; 220\nF229    ; 222  and for V2\nD345    ; 224\n1226    ; 226  jump here: the end\n"
 },
 {
  "name": "samples/collide.hex",
  "title": "Drawing is XOR. Draw a block, then the same block overlapping it:",
  "text": "; Drawing is XOR. Draw a block, then the same block overlapping it:\n; where they overlap, the pixels go dark, and VF says the two met.\n; Games find collisions this way, and move a sprite by drawing it\n; twice: once to erase it, once in its new place.\n\nA218    ; 200  I := 218             the block, below\n6008    ; 202  V0 := 8              x\n6108    ; 204  V1 := 8              y\nD018    ; 206  draw 8 rows at V0, V1\n600C    ; 208  V0 := 12\n610C    ; 20A  V1 := 12\nD018    ; 20C  draw again: VF := 1, since they overlap\n6228    ; 20E  V2 := 40\n630C    ; 210  V3 := 12\nFF29    ; 212  I := the font's picture of digit VF\nD235    ; 214  draw it\n1216    ; 216  the end\nFFFF    ; 218  the block: eight rows of eight pixels\nFFFF\nFFFF\nFFFF\n"
 },
 {
  "name": "samples/quirks.hex",
  "title": "The four differences between the VIP and CHIP-48, each leaving a digit",
  "text": "; The four differences between the VIP and CHIP-48, each leaving a digit\n; in a register, and the four digits drawn: 1 0 0 1 on the VIP, 3 5 8 2\n; with -m chip48.\n\n6B06    ; 200  VB := 6\n6203    ; 202  V2 := 3\n8B26    ; 204  VB := shifted right: V2 >> 1 = 1 on the VIP, VB >> 1 = 3 on CHIP-48\n6F05    ; 206  VF := 5\n6300    ; 208  V3 := 0\n6400    ; 20A  V4 := 0\n8341    ; 20C  V3 |= V4: VF := 0 on the VIP, VF stays 5 on CHIP-48\n8AF0    ; 20E  VA := VF\n6007    ; 210  V0 := 7\n6108    ; 212  V1 := 8\nA300    ; 214  I := 300\nF155    ; 216  store V0, V1 at 300, 301: I is then 302 on the VIP, 301 on CHIP-48\nF065    ; 218  V0 := the byte at I: 0 on the VIP, 8 on CHIP-48\n8C00    ; 21A  VC := V0\n6000    ; 21C  V0 := 0\n6204    ; 21E  V2 := 4\nB228    ; 220  go to 228 + V0 on the VIP, 228 + V2 on CHIP-48\n1222    ; 222  (not reached)\n1222    ; 224\n1222    ; 226\n6D01    ; 228  VD := 1\n122E    ; 22A  jump over the next\n6D02    ; 22C  VD := 2\n6305    ; 22E  V3 := 5              x\n640C    ; 230  V4 := 12             y\nFB29    ; 232  I := the picture of digit VB\nD345    ; 234  draw it\n7306    ; 236  V3 += 6\nFA29    ; 238  VA\nD345    ; 23A\n7306    ; 23C\nFC29    ; 23E  VC\nD345    ; 240\n7306    ; 242\nFD29    ; 244  VD\nD345    ; 246\n1248    ; 248  the end\n"
 },
 {
  "name": "answers/keydigit.hex",
  "title": "Exercise 1: draw the digit in V0 at the top left, wait for a key, and",
  "text": "; Exercise 1: draw the digit in V0 at the top left, wait for a key, and\n; draw that key's digit beside it. V0 is set here, to 5, for the run;\n; the program proper is the nine instructions from 202, 18 bytes.\n\n6005    ; 200  V0 := 5              the digit given\n6100    ; 202  V1 := 0              x\n6200    ; 204  V2 := 0              y\nF029    ; 206  I := the picture of digit V0\nD125    ; 208  draw it: 5 rows at V1, V2\nF30A    ; 20A  V3 := the next key, waiting for it\n6105    ; 20C  V1 := 5              beside the first\nF329    ; 20E  I := the picture of digit V3\nD125    ; 210  draw it\n1212    ; 212  the end\n"
 },
 {
  "name": "answers/multiply.hex",
  "title": "Exercise 3: V0 := V1 times V2 by adding V1 to V0, V2 times. The loop is",
  "text": "; Exercise 3: V0 := V1 times V2 by adding V1 to V0, V2 times. The loop is\n; four instructions, with its test at the bottom; a test before it sends\n; V2 = 0 straight to the end. For 6 times 7 the loop runs 7 times, the\n; last time without its jump back: 4 * 6 + 3 = 27 instructions, and 4\n; before them. The product is drawn in decimal, as samples/answer.hex does.\n\n6106    ; 200  V1 := 6\n6207    ; 202  V2 := 7\n6000    ; 204  V0 := 0\n4200    ; 206  skip if V2 is not 0\n1214    ; 208  V2 is 0: to the end\n8014    ; 20A  V0 += V1             loop:\n72FF    ; 20C  V2 -= 1\n3200    ; 20E  skip if V2 = 0\n120A    ; 210  back to the loop\nA300    ; 212  I := 300\nF033    ; 214  the digits of V0 at 300, 301, 302\nF265    ; 216  V0, V1, V2 := the three digits\n6314    ; 218  V3 := 20             x\n640C    ; 21A  V4 := 12             y\nF029    ; 21C  digit V0\nD345    ; 21E\n7305    ; 220\nF129    ; 222  digit V1\nD345    ; 224\n7305    ; 226\nF229    ; 228  digit V2\nD345    ; 22A\n122C    ; 22C  the end\n"
 },
 {
  "name": "answers/overlap.hex",
  "title": "Exercise 2: a block of two by two drawn at 8,8 and another at 9,9, so",
  "text": "; Exercise 2: a block of two by two drawn at 8,8 and another at 9,9, so\n; that they overlap by one spot; then the first drawn again. VF after\n; each of the last two draws is kept, and drawn as a digit at the top.\n\nA222    ; 200  I := 222             the block, below\n6008    ; 202  V0 := 8\nD002    ; 204  draw 2 rows at V0, V0: the first block, at 8,8\n6209    ; 206  V2 := 9\nD222    ; 208  the second, at 9,9: they share the spot 9,9\n8AF0    ; 20A  VA := VF\nD002    ; 20C  the first again\n8BF0    ; 20E  VB := VF\n6328    ; 210  V3 := 40             x\n6400    ; 212  V4 := 0              y\nFA29    ; 214  I := the picture of digit VA\nD345    ; 216  draw it\n7306    ; 218  V3 += 6\nFB29    ; 21A  digit VB\nD345    ; 21C\n121E    ; 21E  the end\nC0C0    ; 220  (padding, never run)\nC0C0    ; 222  the block: two rows of two spots\n"
 },
 {
  "name": "answers/shift.hex",
  "title": "Exercise 4: 8XY6 shifts VY on the VIP, and VX on CHIP-48. With V2 = 3",
  "text": "; Exercise 4: 8XY6 shifts VY on the VIP, and VX on CHIP-48. With V2 = 3\n; and VB = 6, VB becomes 3 >> 1 = 1 on the VIP, and 6 >> 1 = 3 on\n; CHIP-48; the digit is drawn.\n\n6B06    ; 200  VB := 6\n6203    ; 202  V2 := 3\n8B26    ; 204  VB := shifted right\n6305    ; 206  V3 := 5              x\n640C    ; 208  V4 := 12             y\nFB29    ; 20A  digit VB\nD345    ; 20C\n120E    ; 20E  the end\n"
 }
];
