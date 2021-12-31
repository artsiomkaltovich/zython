from .abstract import _AbstractCollection
from ..par import par
from ..var import var


class SetMixin(_AbstractCollection):
    pass


class SetVar(var, SetMixin):
    def __init__(self, arg):
        self._type = arg.type
        self._value = None
        self._name = None


class SetPar(par, SetMixin):
    def __init__(self, arg):
        if len(arg) < 1:
            raise ValueError("Set should be initialized with not empty collection")
        self._value = arg
        self._type = arg
        self._name = None


class Set(_AbstractCollection):
    def __new__(cls, arg):  # TODO: make positional only
        if isinstance(arg, var):
            return SetVar(arg)
        else:
            return SetPar(arg)
