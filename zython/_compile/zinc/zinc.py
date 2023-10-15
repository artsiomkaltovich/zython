from collections import deque
from functools import singledispatch
from typing import Set

from zython._compile.ir import IR
from zython._compile.zinc.flags import Flags, FLAG_PROCESSORS
from zython._compile.zinc.to_str import to_str, _binary_op, _get_array_shape_decl
from zython._compile.zinc.types import SourceCode
from zython.operations.constraint import Constraint
from zython.var_par.collections.array import ArrayMixin
from zython.var_par.collections.set import SetVar, SetPar
from zython.var_par.get_type import is_range, is_int_range, is_enum


def to_zinc(ir: IR):
    result: SourceCode = deque()
    flags: Set[Flags] = set()
    _process_enums(ir, result, flags)
    _process_pars(ir, result, flags)
    _process_vars(ir, result, flags)
    _process_constraints(ir, result, flags)
    _process_how_to_solve(ir, result)
    _process_flags(flags, result)
    return "\n".join(result)


def _process_flags(flags, result: SourceCode):
    for flag in flags:
        FLAG_PROCESSORS[flag](result)


def _process_enums(ir: IR, result: SourceCode, flags: Set[Flags]) -> None:
    for e in ir.enums:
        result.append(f"enum {e.__name__};")


def _process_pars_and_vars(ir, vars_or_pars, src, decl_prefix, flags):
    for v in vars_or_pars.values():
        # TODO: check reserved word are not used as variable name
        declaration = _get_variable_decl(v, decl_prefix, flags)
        src.append(declaration)
        if isinstance(v.value, Constraint):
            _set_value_as_constraint(ir, v, flags)


def _process_pars(ir, src, flags):
    _process_pars_and_vars(ir, ir.pars, src, "", flags)


def _process_vars(ir, src, flags):
    _process_pars_and_vars(ir, ir.vars, src, "var", flags)


@singledispatch
def _get_variable_decl(v, decl_prefix, flags) -> str:
    return _elementary_var_decl(v, decl_prefix, flags)


@_get_variable_decl.register(ArrayMixin)
def _(v, decl_prefix, flags):
    return f"array[{_get_array_shape_decl(v._shape)}] of {_elementary_var_decl(v, decl_prefix, flags)}"


@_get_variable_decl.register(SetVar)
def _(v, decl_prefix, flags):
    return f"var set of {_elementary_var_decl(v, '', flags)}"


@_get_variable_decl.register(SetPar)
def _(v, decl_prefix, flags):
    return f"set of {_elementary_var_decl(v, '', flags)}"


def _elementary_var_decl(v, decl_prefix, flags):
    declaration = ""
    if v.type is int:
        declaration += f"{decl_prefix} int: {v.name};"
    elif v.type is float:
        flags.add(Flags.float_used)
        declaration += f"{decl_prefix} float: {v.name};"
    elif is_range(v.type):
        if not is_int_range(v.type):
            flags.add(Flags.float_used)
        declaration += f"{decl_prefix} {to_str(v.type, flags_=flags)}: {v.name};"
    elif is_enum(v.type):
        declaration += f"{decl_prefix} {v.type.__name__}: {v.name};"
    else:
        raise TypeError(f"Type {v.type} are not supported, please specify int or range")
    return declaration


def _set_value_as_constraint(ir, variable, flags_):
    # values like `var int: s = sum(a);` should be set as constraint or it won't be returned in result
    ir.constraints.append(_binary_op("==", variable.name, to_str(variable.value, flags_=flags_), flags_=flags_))


def _process_constraints(ir, src, flags_):
    for c in ir.constraints:
        # some constraints, e.g. set value are directly added as strings
        src.append(f"constraint {to_str(c, flags_=flags_)};")


def _process_how_to_solve(ir, result):
    how_to_solve = ir.how_to_solve
    if isinstance(how_to_solve, tuple):
        if len(how_to_solve) == 2:
            result.append(f"solve {how_to_solve[0]} {to_str(how_to_solve[1])};")
            return
        assert len(how_to_solve) == 1
        how_to_solve = how_to_solve[0]
    if isinstance(how_to_solve, str):
        result.append(f"solve {how_to_solve};")
        return
    assert False, "{} how to solve is unknown".format(ir.how_to_solve)  # pragma: no cover
