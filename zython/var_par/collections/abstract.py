from typing import Type

from zython.operations import operation


class _AbstractCollection(operation.Operation):
    # TODO: _AbstractCollection subclass Operation and Constraint
    # so invert of collection is possible, restrict it
    _name: str
    name: str  # remove pycharm warnings, this property is handled by var\par base class
    _type: Type

    @property
    def type(self):
        return self._type
