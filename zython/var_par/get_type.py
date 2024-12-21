import enum
from functools import singledispatch
import warnings

from zython.var_par.types import Ranges, RangesType, _range


def is_range(obj):
    return isinstance(obj, Ranges)


def is_int_range(r: RangesType):
    return all(get_type(s) is int for s in (r.start, r.stop, r.step))


def is_enum(arg):
    return isinstance(arg, enum.EnumMeta)


def get_type(arg):
    return getattr(arg, "type", type(arg))


@singledispatch
def get_base_type(arg):
    return get_base_type(arg.type)


@get_base_type.register
def _(arg: int):
    return int


@get_base_type.register
def _(arg: float):
    return float


@get_base_type.register
def _(arg: enum.EnumMeta):
    return int


@get_base_type.register
def _(arg: type):
    return arg


@get_base_type.register
def _(arg: range):
    return int


@get_base_type.register
def _(arg: _range):
    if is_int_range(arg):
        return int
    return float


def get_wider_type(left, right):
    t_types = get_base_type(left), get_base_type(right)
    types = set(t_types)
    if types == {int}:
        return int
    elif types == {int, float} or types == {float}:
        return float
    warnings.warn("_get_wider_type returns int as fallback")
    return int  # TODO: fix types, do not forget about int/int => float

def derive_operation_type(seq, operation): 
    from zython.var_par.collections.array import ArrayMixin
    if isinstance(seq, ArrayMixin) and operation is None:
        type_ = seq.type
    else:
        type_ = operation.type
    if type_ is None:
        raise ValueError(f"Can't derive the type of {seq=} {operation=} expression")
    return type_
