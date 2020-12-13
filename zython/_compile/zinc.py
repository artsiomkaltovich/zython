import inspect
from collections import UserDict
from typing import Union

import zython as zn
from zython import var
from zython._compile.flags import Flag
from zython._compile.ir import IR
from zython.operations._operation import _Operation
from zython.operations.all_ops import Op
from zython.operations.constraint.constraint import Constraint
from zython.var_par.array import ArrayView, Array


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
        # some constraints, e.g. set value are directly added as strings
        src.append(f"constraint {_to_str(c)};")


def _set_value_as_constraint(ir, variable):
    # values should be set as constraint or it won't be returned
    ir.constraints.append(_eq(variable.name, _get_value_decl(variable)))


def _get_value_decl(variable):
    if isinstance(variable.value, tuple):
        # TODO: support 2 and more d
        return f"array{len(variable.shape)}d({_get_array_shape_decl(variable.shape)}, " \
               f"[{', '.join(str(v) for v in variable.value)}])"
    return _to_str(variable.value)


def _to_str(constraint):
    if isinstance(constraint, ArrayView):
        return _array_view_to_str(constraint)
    elif isinstance(constraint, var):
        return constraint.name
    elif isinstance(constraint, Constraint):
        return constraint if isinstance(constraint, str) else Op2Str[constraint.op](*constraint.params)
    return str(constraint)


def _array_view_to_str(view):
    if hasattr(view.pos, "__index__") or isinstance(view.pos, _Operation):
        if len(view.array.shape) > 1:
            raise ValueError("Accessing of subarrays are not supported in such operations, please use zn.forall "
                             "or specify index of element")
        return f"{view.array.name}[{_to_str(view.pos)}]"
    elif isinstance(view.pos, tuple):
        if len(view.pos) != len(view.array.shape):
            raise ValueError("Accessing of subarrays are not supported in such operations, please use zn.forall "
                             "or specify index of element")
        return f"{view.array.name}{(f'[{p}]' for p in view.pos)}"
    elif isinstance(view.pos, slice):
        raise ValueError("slices are not supported in such operations, please use zn.forall")
    else:
        raise ValueError(f"Only int and tuples supported as indexes, but {type(view.pos)} was used")


def _pow(a, b, /):
    return f"pow({_to_str(a)}, {_to_str(b)})"


def _mul(a, b, /):
    return f"({_to_str(a)} * {_to_str(b)})"


def _truediv(a, b, /):
    return f"({_to_str(a)} / {_to_str(b)})"


def _floatdiv(a, b, /):
    return f"({_to_str(a)} div {_to_str(b)})"


def _mod(a, b, /):
    return f"({_to_str(a)} mod {_to_str(b)})"


def _add(a, b, /):
    return f"({_to_str(a)} + {_to_str(b)})"


def _sub(a, b, /):
    return f"({_to_str(a)} - {_to_str(b)})"


def _eq(a, b, /):
    return f"({_to_str(a)} == {_to_str(b)})"


def _ne(a, b, /):
    return f"({_to_str(a)} != {_to_str(b)})"


def _lt(a, b, /):
    return f"({_to_str(a)} < {_to_str(b)})"


def _gt(a, b, /):
    return f"({_to_str(a)} > {_to_str(b)})"


def _le(a, b, /):
    return f"({_to_str(a)} <= {_to_str(b)})"


def _ge(a, b, /):
    return f"({_to_str(a)} >= {_to_str(b)})"


def _xor(a, b, /):
    return f"({_to_str(a)} xor {_to_str(b)})"


def _or(a, b, /):
    return f"({_to_str(a)} \\/ {_to_str(b)})"


def _and(a, b, /):
    return f"({_to_str(a)} /\\ {_to_str(b)})"


def _forall(seq, func):
    indexes, v = _get_indexes_def_and_func_arg(seq)

    parameters = inspect.signature(func).parameters
    if len(parameters) > 1:
        raise ValueError("only functions and lambdas with one arguments are supported")
    elif len(parameters) == 1:
        if v._name is None:
            v._name, _ = dict(inspect.signature(func).parameters).popitem()
        func_str = _to_str(func(v))
    else:
        func_str = _to_str(func())
    indexes = indexes if indexes else f"{v.name} in {seq.start}..{seq.stop - 1}"
    return f"forall({indexes}){func_str}"


def _get_indexes_def_and_func_arg(seq):
    if isinstance(seq, range):
        if seq.step != 1:
            raise ValueError("Step aren't supported")
        v = var(int)
        def_ = None
    elif isinstance(seq, ArrayView):
        # TODO: support
        raise ValueError(f"seq should be range, but {type(seq)} was specified")
    elif isinstance(seq, Array):
        def_, indexes = _get_indexes_def(seq)
        v = var(seq.type)
        v._name = f"{seq.name}[{', '.join(indexes)}]"
    else:
        raise ValueError(f"seq should be range, but {type(seq)} was specified")
    return def_, v


def _alldifferent(args):
    return f"alldifferent([{', '.join(v.name for v in args)}])"


def _sum(arg, /):
    if isinstance(arg, ArrayView):
        iterators = []
        indexes = []
        i = 0
        level = 0
        for level, pos in enumerate(arg.pos):
            if isinstance(pos, slice):
                if pos.step is not None and pos.step != 1:
                    raise ValueError("step isn't suported for now")
                var_name = f"i{i}__"
                stop = pos.stop - 1 if pos.stop else arg.array.shape[level] - 1
                start = pos.start if pos.start else 0
                if start > stop:
                    raise ValueError("start should be smaller then stop")
                iterators.append(f"{var_name} in {start}..{stop}")
                i += 1
            elif isinstance(pos, int):
                var_name = str(pos)
            else:
                raise ValueError("Only int and slice are supported as indexes")
            indexes.append(var_name)
        for level in range(level + 1, len(arg.array.shape)):
            var_name = f"i{level}__"
            indexes.append(var_name)
            iterators.append(f"{var_name} in 0..{arg.array.shape[level] - 1}")
        return f"sum({', '.join(iterators)})({arg.array.name}[{', '.join(indexes)}])"
    return f"sum({arg.name})"


class Op2Str(UserDict):
    def __init__(self):
        self.data = {}
        self[Op.add] = _add
        self[Op.sub] = _sub
        self[Op.eq] = _eq
        self[Op.ne] = _ne
        self[Op.lt] = _lt
        self[Op.gt] = _gt
        self[Op.le] = _le
        self[Op.ge] = _ge
        self[Op.xor] = _xor
        self[Op.and_] = _and
        self[Op.or_] = _or
        self[Op.mul] = _mul
        self[Op.truediv] = _truediv
        self[Op.floatdiv] = _floatdiv
        self[Op.mod] = _mod
        self[Op.pow] = _pow
        self[Op.alldifferent] = _alldifferent
        self[Op.forall] = _forall
        self[Op.sum_] = _sum


Op2Str = Op2Str()


def _get_indexes_def(array: Union[Array, ArrayView]):
    if isinstance(array, ArrayView):
        raise ValueError("ArrayView isn't supported")
    elif isinstance(array, Array):
        indexes_ = [f"i{i}__" for i in range(len(array.shape))]
        return ", ".join(f"{index} in 0..{s - 1}" for index, s in zip(indexes_, array.shape)), indexes_
    else:
        raise ValueError(f"{type(array)} isn't supported")
