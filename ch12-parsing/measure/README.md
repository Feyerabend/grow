# Three ways to parse, measured

Everything but `measure/` is from `ch12-parsing` in the public repo, as it stands.

    python3 measure/speed.py    # time, Python calls a token, and deepest nesting, each parser
    python3 measure/errors.py   # 2000 one-token mistakes: where each parser reports them

Measured on an Apple M1, 8 GB, macOS 27.2, Python 3.9.6.
