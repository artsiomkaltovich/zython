import zython as zn
from zython._compile.flags import Flag
from zython._compile.ir import IR
from zython.operations._operation import _eq
from zython.operations.constraint import Constraint


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
        declaration = ""
        if isinstance(v, zn.Array):
            declaration = f"array[{_get_array_shape_decl(v.shape)}] of "  # TODO: refactor var vs par
        if v.type is int:
            declaration += f"var int: {v.name};"
        elif isinstance(v.type, range):
            declaration += f"var {v.type.start}..{v.type.stop - 1}: {v.name};"
        else:
            raise TypeError(f"Type {v.type} are not supported, please specify int or range")
        if v.value is not None:
            _set_value_as_constraint(ir, v)
        src.append(declaration)


def _get_array_shape_decl(shape):
    result = [f'0..{s - 1}' for s in shape]
    return f"{', '.join(result)}"


def _process_constraints(ir, src):
    for c in ir.constraints:
        src.append(f"constraint {c};")


def _set_value_as_constraint(ir, variable):
    # values should be set as constraint or it won't be returned
    ir.constraints.append(_eq(variable, _get_value_decl(variable)))


def _get_value_decl(variable):
    if isinstance(variable.value, tuple):
        # TODO: support 2 and more d
        return f"array1d({_get_array_shape_decl(variable.shape)}, [{', '.join(str(v) for v in variable.value)}])"
    return str(variable.value)
