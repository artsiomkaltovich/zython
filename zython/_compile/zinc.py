import enum
import itertools
import types
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
    alldifferent_except_0 = enum.auto()
    all_equal = enum.auto()
    nvalue = enum.auto()
    circuit = enum.auto()
    increasing = enum.auto()
    strictly_increasing = enum.auto()
    decreasing = enum.auto()
    strictly_decreasing = enum.auto()


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
    for flag in flags:
        if flag is Flags.nvalue:
            result.appendleft('include "nvalue_fn.mzn";')
        else:
            result.appendleft(f'include "{flag.name}.mzn";')


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


@singledispatch
def to_str(stmt, *, flatten_arg=False, flags_=None):
    # order is important
    if isinstance(stmt, ArrayMixin):
        stmt = _compile_array_view(stmt) if isinstance(stmt, ArrayView) else stmt
        return _array_to_str(stmt, flatten=flatten_arg)
    elif isinstance(stmt, var):
        return stmt.name
    elif isinstance(stmt, Constraint):
        return Op2Str[stmt.op](*stmt.params, flags_=flags_)
    elif is_range(stmt):
        return _range_or_slice_to_str(stmt)
    return str(stmt)


@to_str.register(tuple)
@to_str.register(list)
@to_str.register(types.GeneratorType)
def _(stmt, *, flatten_arg=False, flags_=None):
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
    slices_pos = [isinstance(p, slice) for p in pos]
    slices_count = sum(slices_pos)
    if slices_count:
        slice_def, slices = _compile_slice(ndim, pos, view)
        if slices_count == len(pos):
            return slice_def
        elif slices_count == 1:
            return _flatt_array(slice_def)
        else:
            decrised_index_set = [i for i in itertools.compress(slices, slices_pos)]
            return _call_func(f"array{len(decrised_index_set)}d", *decrised_index_set, slice_def, flags_=None)
    else:
        assert all(isinstance(p, (Operation, int)) for p in pos)
        return f"{view.array.name}[{', '.join(to_str(p) for p in view.pos)}]"


def _flatt_array(array):
    return _call_func("array1d", array, flags_=None)


def _array_to_str(array, *, flatten=False):
    assert isinstance(array, (ArrayMixin, str))
    name = array if isinstance(array, str) else array.name
    if flatten:
        return _call_func("array1d", name, flags_=None)
    else:
        return name


def _compile_slice(ndim, pos, view):
    slices = [_fill_the_slice(p) for p in pos]
    slices_str = f"[{', '.join(_range_or_slice_to_str(s) for s in slices)}]"
    new_index_set = [_range_or_slice_to_str(range(s.stop - s.start)) for s in slices]
    new_index_set_str = ", ".join(new_index_set)
    return f"slice_{ndim}d({view.array.name}, {slices_str}, {new_index_set_str})", new_index_set


def _pow(a, b, *, flags_):  # TODO: make positional only
    return f"pow({to_str(a, flags_=flags_)}, {to_str(b, flags_=flags_)})"


def _binary_op(sign, a, b, *, flags_):
    return f"({to_str(a, flags_=flags_)} {sign} {to_str(b, flags_=flags_)})"


def _unary_op(sign, a, *, flags_):
    return f"({sign} {to_str(a, flags_=flags_)})"


def _two_brackets_op(op, seq, iter_var, operation, *, flags_):
    indexes, func_str = _get_indexes_and_cycle_body(seq, iter_var, operation, flags_)
    return f"{op}({indexes})({func_str})"


def _one_or_two_brackets(op, seq, iter_var, operation, *, flatten_args=False, flags_):
    if iter_var is None:
        return _call_func(op, seq, operation, flatten_args=flatten_args, flags_=flags_)
    else:
        return _two_brackets_op(op, seq, iter_var, operation, flags_=flags_)


def _call_func(func, *params, flatten_args=False, flags_):
    t = partial(to_str, flatten_arg=flatten_args, flags_=flags_)
    return f"{func}({', '.join(t(p) for p in params if p is not None)})"


def _size(array: ArrayMixin, dim: int, *, flags_):
    ndims = array.ndims()
    if ndims > 1:
        return f"(max(index_set_{dim + 1}of{ndims}({array.name})) + 1)"
    else:
        return f"(max(index_set({array.name})) + 1)"


def _global_constraint(constraint, *params, flags_, flatten_args=True):
    flags_.add(getattr(Flags, constraint))
    return _call_func(constraint, *params, flatten_args=flatten_args, flags_=flags_)


def _array_comprehension_call(op, seq, iter_var, operation, *, flags_):
    if iter_var is not None:
        return _call_func(op, _compile_array_comprehension(seq, iter_var, operation, flags_), flags_=flags_)
    else:
        return _call_func(op, seq, flags_=flags_)


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
        # minizinc 2.5.0 doesn't support 2d array counting
        self[_Op_code.count] = partial(_one_or_two_brackets, "count", flatten_args=True)
        self[_Op_code.sum_] = partial(_one_or_two_brackets, "sum")
        self[_Op_code.min_] = partial(_array_comprehension_call, "min")
        self[_Op_code.max_] = partial(_array_comprehension_call, "max")
        self[_Op_code.size] = _size
        self[_Op_code.alldifferent] = partial(_global_constraint, "alldifferent")
        self[_Op_code.alldifferent_except_0] = partial(_global_constraint, "alldifferent_except_0")
        self[_Op_code.allequal] = partial(_global_constraint, "all_equal")
        self[_Op_code.ndistinct] = partial(_global_constraint, "nvalue")
        self[_Op_code.circuit] = partial(_global_constraint, "circuit", flatten_args=False)
        self[_Op_code.increasing] = partial(_global_constraint, "increasing")
        self[_Op_code.strictly_increasing] = partial(_global_constraint, "strictly_increasing")
        self[_Op_code.decreasing] = partial(_global_constraint, "decreasing")
        self[_Op_code.strictly_decreasing] = partial(_global_constraint, "strictly_decreasing")

    def __missing__(self, key):  # pragma: no cover
        raise ValueError(f"Function {key} is undefined")


Op2Str = Op2Str()


def _get_indexes_and_cycle_body(seq, iter_var, func, flags_):
    return f"{iter_var.name} in {to_str(seq, flags_=flags_)}", to_str(func, flags_=flags_)


def _compile_array_comprehension(seq, iter_var, func, flags_):
    indexes, func_str = _get_indexes_and_cycle_body(seq, iter_var, func, flags_=flags_)
    return f"[{func_str} | {indexes}]"
