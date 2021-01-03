import inspect

from zython.operations._operation import _Operation
from zython.operations.constraint.constraint import Constraint


class var(_Operation):
    def __init__(self, type_):  # TODO: make positional only
        self._name = None
        self._value = None
        if isinstance(type_, Constraint):
            self._type = type_.type
            self._value = type_
        else:
            if isinstance(type_, range):
                if type_.step != 1:
                    raise ValueError("Step values other than 1 are not supported")
                self._type = type_
            elif inspect.isclass(type_):
                if issubclass(type_, int):
                    self._type = int
        if self._type is None:
            raise ValueError(f"{type_} is a variable of unsupported type")

    @property
    def name(self):
        assert self._name, "name wasn't specified"
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    def __repr__(self):
        return f"var({self._type}: {self._name})"
