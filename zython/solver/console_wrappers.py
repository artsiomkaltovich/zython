from typing import Tuple

import minizinc as mz


def available_solver_tags(refresh: bool = False) -> Tuple[str, ...]:
    """ Returns tags of available solvers

    Parameters
    ----------
    refresh: bool
        refresh inner cache or not

    Examples
    --------
    > available_solver_tags()
    ('cp', 'lcg', 'gecode', ...)

    Notes
    -----
    1. The method calls minizinc cli
    2. The list of solvers might be cached for future usage.
        The refresh argument can be used to ignore the current cache.
    """
    return tuple(mz.default_driver.available_solvers(refresh=refresh).keys())
