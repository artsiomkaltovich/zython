from collections import namedtuple


class Result:
    """ Represents model solution

    Warnings
    --------
    It is supposed this class is used by package itself only, there should be no need for user to create it,
    but they can use this class as base class for their extensions.

    """
    def __init__(self, mzn_result):
        self._original = mzn_result
        if mzn_result.solution is not None:
            if isinstance(mzn_result.solution, list):
                if mzn_result.solution:
                    # several solutions
                    names = [name for name in vars(mzn_result.solution[0]) if not name.startswith("_")]
                    Solution = namedtuple("Solution", names)
                    solutions = []
                    for i in range(len(mzn_result.solution)):
                        solutions.append(Solution(*(mzn_result[i, name] for name in names)))
                    self._solution = solutions
                else:
                    # no solutions while all_solutions=True
                    self._solution = None
            else:
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

    def __len__(self):
        if self._solution is None:
            return 0
        elif isinstance(self._solution, list):
            return len(self._solution)
        else:
            return 1


def as_original(mnz_result):
    """ returns original result, returned by minizinc-python """
    return mnz_result
