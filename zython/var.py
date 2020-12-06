import inspect

from zython.operations import _Operation


class var(_Operation):
    def __init__(self, type_or_value, /):
        self._name = None
        if isinstance(type_or_value, range):
            # TODO: check for type in range
            # TODO: assert step
            self._type = type_or_value
            self._value = None
        elif isinstance(type_or_value, int):
            self._type = int
            self._value = type_or_value
        else:
            raise ValueError(f"{type_or_value} is a variable of unsupported type")

    @property
    def name(self):
        assert self._name, "name wasn't specified"
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    def __str__(self):
        return self.name
