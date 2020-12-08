from zython.operations.constraint import Constraint


def _all(collection, /):
    # TODO: test
    constraints = []
    for c in collection:
        if isinstance(c, Constraint):
            constraints.append(c)
        else:
            if not c:
                return False
    if constraints:
        return constraints
    return True
