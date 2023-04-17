import enum

from zython import var
from zython.var_par.par import par


class IR:
    def __init__(self, model, how_to_solve):
        self.flags = set()
        self._model = model
        self._enums = set()
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
    def enums(self):
        return self._enums

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
            if not attr:
                continue
            self._add_types(attr)
            attr._name = name
            if isinstance(attr, par):
                _pars[name] = attr
            elif isinstance(attr, var):
                _vars[name] = attr
        return _vars, _pars

    def _add_types(self, attr: var):
        if isinstance(attr.type, enum.EnumMeta):
            self._add_enum(attr.type)

    def _add_enum(self, e: enum.EnumMeta):
        self._enums.add(e)

    def _process_constraints(self, model):
        if not hasattr(model, "_constraints"):
            model._constraints = []
        for c in model._constraints:
            for p in c.params:
                pass
                if isinstance(p, enum.EnumMeta):
                    self._add_enum(p)
