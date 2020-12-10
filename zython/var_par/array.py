from zython import var


class Array(var):
    def __init__(self, arg, shape):
        # TODO: support other then 1d shape
        self._type = None
        self._name = None
        self._value = None
        if isinstance(arg, var):
            self._type = arg.type  # var._type isn't working for some reasons
            self._shape = shape
        else:
            raise ValueError("Arrays either then var are not supported")
        pass

    @property
    def shape(self):
        return self._shape

    def __getitem__(self, item):
        if item >= len(self):
            raise StopIteration
        return _ArrayVar(self, item)

    def __len__(self):
        return self.shape


class _ArrayVar(var):
    def __init__(self, array, pos):
        self.array = array
        self.pos = pos
        self._type = array.type
        self._name = None
        self._value = None
        # TODO: check out of the bound
