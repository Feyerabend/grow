"""
Write samples.js: the programs of samples/ and answers/, as text, for
the page to offer without fetching them, which a page opened from disk
may not. Each is named by its file, and titled by its first comment.

    python3 samples.py > samples.js
"""

import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    programs = []
    for folder in ("samples", "answers"):
        for path in sorted(glob.glob(os.path.join(HERE, "..", folder, "*.hex"))):
            text = open(path).read()
            first = text.splitlines()[0].lstrip("; ").rstrip() if text else ""
            programs.append({"name": f"{folder}/{os.path.basename(path)}",
                             "title": first, "text": text})
    print("// Made by samples.py from samples/*.hex and answers/*.hex: do not edit.")
    print("const SAMPLES = " + json.dumps(programs, indent=1) + ";")


if __name__ == "__main__":
    main()
