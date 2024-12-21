import inspect

from .abstract import _AbstractCollection
from ..par import par
from ..get_type import is_range, is_enum
from ..var import var


class SetMixin(_AbstractCollection):
    @staticmethod
    def _validate_type(type_):
        if type_ is not int and not is_range(type_) and not is_enum(type_):
            raise ValueError(f"Unsupported type for set: {type(type_)}")


class SetVar(var, SetMixin):
    def __init__(self, arg):
        type_ = arg.type
        self._validate_type(type_)
        self._type = type_
        self._value = None
        self._name = None


class SetPar(par, SetMixin):
    def __init__(self, arg):
        if inspect.isgenerator(arg):
            arg = tuple(arg)
        if len(arg) < 1:
            raise ValueError("Set should be initialized with not empty collection")
        # TODO: single dispatch
        if isinstance(arg, (tuple, list)):
            if len(arg) < 1:
                raise ValueError("Set should be initialized with not empty collection")
            type_ = type(arg[0])
        elif isinstance(arg, set):
            elem = next(iter(arg))  # get set item without removing it
            type_ = type(elem)
        else:
            type_ = arg
        self._validate_type(type_)
        self._type = type_
        self._value = arg
        self._name = None


class Set(SetMixin):
    def __new__(cls, arg, /):
        if isinstance(arg, var):
            return SetVar(arg)
        else:
            return SetPar(arg)
