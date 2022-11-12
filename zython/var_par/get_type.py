import enum
from functools import singledispatch

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
