from zython.operations.constraint.constraint import Constraint
from zython.var_par.array import ArrayView


class all_different(Constraint):
    # TODO: array support?
    def __init__(self, *params):
        super().__init__(_all_different, params)


def _all_different(args):
    return f"alldifferent([{', '.join(v.name for v in args)}])"


class sum(Constraint):
    def __init__(self, array, /):
        super().__init__(_sum, array)
        self._type = array.type


def _sum(arg, /):
    if isinstance(arg, ArrayView):
        iterators = []
        indexes = []
        i = 0
        level = 0
        for level, pos in enumerate(arg.pos):
            if isinstance(pos, slice):
                if pos.step is not None and pos.step != 1:
                    raise ValueError("step isn't suported for now")
                var_name = f"i{i}__"
                stop = pos.stop - 1 if pos.stop else arg.array.shape[level] - 1
                start = pos.start if pos.start else 0
                if start > stop:
                    raise ValueError("start should be smaller then stop")
                iterators.append(f"{var_name} in {start}..{stop}")
                i += 1
            elif isinstance(pos, int):
                var_name = str(pos)
            else:
                raise ValueError("Only int and slice are supported as indexes")
            indexes.append(var_name)
        for level in range(level + 1, len(arg.array.shape)):
            var_name = f"i{level}__"
            indexes.append(var_name)
            iterators.append(f"{var_name} in 0..{arg.array.shape[level] - 1}")
        return f"sum({', '.join(iterators)})({arg.array.name}[{', '.join(indexes)}])"
    return f"sum({arg.name})"
