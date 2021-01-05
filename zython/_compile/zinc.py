import enum
import inspect
from collections import UserDict, deque
from typing import Union

from zython import var
from zython._compile.ir import IR
from zython.operations.all_ops import Op
from zython.operations.constraint.constraint import Constraint
from zython.var_par.array import ArrayView, ArrayMixin
from zython.var_par.types import is_range


class Flags(enum.Enum):
    none = enum.auto()
    alldifferent = enum.auto()


def to_zinc(ir: IR):
    result = deque()
    flags = set()
    _process_pars(ir, result, flags)
    _process_vars(ir, result, flags)
    _process_constraints(ir, result, flags)
    result.append(f"solve {ir.how_to_solve};")
    _process_flags(flags, result)
    return "\n".join(result)


def _process_flags(flags, result):
    if Flags.alldifferent in flags:
        result.appendleft('include "alldifferent.mzn";')


def _process_pars_and_vars(ir, vars_or_pars, src, decl_prefix, flags):
    if not decl_prefix.endswith(" "):
        decl_prefix += " "
    for v in vars_or_pars.values():
        # TODO: check reserved word are not used as variable name
        declaration = ""
        if isinstance(v, ArrayMixin):
            declaration = f"array[{_get_array_shape_decl(v._shape)}] of "  # TODO: refactor var vs par
        if v.type is int:
            declaration += f"{decl_prefix}int: {v.name};"
        elif is_range(v.type):
            declaration += f"{decl_prefix}{_to_str(v.type.start)}..{_to_str(v.type.stop - 1)}: {v.name};"
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
    ir.constraints.append(_eq(variable.name, _get_value_decl(variable), flags_=flags))


def _get_array_shape_decl(shape):
    result = [f'0..{s - 1}' for s in shape]
    return f"{', '.join(result)}"


def _process_constraints(ir, src, flags):
    for c in ir.constraints:
        # some constraints, e.g. set value are directly added as strings
        src.append(f"constraint {_to_str(c, flags)};")


def _get_value_decl(variable):
    if isinstance(variable.value, tuple):
        # TODO: support 2 and more d
        return f"array{len(variable._shape)}d({_get_array_shape_decl(variable._shape)}, " \
               f"[{', '.join(str(v) for v in variable.value)}])"
    return _to_str(variable.value)


def _to_str(constraint, flags=None):
    if isinstance(constraint, ArrayView):
        return _array_view_to_str(constraint)
    elif isinstance(constraint, var):
        return constraint.name
    elif isinstance(constraint, Constraint):
        return Op2Str[constraint.op](*constraint.params, flags_=flags)
    return str(constraint)


def _array_view_to_str(view):
    if isinstance(view.pos, tuple):
        if len(view.pos) != len(view.array._shape):
            raise ValueError("Accessing of subarrays are not supported in such operations, please use zn.forall "
                             "or specify index of element")
        return f"{view.array.name}[{', '.join(_to_str(p) for p in view.pos)}]"
    elif isinstance(view.pos, slice):
        raise ValueError("slices are not supported in such operations, please use zn.forall")
    else:
        raise ValueError(f"Only int and tuples supported as indexes, but {type(view.pos)} was used")


def _pow(a, b, *, flags_):  # TODO: make positional only
    return f"pow({_to_str(a)}, {_to_str(b)})"


def _mul(a, b, *, flags_):
    return f"({_to_str(a)} * {_to_str(b)})"


def _truediv(a, b, *, flags_):
    return f"({_to_str(a)} / {_to_str(b)})"


def _floatdiv(a, b, *, flags_):
    return f"({_to_str(a)} div {_to_str(b)})"


def _mod(a, b, *, flags_):
    return f"({_to_str(a)} mod {_to_str(b)})"


def _add(a, b, *, flags_):
    return f"({_to_str(a)} + {_to_str(b)})"


def _sub(a, b, *, flags_):
    return f"({_to_str(a)} - {_to_str(b)})"


def _eq(a, b, *, flags_):
    return f"({_to_str(a)} == {_to_str(b)})"


def _ne(a, b, *, flags_):
    return f"({_to_str(a)} != {_to_str(b)})"


def _lt(a, b, *, flags_):
    return f"({_to_str(a)} < {_to_str(b)})"


def _gt(a, b, *, flags_):
    return f"({_to_str(a)} > {_to_str(b)})"


def _le(a, b, *, flags_):
    return f"({_to_str(a)} <= {_to_str(b)})"


def _ge(a, b, *, flags_):
    return f"({_to_str(a)} >= {_to_str(b)})"


def _xor(a, b, *, flags_):
    return f"({_to_str(a)} xor {_to_str(b)})"


def _or(a, b, *, flags_):
    return f"({_to_str(a)} \\/ {_to_str(b)})"


def _and(a, b, *, flags_):
    return f"({_to_str(a)} /\\ {_to_str(b)})"


def _forall(seq, func, *, flags_):
    func_str, indexes = _get_indexes_and_cycle_body(seq, func, flags_)
    return f"forall({indexes})({func_str})"


def _exists(seq, func, *, flags_):
    func_str, indexes = _get_indexes_and_cycle_body(seq, func, flags_)
    return f"exists({indexes})({func_str})"


def _alldifferent(args, *, flags_):
    flags_.add(Flags.alldifferent)
    if isinstance(args[0], ArrayMixin):
        if len(args) > 1:
            raise ValueError("Several arrays are not supported")
        arg = args[0]
        def_, indexes = _get_indexes_def(arg)
        return f"alldifferent([{arg.name}[{', '.join(indexes)}] | {', '.join(def_)}])"
    return f"alldifferent([{', '.join(v.name for v in args)}])"


def _sum(arg, *, flags_):
    if isinstance(arg, ArrayView):
        iterators, indexes = _get_indexes_def(arg)
        return f"sum({', '.join(iterators)})({arg.array.name}[{', '.join(indexes)}])"
    elif isinstance(arg, ArrayMixin):
        return f"sum({arg.name})"
    else:
        raise ValueError(f"Only arrays and array views are supported as sum argument, but {type(arg)} was specified.")


def _size(array: ArrayMixin, dim: int, *, flags_):
    return f"max(index_set_{dim + 1}of{array.ndims()}({array.name})) + 1"


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
        self[Op.exists] = _exists
        self[Op.sum_] = _sum
        self[Op.size] = _size

    def __missing__(self, key):
        raise ValueError(f"Function {key} is undefined")


Op2Str = Op2Str()


def _get_indexes_and_cycle_body(seq, func, flags_):
    indexes, v = _get_indexes_def_and_func_arg(seq)
    if isinstance(func, Constraint):
        func_str = _to_str(func, flags_)
    else:
        func_str = _extract_func_body(flags_, func, v)
    indexes = indexes if indexes else f"{v.name} in {_to_str(seq.start, flags_)}..{_to_str(seq.stop - 1, flags_)}"
    return func_str, indexes


def _extract_func_body(flags_, func, v):
    parameters = inspect.signature(func).parameters
    if len(parameters) > 1:
        raise ValueError("only functions and lambdas with one arguments are supported")
    elif len(parameters) == 1:
        if v._name is None:
            v._name, _ = dict(inspect.signature(func).parameters).popitem()
        func_str = _to_str(func(v), flags_)
    else:
        func_str = _to_str(func(), flags_)
    return func_str


def _get_indexes_def_and_func_arg(seq):
    if is_range(seq):
        if seq.step != 1:
            raise ValueError("Step aren't supported")
        v = var(int)
        def_ = None
    elif isinstance(seq, ArrayMixin):
        def_, indexes = _get_indexes_def(seq)
        v = var(seq.type)
        v._name = f"{seq.name}[{', '.join(indexes)}]"
    else:
        raise ValueError(f"seq should be range, but {type(seq)} was specified")
    return def_, v


def _get_indexes_def(array: Union[ArrayMixin, ArrayView]):
    if isinstance(array, ArrayView):
        iterators = []
        indexes = []
        i = 0
        for level, pos in enumerate(array.pos):
            if isinstance(pos, slice):
                if pos.step is not None and pos.step != 1:
                    raise ValueError("step isn't suported for now")
                var_name = f"i{i}__"
                stop = pos.stop - 1 if pos.stop else array.array._shape[level] - 1
                start = pos.start if pos.start else 0
                if isinstance(start, int) and isinstance(stop, int) and start > stop:
                    raise ValueError(f"start ({start}) should be smaller then stop ({stop})")
                def_ = f"{var_name} in {_to_str(start)}..{_to_str(stop)}"
                iterators.append(def_)
                i += 1
            elif isinstance(pos, int):
                var_name = str(pos)
            elif isinstance(pos, var):
                var_name = pos.name
            else:
                raise ValueError("Only int and slice are supported as indexes")
            indexes.append(var_name)
        return iterators, indexes
    elif isinstance(array, ArrayMixin):
        indexes_ = [f"i{i}__" for i in range(len(array._shape))]
        return ", ".join(f"{index} in 0..{s - 1}" for index, s in zip(indexes_, array._shape)), indexes_
    else:
        raise ValueError(f"{type(array)} isn't supported")
