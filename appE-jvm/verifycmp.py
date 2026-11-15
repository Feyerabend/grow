#!/usr/bin/env python3
"""The broken class files, put to this machine's verifier and to Java's.

For each case that break.py made, it runs `build/jvm -v` and, if a java
is given, `java` on the class, and prints one line: the case, what each
said, and the first line of each one's reason. It fails if either accepts a
case it should refuse, or if the two differ where they are not known to.

    usage: verifycmp.py [broken folder] [java]
"""

import os
import re
import subprocess
import sys


def ours(folder, cls):
    r = subprocess.run(["build/jvm", "-v", os.path.join(folder, cls + ".class")],
                       capture_output=True, text=True)
    if r.returncode == 0:
        return "accepted", ""
    reason = r.stderr.strip().split(": ", 1)[-1]
    return "refused", reason


def java(command, folder, cls):
    # -Xshare:off and no JAVA_TOOL_OPTIONS, so that nothing else is printed.
    env = {k: v for k, v in os.environ.items() if k != "JAVA_TOOL_OPTIONS"}
    r = subprocess.run([command, "-cp", folder, cls], capture_output=True, text=True,
                       env=env, timeout=60)
    found = re.search(r"java\.lang\.(\w+Error)[: ]*(.*)", r.stderr)
    if found:
        return "refused", f"{found.group(1)}: {found.group(2).strip()}"[:110]
    return "accepted", ""


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "build/broken"
    command = sys.argv[2] if len(sys.argv) > 2 else None
    bad = 0
    with open(os.path.join(folder, "cases.txt")) as f:
        cases = [line.rstrip("\n").split("\t") for line in f]
    for name, cls, why, who, differ in cases:
        where = os.path.join(folder, name)
        mine, my_reason = ours(where, cls)
        print(f"{name}: {why}")
        print(f"    this machine {mine}{': ' + my_reason if my_reason else ''}")
        if mine != ("accepted" if who == "this machine" else "refused"):
            bad += 1
            print("    not as expected")
        if command:
            try:
                theirs, their_reason = java(command, where, cls)
            except subprocess.TimeoutExpired:
                theirs, their_reason = "accepted", "and ran for a minute"
            print(f"    Java {theirs}{': ' + their_reason if their_reason else ''}")
            if theirs != ("accepted" if who == "Java" else "refused"):
                bad += 1
                print("    not as expected")
        if differ:
            print(f"    known: {differ}")
    n = len(cases)
    print(f"{n} broken class files: " + ("as expected" if not bad else f"{bad} not as expected"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
