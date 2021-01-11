import enum
from collections import UserDict, deque
from functools import singledispatch, partial

from zython import var
from zython._compile.ir import IR
from zython._helpers.validate import _start_stop_step_validate
from zython.operations._op_codes import _Op_code
from zython.operations.constraint import Constraint
from zython.operations.operation import Operation
from zython.var_par.array import ArrayView, ArrayMixin
from zython.var_par.types import is_range


class Flags(enum.Enum):
    none = enum.auto()
    alldifferent = enum.auto()
    circuit = enum.auto()


def to_zinc(ir: IR):
    result = deque()
    flags = set()
    _process_pars(ir, result, flags)
    _process_vars(ir, result, flags)
    _process_constraints(ir, result, flags)
    _process_how_to_solve(ir, result)
    _process_flags(flags, result)
    return "\n".join(result)


def _process_flags(flags, result):
    if Flags.alldifferent in flags:
        result.appendleft('include "alldifferent.mzn";')
    if Flags.circuit in flags:
        result.appendleft('include "circuit.mzn";')


def _process_pars_and_vars(ir, vars_or_pars, src, decl_prefix, flags):
    for v in vars_or_pars.values():
        # TODO: check reserved word are not used as variable name
        declaration = ""
        if isinstance(v, ArrayMixin):
            declaration = f"array[{_get_array_shape_decl(v._shape)}] of "  # TODO: refactor var vs par
        if v.type is int:
            declaration += f"{decl_prefix} int: {v.name};"
        elif is_range(v.type):
            declaration += f"{decl_prefix} {to_str(v.type)}: {v.name};"
        else:
            raise TypeError(f"Type {v.type} are not supported, please specify int or range")
        src.append(declaration)
        if isinstance(v.value, Constraint):
            _set_value_as_constraint(ir, v, flags)


def _process_pars(ir, src, flags):
    _process_pars_and_vars(ir, ir.pars, src, "", flags)


def _process_vars(ir, src, flags):
    _process_pars_and_vars(ir, ir.vars, src, "var", flags)


def _set_value_as_constraint(ir, variable, flags):
    # values like `var int: s = sum(a);` should be set as constraint or it won't be returned in result
    ir.constraints.append(_binary_op("==", variable.name, to_str(variable.value), flags_=flags))


def _get_array_shape_decl(shape):
    result = [f'0..{s - 1}' for s in shape]
    return f"{', '.join(result)}"


def _process_constraints(ir, src, flags):
    for c in ir.constraints:
        # some constraints, e.g. set value are directly added as strings
        src.append(f"constraint {to_str(c, flags)};")


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


@singledispatch
def to_str(stmt, flags=None):
    # order is important
    if isinstance(stmt, ArrayView):
        return _compile_array_view(stmt)
    elif isinstance(stmt, var):
        return stmt.name
    elif isinstance(stmt, Constraint):
        return Op2Str[stmt.op](*stmt.params, flags_=flags)
    elif is_range(stmt):
        return _range_or_slice_to_str(stmt)
    return str(stmt)


@to_str.register(tuple)
@to_str.register(list)
def _(stmt, flags=None):
    return f"[{', '.join(to_str(s) for s in stmt)}]"


def _range_or_slice_to_str(stmt):
    _start_stop_step_validate(stmt)
    return f"{to_str(stmt.start)}..{to_str(stmt.stop - 1)}"


@singledispatch
def _fill_the_slice(stmt):
    assert isinstance(stmt, (Operation, int))
    return slice(stmt, stmt + 1, 1)


@_fill_the_slice.register(slice)
def _(obj):
    return obj


def _compile_array_view(view):
    pos = view.pos
    ndim = len(view.pos)
    assert isinstance(pos, tuple), "Array index should be converted to tuple by IR class"
    assert ndim == len(view.array._shape), "Array index should specify all dimensions, see ArrayView.__init__"
    if any(isinstance(p, slice) for p in pos):
        slices = [_fill_the_slice(p) for p in pos]
        slices_str = f"[{', '.join(_range_or_slice_to_str(s) for s in slices)}]"
        new_index_set = ", ".join(_range_or_slice_to_str(range(s.stop - s.start)) for s in slices)
        return f"slice_{ndim}d({view.array.name}, {slices_str}, {new_index_set})"
    else:
        assert all(isinstance(p, (Operation, int)) for p in pos)
        return f"{view.array.name}[{', '.join(to_str(p) for p in view.pos)}]"


def _pow(a, b, *, flags_):  # TODO: make positional only
    return f"pow({to_str(a)}, {to_str(b)})"


def _binary_op(sign, a, b, *, flags_):
    return f"({to_str(a)} {sign} {to_str(b)})"


def _unary_op(sign, a, *, flags_):
    return f"({sign}{to_str(a)})"


def _two_brackets_op(op, seq, iter_var, operation, *, flags_):
    indexes, func_str = _get_indexes_and_cycle_body(seq, iter_var, operation, flags_)
    return f"{op}({indexes})({func_str})"


def _one_or_two_brackets(op, seq, iter_var, operation, *, flags_):
    if iter_var is None:
        return _call_func(op, seq, operation, flags_=flags_)
    else:
        return _two_brackets_op(op, seq, iter_var, operation, flags_=flags_)


def _call_func(func, *params, flags_):
    return f"{func}({', '.join(to_str(p) for p in params if p is not None)})"


def _size(array: ArrayMixin, dim: int, *, flags_):
    ndims = array.ndims()
    if ndims > 1:
        return f"(max(index_set_{dim + 1}of{ndims}({array.name})) + 1)"
    else:
        return f"(max(index_set({array.name})) + 1)"


def _global_constraint(constraint, *params, flags_):
    flags_.add(getattr(Flags, constraint))
    return _call_func(constraint, *params, flags_=flags_)


class Op2Str(UserDict):
    def __init__(self):
        self.data = {}
        self[_Op_code.add] = partial(_binary_op, "+")
        self[_Op_code.sub] = partial(_binary_op, "-")
        self[_Op_code.eq] = partial(_binary_op, "==")
        self[_Op_code.ne] = partial(_binary_op, "!=")
        self[_Op_code.lt] = partial(_binary_op, "<")
        self[_Op_code.gt] = partial(_binary_op, ">")
        self[_Op_code.le] = partial(_binary_op, "<=")
        self[_Op_code.ge] = partial(_binary_op, ">=")
        self[_Op_code.xor] = partial(_binary_op, "xor")
        self[_Op_code.and_] = partial(_binary_op, "/\\")
        self[_Op_code.or_] = partial(_binary_op, "\\/")
        self[_Op_code.mul] = partial(_binary_op, "*")
        self[_Op_code.truediv] = partial(_binary_op, "/")
        self[_Op_code.floordiv] = partial(_binary_op, "div")
        self[_Op_code.mod] = partial(_binary_op, "mod")
        self[_Op_code.pow] = _pow
        self[_Op_code.invert] = partial(_unary_op, "not")
        self[_Op_code.forall] = partial(_two_brackets_op, "forall")
        self[_Op_code.exists] = partial(_two_brackets_op, "exists")
        self[_Op_code.count] = partial(_one_or_two_brackets, "count")
        self[_Op_code.sum_] = partial(_one_or_two_brackets, "sum")
        self[_Op_code.size] = _size
        self[_Op_code.alldifferent] = partial(_global_constraint, "alldifferent")
        self[_Op_code.circuit] = partial(_global_constraint, "circuit")

    def __missing__(self, key):  # pragma: no cover
        raise ValueError(f"Function {key} is undefined")


Op2Str = Op2Str()


def _get_indexes_and_cycle_body(seq, iter_var, func, flags_):
    return f"{iter_var.name} in {to_str(seq, flags_)}", to_str(func, flags_)
