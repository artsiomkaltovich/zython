from typing import Type, Optional

from zython.operations import operation


class _AbstractCollection(operation.Operation):
    # TODO: _AbstractCollection subclass Operation and Constraint
    # so invert of collection is possible, restrict it
    _name: Optional[str]
    name: str  # remove pycharm warnings, this property is handled by var\par base class
    _type: Type

    @property
    def type(self):
        return self._type

    def contains(self, item):
        return operation._in(item, self)
