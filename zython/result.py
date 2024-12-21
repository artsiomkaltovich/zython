from collections import namedtuple
from functools import singledispatch
from typing import Any
import typing

import minizinc


class Result:
    """Represents model solution

    Warnings
    --------
    It is supposed this class is used by package itself only, there should be no need for user to create it,
    but they can use this class as base class for their extensions.

    """

    def __init__(self, mzn_result: minizinc.Result):
        self._original = mzn_result
        if mzn_result.solution is not None:
            if isinstance(mzn_result.solution, list):
                if mzn_result.solution:
                    # several solutions
                    names, Solution = _generate_solution_class_and_field_names(
                        mzn_result.solution[0]
                    )
                    solutions = []
                    for i in range(len(mzn_result.solution)):
                        solutions.append(
                            Solution(
                                *convert_result_value(
                                    (mzn_result[i, name]) for name in names
                                )
                            )
                        )
                    self._solution = solutions
                else:
                    # no solutions while all_solutions=True
                    self._solution = None
            else:
                names, Solution = _generate_solution_class_and_field_names(mzn_result.solution)
                self._solution = Solution(
                    *(convert_result_value(mzn_result[name]) for name in names)
                )
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


def as_original(mzn_result: minizinc.Result):
    """Returns original result, returned by minizinc-python"""
    return mzn_result


@singledispatch
def convert_result_value(value: Any) -> Any:
    return value


@convert_result_value.register
def _(value: float) -> float:
    return -value if value == -0.0 else value


def _generate_solution_class_and_field_names(
    mzn_solution,
) -> typing.Tuple[typing.Tuple[str, ...], typing.NamedTuple]:
    names = [name for name in vars(mzn_solution) if not name.startswith("_")]
    Solution = namedtuple("Solution", names)
    return names, Solution
