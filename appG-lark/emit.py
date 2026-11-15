r"""
Write a Lark program's typed tree to a file, for the C CEK machine to
read: the change this appendix makes to Lark, which compiled each
program's tree into C data, and so into a binary of its own.

    python3 emit.py program.lark > program.tree

Lark's own front end, in lark/src, parses the program, checks its types,
and resolves its imports, as emit_c_ast.py does; this writes the same
tree as an S-expression. One node is one list: its kind, then its parts.

    (lark 2 DECL ...)

    (fn NAME PARAM EXPR)            a function; more parameters are lambdas
    (let NAME EXPR)
    (type NAME (NAME ARITY) ...)    a type's constructors
    (impl TYPE TRAIT (NAME PARAM EXPR) ...)

    (int N) (float BITS) (bool 0|1) (str S) (unit)      literals
    (var NAME DEPTH) (con NAME DEPTH) (tuple EXPR ...)
    (apply FN EXPR ...) (binop OP L R) (unary OP E)
    (let NAME VALUE BODY) (if C T E) (lambda PARAM BODY)
    (match EXPR (arm PAT EXPR) ...)

    (wild) (pvar NAME) (plit LIT) (pcon NAME PAT ...) (ptuple PAT ...)

Every name, operator and string is in double quotes, with \\, \", \n,
\r, \t and \xHH escaped. A float is its 32 bits, as an unsigned number,
so that nothing is lost in writing it out.

A variable's DEPTH says where the machine will find it: how many cells
of the environment to pass over, or -1 for a name at the top level. It
is worked out here, once, from where the program binds its names, in
the order the machine binds them (cek.c):

- calling a function binds its parameter, then, for a function declared
  with fn or a method, its own name, so that the name is innermost;
- let binds its name; a lambda its parameter;
- a match arm binds its pattern's variables left to right, each in front
  of the one before, so that the last is innermost;
- a top-level let is evaluated with no local names at all.
"""

import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lark", "src"))

import emit_c_ast                         # noqa: E402
import infer                              # noqa: E402
import parser                             # noqa: E402
from ty import T_UNIT                     # noqa: E402
from typed_tree import (                  # noqa: E402
    TFnDecl, TLetDecl, TTypeDecl, TImplDecl,
    TLit, TVar, TCon, TTupleExpr, TApply, TBinOp, TUnaryOp,
    TLetExpr, TIfExpr, TMatchExpr, TLambda,
    TPWild, TPVar, TPLit, TPCon, TPTuple,
)


def quote(s):
    out = ['"']
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 32:
            out.append(f"\\x{ord(ch):02x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def literal(value):
    if value is None:
        return "(unit)"
    if isinstance(value, bool):
        return f"(bool {int(value)})"
    if isinstance(value, int):
        return f"(int {value})"
    if isinstance(value, float):
        return f"(float {struct.unpack('I', struct.pack('f', value))[0]})"
    if isinstance(value, str):
        return f"(str {quote(value)})"
    raise TypeError(f"literal: {type(value).__name__}")


def lambdas(params, body):
    """The extra parameters of a function, as nested one-parameter lambdas."""
    for name, _ in reversed(params):
        body = TLambda(params=((name, T_UNIT),), body=body, typ=T_UNIT)
    return body


def where(name, scope):
    """The depth of name in scope (innermost first), or -1 for top level."""
    for depth, n in enumerate(scope):
        if n == name:
            return depth
    return -1


def expr(e, scope):
    if isinstance(e, TLit):
        return literal(e.value)
    if isinstance(e, TVar):
        return f"(var {quote(e.name)} {where(e.name, scope)})"
    if isinstance(e, TCon):
        return f"(con {quote(e.name)} {where(e.name, scope)})"
    if isinstance(e, TTupleExpr):
        return "(tuple" + "".join(" " + expr(x, scope) for x in e.elems) + ")"
    if isinstance(e, TApply):
        return f"(apply {expr(e.fn, scope)}" + "".join(" " + expr(a, scope) for a in e.args) + ")"
    if isinstance(e, TBinOp):
        return f"(binop {quote(e.op)} {expr(e.left, scope)} {expr(e.right, scope)})"
    if isinstance(e, TUnaryOp):
        return f"(unary {quote(e.op)} {expr(e.operand, scope)})"
    if isinstance(e, TLetExpr):
        return (f"(let {quote(e.name)} {expr(e.value, scope)} "
                f"{expr(e.body, [e.name] + scope)})")
    if isinstance(e, TIfExpr):
        return f"(if {expr(e.cond, scope)} {expr(e.then_, scope)} {expr(e.else_, scope)})"
    if isinstance(e, TMatchExpr):
        arms = ""
        for p, b in e.arms:
            bound = []
            text = pattern(p, bound)
            arms += f" (arm {text} {expr(b, list(reversed(bound)) + scope)})"
        return f"(match {expr(e.scrutinee, scope)}{arms})"
    if isinstance(e, TLambda):
        param = e.params[0][0]
        body = lambdas(e.params[1:], e.body)
        return f"(lambda {quote(param)} {expr(body, [param] + scope)})"
    raise TypeError(f"expr: {type(e).__name__}")


def pattern(p, bound):
    """A pattern; the names it binds are added to bound, in binding order."""
    if isinstance(p, TPWild):
        return "(wild)"
    if isinstance(p, TPVar):
        bound.append(p.name)
        return f"(pvar {quote(p.name)})"
    if isinstance(p, TPLit):
        return f"(plit {literal(p.value)})"
    if isinstance(p, TPCon):
        return f"(pcon {quote(p.name)}" + "".join(" " + pattern(a, bound) for a in p.args) + ")"
    if isinstance(p, TPTuple):
        return "(ptuple" + "".join(" " + pattern(x, bound) for x in p.elems) + ")"
    raise TypeError(f"pattern: {type(p).__name__}")


def decl(d):
    """A declaration, or None for one with nothing to run (an alias)."""
    if isinstance(d, TFnDecl):
        if not d.params:
            raise ValueError(f"function {d.name!r} has no parameters")
        param = d.params[0][0]
        body = expr(lambdas(d.params[1:], d.body), [d.name, param])
        return f"(fn {quote(d.name)} {quote(param)} {body})"
    if isinstance(d, TLetDecl):
        return f"(let {quote(d.name)} {expr(d.value, [])})"
    if isinstance(d, TTypeDecl):
        if not d.variants:
            return None
        return f"(type {quote(d.name)}" + "".join(
            f" ({quote(v.name)} {len(v.payload)})" for v in d.variants) + ")"
    if isinstance(d, TImplDecl):
        methods = [m for m in d.methods if m.params]
        if not methods:
            return None
        return f"(impl {quote(d.for_type)} {quote(d.trait_name)}" + "".join(
            f" ({quote(m.name)} {quote(m.params[0][0])} "
            f"{expr(lambdas(m.params[1:], m.body), [m.name, m.params[0][0]])})"
            for m in methods) + ")"
    raise TypeError(f"decl: {type(d).__name__}")


def emit(path):
    program = parser.parse_file(path)
    typed = infer.typecheck(program, source_file=path)
    imports = emit_c_ast._load_imports(program, os.path.dirname(os.path.abspath(path)))
    lines = ["(lark 2"]
    for d in list(imports) + list(typed.decls):
        text = decl(d)
        if text:
            lines.append(" " + text)
    lines.append(")")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: emit.py program.lark > program.tree")
    try:
        text = emit(sys.argv[1])
    except (*infer.DIAGNOSTICS, OSError) as e:    # refused, as Lark's cek.py says it
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    sys.stdout.write(text)
