#!/usr/bin/env python3
"""Random breakage: the verifier against changed bytes.

Each mutant is one of javac's classes, from classes/, with one to three
bytes of one method's code, or of its StackMapTable, set at random. Every
mutant goes to this machine's verifier. One it accepts is then run, on a
build with AddressSanitizer and UBSan, for at most two seconds: if the
verifier is sound, a run may trap as Java does, or loop, but never crash
the machine itself. With a java, each mutant also goes to Java, and the
two verdicts are counted.

    usage: mutate.py count seed checked-jvm [java]
"""

import collections
import os
import random
import subprocess
import sys
import tempfile

from classfile import ClassFile


def verdict_ours(path):
    r = subprocess.run(["build/jvm", "-v", path], capture_output=True, text=True)
    return "accepted" if r.returncode == 0 else "refused"


def verdict_java(java, folder, cls):
    env = {k: v for k, v in os.environ.items() if k != "JAVA_TOOL_OPTIONS"}
    try:
        r = subprocess.run([java, "-XX:-ShowCodeDetailsInExceptionMessages", "-cp", folder, cls],
                           capture_output=True, text=True, env=env, timeout=5)
    except subprocess.TimeoutExpired:
        return "accepted"           # it ran, and went on running
    if "java.lang.VerifyError" in r.stderr or "java.lang.ClassFormatError" in r.stderr:
        return "refused"
    return "accepted"


def main():
    count, seed, checked = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    java = sys.argv[4] if len(sys.argv) > 4 else None
    rng = random.Random(seed)
    classes = sorted(f[:-6] for f in os.listdir("classes") if f.endswith(".class"))
    originals = {}
    for c in classes:
        with open(f"classes/{c}.class", "rb") as f:
            originals[c] = f.read()
    tally = collections.Counter()
    crashes = 0
    differ = []
    with tempfile.TemporaryDirectory() as work:
        for n in range(count):
            cls = rng.choice(classes)
            c = ClassFile(originals[cls])
            m = c.methods[rng.choice(sorted(c.methods))]
            places = list(range(m.code, m.code + m.code_length))
            if m.stackmap and rng.random() < 0.3:
                places = list(range(m.stackmap, m.stackmap + 2 + 64))
                places = [p for p in places if p < len(c.data)]
            for _ in range(rng.randint(1, 3)):
                c.data[rng.choice(places)] = rng.randrange(256)
            if bytes(c.data) == originals[cls]:
                continue
            folder = os.path.join(work, str(n))
            os.mkdir(folder)
            path = os.path.join(folder, cls + ".class")
            with open(path, "wb") as f:
                f.write(c.data)
            ours = verdict_ours(path)
            if ours == "accepted":
                try:
                    r = subprocess.run([checked, path], capture_output=True, text=True, timeout=2)
                    if r.returncode not in (0, 1) or "Sanitizer" in r.stderr or "runtime error" in r.stderr:
                        crashes += 1
                        keep = f"build/crash-{seed}-{n}.class"
                        with open(keep, "wb") as f:
                            f.write(c.data)
                        print(f"crash: {keep}: {r.stderr.strip().splitlines()[:3]}")
                except subprocess.TimeoutExpired:
                    pass
            if java:
                theirs = verdict_java(java, folder, cls)
                tally[(ours, theirs)] += 1
                if ours != theirs:
                    keep = f"build/differ-{seed}-{n}-{cls}.class"
                    with open(keep, "wb") as f:
                        f.write(c.data)
                    differ.append(keep)
            else:
                tally[(ours, "")] += 1
            subprocess.run(["rm", "-rf", folder])
    total = sum(tally.values())
    print(f"{total} mutants, {crashes} crashes of the machine")
    for (ours, theirs), k in sorted(tally.items()):
        print(f"  {k:5d}  this machine {ours}" + (f", Java {theirs}" if theirs else ""))
    for d in differ:
        print("  differ:", d)
    sys.exit(1 if crashes else 0)


if __name__ == "__main__":
    main()
