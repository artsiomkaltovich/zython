Solvers
=======

.. _solvers:

Solvers are programs which are find actual solutions for your
models. Solvers differs by supported types, features and performance.
You can find more info in
`minizinc cmd options doc <https://www.minizinc.org/doc-2.5.0/en/command_line.html?#cmdoption-solver>`_

Solvers can be specified in solve methods. Default solver of
minizinc is `gecode <https://www.gecode.org/>`_ it is fast and
general purpose, but it is not fully support of float types.
For float number models solving you can use
`cbc <https://github.com/coin-or/Cbc>`_.

::

    m = Model(...)
    m.solve_satisfy(solver="cbc")
