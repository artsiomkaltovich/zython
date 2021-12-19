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
        print(type(arg))
        self._type = None
        self._name = None
        self._value = arg


class Set(_AbstractCollection):
    def __new__(cls, arg):  # TODO: make positional only
        if isinstance(arg, var):
            return SetVar(arg)
        else:
            return SetPar(arg)
