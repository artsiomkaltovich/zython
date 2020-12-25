from zython import var
from zython.var_par.par import par


class IR:
    def __init__(self, model, how_to_solve):
        self.flags = set()
        self._model = model
        _vars, _pars = self._get_vars_and_pars()
        self._vars = _vars
        self._pars = _pars
        self._process_constraints(model)
        self._src = None
        self._how_to_solve = how_to_solve

    @property
    def vars(self):
        return self._vars

    @property
    def pars(self):
        return self._pars

    @property
    def constraints(self):
        return self._model.constraints

    @property
    def how_to_solve(self):
        return self._how_to_solve

    def _get_vars_and_pars(self):
        _vars = {}
        _pars = {}
        for name, attr in vars(self._model).items():
            attr = self._model._get_var_or_par_attr(name, attr)
            if isinstance(attr, par):
                attr._name = name
                _pars[name] = attr
            elif isinstance(attr, var):
                attr._name = name
                _vars[name] = attr
        return _vars, _pars

    def _process_constraints(self, model):
        if not hasattr(model, "_constraints"):
            model._constraints = []
