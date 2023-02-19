import inspect

from zython.operations.operation import Operation
from zython.operations.constraint import Constraint
from zython.var_par.get_type import is_range, is_enum


class var(Operation):
    def __init__(self, /, type_, value=None):
        self._name = None
        self._value = value
        self._type = None
        if isinstance(type_, Constraint):
            self._type = type_.type
            self._value = type_
            if value is not None:
                raise ValueError("Can not pass value to constraint")
        else:
            if is_range(type_):
                if type_.step != 1:
                    raise ValueError("Step values other than 1 are not supported")
                self._type = type_
            elif is_enum(type_):
                self._type = type_
            elif inspect.isclass(type_):
                if issubclass(type_, int):
                    self._type = int
                if issubclass(type_, float):
                    self._type = float
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
