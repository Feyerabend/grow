#!/usr/bin/env python3
"""
Exercise 16.1, measured: measure/cost.py's table, run on the machine as it is
and on build.py's, which keeps the saved block. measure/cost.py is run as it
is, in a copy of the chapter's folder whose vm is the one being measured.

    usage: python3 table.py [times]
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(HERE, "..")

with tempfile.TemporaryDirectory() as work:
    for name in ("as it is", "keeping the block"):
        folder = os.path.join(work, name.replace(" ", "_"))
        shutil.copytree(CH, folder, ignore=shutil.ignore_patterns("answers", "vm", "__pycache__"))
        if name == "keeping the block":
            with open(os.path.join(folder, "vm.c"), "w") as f:
                subprocess.run([sys.executable, os.path.join(HERE, "build.py")], stdout=f, check=True)
        subprocess.run(["make", "-s", "vm"], cwd=folder, check=True, capture_output=True)
        r = subprocess.run([sys.executable, "measure/cost.py"], cwd=folder,
                           capture_output=True, text=True, check=True)
        print(name)
        for line in r.stdout.splitlines():
            if "times" in sys.argv[1:]:
                print("  " + line)
            elif "places/trip" in line:
                print(f"  {'':16} {'places/trip':>11} {'collections':>12}")
            else:
                words = line.split()                # name..., places, collections, seconds, ms
                print(f"  {' '.join(words[:-4]):16} {words[-4]:>11} {words[-3]:>12}")
