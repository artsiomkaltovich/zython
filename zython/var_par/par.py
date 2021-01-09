from zython import var
from zython.operations.constraint import Constraint


class par(var):
    def __init__(self, value):  # TODO: make positional onlyif isinstance(type_or_value, int):
        self._name = None
        self._value = None
        self._type = None
        if isinstance(value, int):
            self._type = int
            self._value = value
        elif isinstance(value, Constraint):
            self._type = value.type
            self._value = value
        if self._type is None:
            raise ValueError(f"{value} is a variable of unsupported type")

    def __repr__(self):
        return f"par({self._type}: {self._name} = {self.value})"
