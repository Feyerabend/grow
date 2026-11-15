#!/usr/bin/env python3
"""
lambda.py with three changes, each behind an option:

  -tail     15.1: a call in tail position is TAILCALLI 2, which replaces the
            current frame instead of adding one. Tail positions: a
            function's body, both branches of an if in one, a let's body,
            and the last expression of a sequence.
  -once     15.4: a closure that captures nothing is made once, at the start,
            and kept in memory, address 4095 down; each fun then reads it
            from there instead of making a new block.
  -direct   15.5: a function bound by 'let rec f a b = ...', called with both
            arguments where f is known to mean it, is called at a second
            entry, direct_f, with f's closure and both arguments as its
            three locals, and no closure for the first argument.

    usage: lambda_more.py [-tail] [-once] [-direct] program.lam
"""

import os
import sys

import importlib.util                           # noqa: E402

# lambda.py cannot be imported by name: lambda is a word of Python's.
_spec = importlib.util.spec_from_file_location(
    "lam", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lambda.py"))
lam = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lam)


class Where(tuple):
    """Where a variable is, as lambda.py's ("local", k) or ("captured", i),
    and, when it is a known function of two arguments, its direct entry."""

    def __new__(cls, place, direct=None):
        w = super().__new__(cls, place)
        w.direct = direct
        return w


class Generator(lam.Generator):
    def __init__(self, tail, once, direct):
        super().__init__()
        self.tail, self.once, self.use_direct = tail, once, direct
        self.constants = []                     # (address, label) made at the start
        self.directs = []                       # (label, fun, outer names) to compile

    def program(self, node):
        self.out.append("main:")
        start = len(self.out)
        self.gen(node, {}, 0)
        self.emit("DROP")
        self.emit("HALT")
        while self.functions or self.directs:
            if self.functions:
                label, fun, names, known = self.functions.pop(0)
                self.out.append("")
                self.out.append(f"; fun {fun[1]} -> ..., capturing: {' '.join(names) or 'nothing'}")
                self.out.append(f"{label}:")
                env = {fun[1]: Where(("local", 1))}
                for i, name in enumerate(names):
                    env.setdefault(name, Where(("captured", i + 1), known.get(name)))
                self.gen(fun[2], env, 2, tail=True)
                self.emit("RET")
            else:
                label, fun, names, known = self.directs.pop(0)
                # The direct entry: local 0 is f's own closure, locals 1 and 2
                # the two arguments; what f's closure holds is still its fields.
                inner = fun[2]
                self.out.append("")
                self.out.append(f"; direct entry: fun {fun[1]} {inner[1]} -> ...")
                self.out.append(f"{label}:")
                env = {}
                for i, name in enumerate(names):
                    env[name] = Where(("captured", i + 1), known.get(name))
                env[fun[1]] = Where(("local", 1))
                env[inner[1]] = Where(("local", 2))
                self.gen(inner[2], env, 3, tail=True)
                self.emit("RET")
        # The closures that capture nothing, made once, at the start.
        made = []
        for address, label in self.constants:
            made += [f"        PUSH {address}", "        PUSH 1", "        NEW", "        DUP",
                     "        PUSH 0", f"        PUSH {label}", "        SETF", "        STOREM"]
        self.out[start:start] = made
        return "\n".join(self.out) + "\n"

    def closure(self, fun, env, depth, itself=None, direct=None):
        names = sorted(lam.free(fun))
        for name in names:
            if name != itself and name not in env:
                raise lam.CompileError(f"'{name}' is not defined", lam.first_use(fun, name))
        known = {name: env[name].direct for name in names
                 if name in env and getattr(env[name], "direct", None)}
        if itself and direct:
            known[itself] = direct
        label = self.new_label("fun_")
        self.functions.append((label, fun, names, known))
        if direct:
            self.directs.append((direct, fun, names, known))
        if self.once and not names:
            address = 4095 - len(self.constants)
            self.constants.append((address, label))
            self.emit(f"PUSH {address}")
            self.emit("LOADM")
            return
        self.emit(f"PUSH {1 + len(names)}")
        self.emit("NEW")
        self.emit("DUP")
        self.emit("PUSH 0")
        self.emit(f"PUSH {label}")
        self.emit("SETF")
        for i, name in enumerate(names):
            self.emit("DUP")
            self.emit(f"PUSH {i + 1}")
            if name == itself:
                self.emit("OVER")
            else:
                self.variable(name, env, fun[3])
            self.emit("SETF")

    def gen(self, node, env, depth, tail=False):
        kind = node[0]
        tail = tail and self.tail
        if kind == "app":
            _, function, argument, _ = node
            if (self.use_direct and function[0] == "app" and function[1][0] == "var"
                    and getattr(env.get(function[1][1]), "direct", None)):
                label = env[function[1][1]].direct
                self.gen(function[1], env, depth)
                self.gen(function[2], env, depth + 1)
                self.gen(argument, env, depth + 2)
                if tail:
                    self.emit(f"PUSH {label}")
                    self.emit("TAILCALLI 3")
                else:
                    self.emit(f"CALL {label} 3")
                return
            self.gen(function, env, depth)
            self.gen(argument, env, depth + 1)
            self.emit("OVER")
            self.emit("PUSH 0")
            self.emit("GETF")
            self.emit("TAILCALLI 2" if tail else "CALLI 2")
        elif kind == "if":
            _, condition, then, otherwise, _ = node
            other, done = self.new_label(), self.new_label()
            self.gen(condition, env, depth)
            self.emit(f"JZ {other}")
            self.gen(then, env, depth, tail)
            self.emit(f"JMP {done}")
            self.out.append(f"{other}:")
            self.gen(otherwise, env, depth, tail)
            self.out.append(f"{done}:")
        elif kind == "let":
            _, name, value, body, recursive, _ = node
            direct = None
            if (recursive and self.use_direct and value[0] == "fun" and value[2][0] == "fun"):
                direct = self.new_label(f"direct_{name}_")
            if recursive:
                self.closure(value, env, depth, itself=name, direct=direct)
            else:
                self.gen(value, env, depth)
            inner = dict(env)
            inner[name] = Where(("local", depth), direct)
            self.gen(body, inner, depth + 1, tail)
            self.emit("SWAP")
            self.emit("DROP")
        elif kind == "seq":
            for k, item in enumerate(node[1]):
                last = k == len(node[1]) - 1
                self.gen(item, env, depth, tail and last)
                if not last:
                    self.emit("DROP")
        elif kind == "fun":
            self.closure(node, env, depth)
        else:
            # Everything else is lambda.py's, with tail calls nowhere below it.
            super().gen(node, env, depth)


def main():
    args = sys.argv[1:]
    flags = {a for a in args if a.startswith("-")}
    path = [a for a in args if not a.startswith("-")][0]
    text = open(path).read()
    try:
        node = lam.Parser(lam.scan(text)).program()
        g = Generator("-tail" in flags, "-once" in flags, "-direct" in flags)
        sys.stdout.write(g.program(node))
    except lam.CompileError as error:
        lam.report(path, text, error)
        sys.exit(1)


if __name__ == "__main__":
    main()
