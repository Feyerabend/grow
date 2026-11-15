#!/usr/bin/env python3
"""
Exercise 5.5: a check value after the length, the sum of the code words,
modulo 2**32. tobin.py writes it, the loader checks it, and then
measure/damage.py, unchanged, damages the files of the new format. The changed
tobin.py and vm.c are made from chapter 5's, in a folder of their own.

    usage: python3 checksum.py [count] [seed]
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH05 = os.path.join(HERE, "..")


def changed_tobin():
    s = open(os.path.join(CH05, "tobin.py")).read()
    old = '        f.write(struct.pack("<i", len(code)))\n'
    assert s.count(old) == 1
    return s.replace(old, old + '        total = sum(code) % 2**32\n'
                     '        f.write(struct.pack("<I", total))\n')


def changed_vm():
    s = open(os.path.join(CH05, "vm.c")).read()
    old = '''    if (fgetc(f) != EOF)
        bad_file(path, "extra bytes after the code");'''
    assert s.count(old) == 1
    s = s.replace(old, old + '''
    {
        unsigned long total = 0;
        for (i = 0; i < n; i++)
            total = (total + (unsigned long) (unsigned int) words[i]) & 0xffffffffUL;
        if (total != (unsigned long) (unsigned int) word32(check))
            bad_file(path, "wrong check value");
    }''')
    old = "    n = word32(header + 4);\n"
    assert s.count(old) == 1
    s = s.replace(old, old + '    if (fread(check, 1, 4, f) != 4)\n'
                  '        bad_file(path, "too short to be a program");\n')
    s = s.replace("    unsigned char header[8], b[4];", "    unsigned char header[8], b[4], check[4];")
    return s


def main():
    with tempfile.TemporaryDirectory() as folder:
        open(os.path.join(folder, "tobin.py"), "w").write(changed_tobin())
        open(os.path.join(folder, "vm.c"), "w").write(changed_vm())
        shutil.copytree(os.path.join(CH05, "samples"), os.path.join(folder, "samples"))
        os.mkdir(os.path.join(folder, "measure"))
        shutil.copy(os.path.join(CH05, "measure", "damage.py"), os.path.join(folder, "measure"))
        r = subprocess.run([sys.executable, "measure/damage.py", *sys.argv[1:]],
                           cwd=folder, capture_output=True, text=True, check=True)
    print(r.stdout, end="")


if __name__ == "__main__":
    main()
