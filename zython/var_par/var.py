import inspect

from zython.operations._operation import _Operation
from zython.operations.constraint import Constraint


class var(_Operation):
    def __init__(self, type_or_value, /):
        self._name = None
        self._value = None
        self._type = type_or_value
        if isinstance(type_or_value, range):
            if type_or_value.step != 1:
                raise ValueError("Step values other than 1 are not supported")
            self._type = type_or_value
        elif isinstance(type_or_value, int):
            self._type = int
            self._value = type_or_value
        elif isinstance(type_or_value, Constraint):
            self._type = type_or_value.type
            self._value = type_or_value
        elif inspect.isclass(type_or_value):
            if issubclass(type_or_value, int):
                self._type = int
        if self._type is None:
            raise ValueError(f"{type_or_value} is a variable of unsupported type")

    @property
    def name(self):
        assert self._name, "name wasn't specified"
        return self._name

    @property
    def value(self):
        return self._value

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"var({self._type}: {self._name})"
