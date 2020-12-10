import zython as zn
from zython._compile.flags import Flag
from zython._compile.ir import IR


def to_zinc(ir: IR):
    result = []
    _make_imports(ir, result)
    _process_vars(ir, result)
    _process_constraints(ir, result)
    result.append(f"solve {ir.how_to_solve};")
    return "\n".join(result)


def _make_imports(ir, src):
    if Flag.all_different in ir.flags:
        src.append('include "alldifferent.mzn";')


def _process_vars(ir, src):
    for v in ir.vars.values():
        # TODO: check reserved word are not used as variable name
        declaration = None
        if isinstance(v, zn.Array):
            declaration = f"array{_get_array_shape_decl(v)} of var "  # TODO: refactor var vs par
        if v.type is int:
            declaration += f"int: {v.name};"
        elif isinstance(v.type, range):
            declaration += f"var {v.type.start}..{v.type.stop - 1}: {v.name};"
        else:
            raise TypeError(f"Type {v.type} are not supported, please specify int or range")
        src.append(declaration)


def _get_array_shape_decl(array):
    return f"[0..{array.shape - 1}]"


def _process_constraints(ir, src):
    for c in ir.constraints:
        src.append(f"constraint {c};")
