from zython import var


class Array(var):
    def __init__(self, arg, /, shape=None):
        # TODO: support other then 1d shape
        self._type = None
        self._name = None
        self._value = None
        if isinstance(arg, var):
            self._type = arg.type
            self._shape = shape if isinstance(shape, tuple) else (shape, )
        elif hasattr(arg, "__iter__") or hasattr(arg, "__getitem__"):
            self._value = tuple(arg)
            if not self._value:
                raise ValueError("Empty array was specified")
            self._shape = (len(self._value), )
            self._type = type(self._value[0])
        else:
            raise ValueError(f"var or sequence is expected as the first argument, but {type(arg)} was passed")
        pass

    @property
    def shape(self):
        return self._shape

    @property
    def value(self):
        return self._value

    def __len__(self):
        return self.shape[0]
