from collections import deque

from zython import var


class Array(var):
    def __init__(self, arg, shape=None):  # TODO: make positional only
        # TODO: support other then 1d shape
        self._type = None
        self._name = None
        self._value = None
        if isinstance(arg, var):
            self._type = arg.type
            self._shape = shape if isinstance(shape, tuple) else (shape, )
        else:
            self._create_array(arg)
        if self._type is None:
            raise ValueError(f"var or sequence is expected as the first argument, but {type(arg)} was passed")

    def _create_array(self, arg):
        shape = []
        queue = deque()
        level = 0
        old_length = 0
        length = 0
        while self._can_create_array_from(arg):
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
        values = [arg]
        if not isinstance(arg, int):
            raise ValueError("Only array with dtype int are supported")
        self._type = type(arg)
        for val, new_level in queue:
            if not isinstance(val, self._type):
                raise ValueError(f"All elements of the array should be the same type, "
                                 f"but {self._type} and {type(val)} were found")
            if self._can_create_array_from(val) or level != new_level:
                raise ValueError("Subarrays of different length are not supported")
            values.append(val)
        self._value = tuple(values)
        self._shape = tuple(shape)

    @property
    def shape(self):
        return self._shape

    @property
    def value(self):
        return self._value

    def __len__(self):
        return self.shape[0]

    def __getitem__(self, item):
        return ArrayView(self, item)

    def _can_create_array_from(self, arg):
        return hasattr(arg, "__iter__") or hasattr(arg, "__getitem__") and (not isinstance(arg, str))


class ArrayView(Array):
    def __init__(self, array, pos):
        self.array = array
        self.pos = pos if isinstance(pos, tuple) else (pos, )
        self._type = array.type

    @property
    def name(self):
        return self.array.name
