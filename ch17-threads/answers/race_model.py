#!/usr/bin/env python3
"""
Exercise 17.2: a model of measure/race.py's race, small enough to follow by
hand, checked against the machine. Each thread runs t's code from suite/race.asm:
PUSH 1000, then a loop of fourteen instructions, of which LOADM reads the
shared place and STOREM writes it back, plus one, four instructions later.
The scheduler runs the threads in turn, a and b, each for a turn of T
instructions or until it ends.

The model's total must equal the machine's for every turn from 1 to 30; then
its first rounds are shown for the turns the exercise asks about.

    usage: python3 race_model.py
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(CH, "measure"))
os.chdir(CH)
import race                                     # noqa: E402

LOOP = ["LOAD 1", "JZ done", "PUSH 0", "LOADM", "PUSH 1", "ADD", "PUSH 0", "SWAP",
        "STOREM", "LOAD 1", "PUSH 1", "SUB", "STORE 1", "JMP next"]
ROUNDS = 1000


def model(turn, show=0):
    memory = 0
    threads = [{"name": n, "at": -1, "left": ROUNDS, "held": None, "dead": False} for n in "ab"]
    lines = []
    while not all(t["dead"] for t in threads):
        for t in threads:
            if t["dead"]:
                continue
            done = []
            for _ in range(turn if turn else 10**9):
                if t["at"] == -1:                       # PUSH 1000
                    t["at"] = 0
                    done.append("PUSH 1000")
                    continue
                op = LOOP[t["at"]]
                if op == "JZ done" and t["left"] == 0:
                    done.append(op)
                    t["at"] = "done"
                    break
                if op == "LOADM":
                    t["held"] = memory
                    done.append(f"LOADM={memory}")
                elif op == "STOREM":
                    memory = t["held"] + 1
                    done.append(f"STOREM={memory}")
                elif op == "SUB":
                    t["left"] -= 1
                    done.append(op)
                else:
                    done.append(op)
                t["at"] = (t["at"] + 1) % len(LOOP)
            if t["at"] == "done":                        # PUSH 0, RET: two more, then dead
                t["dead"] = True
            if show and len(lines) < show:
                lines.append(f"  {t['name']}: " + " ".join(w for w in done if w.startswith(("LOADM", "STOREM")))
                             + f"   (stops before {LOOP[t['at']] if isinstance(t['at'], int) else 'its end'})")
    return memory, lines


def machine(turn, folder):
    path = os.path.join(folder, "p")
    open(path + ".asm", "w").write(race.program(turn, race.NONE))
    subprocess.run([sys.executable, "asm.py", path + ".asm", path + ".vm"], check=True)
    return int(subprocess.run(["./vm", path + ".vm"], capture_output=True, text=True, check=True).stdout)


with tempfile.TemporaryDirectory() as folder:
    wrong = [t for t in range(1, 31) if model(t)[0] != machine(t, folder)]
print("the model agrees with the machine for every turn from 1 to 30" if not wrong
      else f"the model is wrong for turns {wrong}")
for turn in (2, 3, 5, 7, 10, 14):
    total, lines = model(turn, show=6)
    print(f"\nturn {turn}: total {total}; the first turns, with each LOADM and STOREM and what it saw:")
    print("\n".join(lines))
