class IR:
    def __init__(self, model, how_to_solve):
        self._model = model
        self._vars = self._get_vars()
        self._src = None
        self._how_to_solve = how_to_solve

    @property
    def vars(self):
        return self._vars

    @property
    def constraints(self):
        return self._model.constraints

    @property
    def how_to_solve(self):
        return self._how_to_solve

    def _get_vars(self):
        result = {}
        for name, attr in vars(self._model).items():
            attr = self._model.get_var_attr(name, attr)
            if attr is not None:
                attr._name = name
                result[name] = attr
        return result
