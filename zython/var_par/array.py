import inspect
from collections import deque

from zython import var, par
from zython.operations._operation import _Operation


def _can_create_array_from(arg):
    return hasattr(arg, "__iter__") or hasattr(arg, "__getitem__") and (not isinstance(arg, str))


class ArrayMixin(_Operation):
    @property
    def name(self):
        assert self._name, "name wasn't specified"
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def shape(self):
        return self._shape

    def __len__(self):
        return self.shape[0]

    def __getitem__(self, item):
        return ArrayView(self, item)


class ArrayView(ArrayMixin):
    def __init__(self, array, pos):
        self.array = array
        self.pos = pos if isinstance(pos, tuple) else (pos, )
        self._type = array.type

    @property
    def name(self):
        return self.array.name


class ArrayVar(var, ArrayMixin):
    def __init__(self, arg, *, shape=None):
        self._type = arg.type
        self._value = None
        self._name = None
        self._shape = shape if isinstance(shape, tuple) else (shape, )


class ArrayPar(par, ArrayMixin):
    def __init__(self, arg):
        self._type = None
        self._name = None
        self._value = arg
        self._shape = None
        self._create_array(arg)
        if self._type is None:
            raise ValueError(f"var or sequence is expected as the first argument, but {type(arg)} was passed")

    def _create_array(self, arg):
        is_generator = inspect.isgenerator(arg)
        shape = []
        queue = deque()
        level = 0
        old_length = 0
        length = 0
        while _can_create_array_from(arg):
            old_length = length
            length = 0
            for a in arg:
                queue.append((a, level + 1))
                length += 1
            if not length:
                raise ValueError("Empty array was specified")
            arg, new_level = queue.popleft()
            if len(shape) <= level:
                shape.append(length)
            elif old_length != length:
                raise ValueError("Subarrays of different length are not supported, length of all subarrays "
                                 f"at level {level} should be {old_length}, but one has {length}")
            level = new_level
        if not isinstance(arg, int):
            raise ValueError("Only array with dtype int are supported")
        self._type = type(arg)
        values = [arg]
        self._check_and_set_values(is_generator, level, queue, values)
        self._shape = tuple(shape)

    def _check_and_set_values(self, is_generator, level, queue, values):
        for val, new_level in queue:
            if not isinstance(val, self._type):
                raise ValueError(f"All elements of the array should be the same type, "
                                 f"but {self._type} and {type(val)} were found")
            if _can_create_array_from(val) or level != new_level:
                raise ValueError("Subarrays of different length are not supported")
            values.append(val)
        if is_generator:
            self._value = values


class Array:
    def __new__(cls, arg, shape=None):  # TODO: make positional only
        if isinstance(arg, var):
            return ArrayVar(arg, shape=shape)
        else:
            if shape is not None:
                raise ValueError("shape is calculated from the value, you passed, do not specify it.")
            if _can_create_array_from(arg):
                return ArrayPar(arg)
            else:
                raise ValueError(f"Sequence of var is expected as parameter for array creation, "
                                 f"but {type(arg)} was passed")
