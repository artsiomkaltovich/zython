import inspect
import itertools
from collections import deque
from typing import Type

from zython import var, par
from zython._helpers.validate import _start_stop_step_validate
from zython.operations import operation


def _can_create_array_from(arg):
    return hasattr(arg, "__iter__") or hasattr(arg, "__getitem__") and (not isinstance(arg, str))


class ArrayMixin(operation.Operation):
    _shape: tuple
    _name: str
    name: str  # remove pycharm warnings, this property is handled by var\par base class
    _type: Type

    @property
    def type(self):
        return self._type

    def __getitem__(self, item):
        return ArrayView(self, item)

    def ndims(self):
        return len(self._shape)

    def size(self, dim=0):
        """ returns constraint, which is evaluated as the number of items in the specified dimension of the array.

        Parameters
        ----------
        dim: int
            dimension of the array

        Returns
        -------
        size: Operation
            Operation which is evaluated as number of the items in specified dimension by the model
        """
        return operation._size(self, dim)


class ArrayView(ArrayMixin):
    def __init__(self, array, pos):
        self.array: ArrayMixin = array
        # pos is a tuple with the same size as number of array dimensions, the user can specify less iterators,
        # slice(None, None, 1) will be added to fit the number of dimensions, so compilers shouldn't worry about it
        self.pos = self._get_pos(pos)
        self._type = array.type

    def _get_pos(self, pos):
        if not isinstance(pos, tuple):
            pos = [pos]
        self._check_for_index_error(pos)
        repeat = itertools.repeat(slice(None, None, 1), self.array.ndims() - len(pos))
        pos = tuple(self._process_pos_item(dim, p) for dim, p in enumerate(itertools.chain(pos, repeat)))
        if len(pos) > self.array.ndims():
            raise ValueError(f"Array has {self.array.ndims()} dimensions but {len(pos)} were specified")
        return pos

    def _check_for_index_error(self, pos):
        for p, s in zip(pos, self.array._shape):
            if isinstance(p, int):
                if p >= s:
                    raise IndexError()

    @property
    def name(self):
        return self.array.name

    def _is_neg_index(self, p):
        if isinstance(p, int) and p < 0:
            raise ValueError(f"Negative indexes are not supported for now, but {p} was specified")

    def _process_pos_item(self, dim, p):
        if isinstance(p, slice):
            self._is_neg_index(p.start)
            self._is_neg_index(p.stop)
            start = p.start if p.start is not None else 0
            stop = p.stop if p.stop is not None else self.array.size(dim)
            step = p.step if p.step is not None else 1
            p = slice(start, stop, step)
            _start_stop_step_validate(p)
        else:
            self._is_neg_index(p)
        return p


class ArrayVar(var, ArrayMixin):
    def __init__(self, arg, *, shape=None):
        if not shape:
            raise ValueError("shape wasn't specified")
        self._type = arg.type
        self._value = None
        self._name = None
        self._shape = shape if isinstance(shape, tuple) else (shape,)


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
        self._shape = tuple(shape)
        self._check_and_set_values(arg, is_generator, level, queue)

    def _check_and_set_values(self, arg, is_generator, level, queue):
        flatten_values = [arg]
        for val, new_level in queue:
            if not isinstance(val, self._type):
                raise ValueError(f"All elements of the array should be the same type, "
                                 f"but {self._type} and {type(val)} were found")
            if _can_create_array_from(val) or level != new_level:
                raise ValueError("Subarrays of different length are not supported")
            flatten_values.append(val)
        if is_generator:
            self._value = self._flatten_to_shaped(flatten_values)

    def _flatten_to_shaped(self, flatten_values):
        if len(self._shape) > 1:
            values = []
            for s in reversed(self._shape[1:]):
                values = []
                start = 0
                end = 0
                while end < len(flatten_values):
                    end = start + s
                    values.append(flatten_values[start:end])
                    start = end
                flatten_values = values
            return values
        else:
            return flatten_values


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
