from collections import namedtuple


class Result:
    """ Represents model solution

    Warnings
    --------
    It is supposed this class is used by package itself only, there should be now need for user to create it,
    but they can use this class as base class for their purpose.

    """
    def __init__(self, mzn_result):
        self._original = mzn_result
        if mzn_result.solution:
            names = [name for name in vars(mzn_result.solution) if not name.startswith("_")]
            Solution = namedtuple("Solution", names)
            self._solution = Solution(*(mzn_result[name] for name in names))
        else:
            self._solution = None

    @property
    def original(self):
        return self._original

    def __getitem__(self, item):
        return self._original[item]

    def __str__(self):
        return str(self._solution)

    def __repr__(self):
        return str(self)
