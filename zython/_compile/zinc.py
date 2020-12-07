from zython._compile.flags import Flag
from zython._compile.ir import IR


def to_zinc(ir: IR):
    result = []
    _make_imports(ir, result)
    for var in ir.vars.values():
        if var.type is int:
            result.append(f"int: {var.name};")
        elif isinstance(var.type, range):
            result.append(f"var {var.type.start}..{var.type.stop - 1}: {var.name};")
    for c in ir.constraints:
        result.append(f"constraint {c};")
    result.append(f"solve {ir.how_to_solve};")
    return "\n".join(result)


def _make_imports(ir, result):
    if Flag.all_different in ir.flags:
        result.append('include "alldifferent.mzn";')
