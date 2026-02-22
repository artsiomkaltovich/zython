Dynamically Generated Grid Coloring
===================================

Let's solve the following problem:

* there is a 2d grid (NxM)
* is there a way to paint every vertex in the grid with such a manner that for every possible rectangle 4 corners won't be the same color.

.. image:: ../../_static/img/guides/coloring/dynamic_grid_coloring/grid_small_uncolored.png
  :width: 300
  :alt: Grid

The solution of such task can be rather tricky, but zython helps to express it in small script. We will separate this
task on two small subtask: generate coordinates of every rectangle, find actual solution with constraint for every
rectangle. The first subtask will be solved in python, it will generate every possible rectangle and pass it in
``allequal`` constraint, and then use boolean inversion to specify that at least one corner should be different.
While solver will solve the second subtask and find actual solution.

The goal of such example is to show that zython can be used for dynamic minizinc source code generation, such
collaboration helps to solve tricky problems with small and simple scripts.

Python Model
------------

.. testcode::

    import zython as zn
    import itertools


    class Rectangles(zn.Model):
        def __init__(self, shape):
            self.field = zn.Array(zn.var(range(5)), shape=shape)
            self.constraints = []
            self.init_constraints(shape)

        def init_constraints(self, shape):
            for rect in get_rect(shape):
                self.constraints.append(~zn.allequal(self.field[p] for p in rect))


    def get_rect(shape):
        for i in range(1, shape[0]):
            for j in range(1, shape[1]):
                width = shape[0] - i
                height = shape[1] - j
                for left, top in itertools.product(range(i), range(j)):
                    rigth = left + width
                    bottom = top + height
                    yield (left, top), (rigth, top), (rigth, bottom), (left, bottom)


    model = Rectangles((3, 4))
    result = model.solve_satisfy(verbose=True)

.. testoutput::

    include "all_equal.mzn";
    array[0..2, 0..3] of var 0..4: field;
    constraint (not all_equal([field[0, 0], field[2, 0], field[2, 3], field[0, 3]]));
    constraint (not all_equal([field[0, 0], field[2, 0], field[2, 2], field[0, 2]]));
    constraint (not all_equal([field[0, 1], field[2, 1], field[2, 3], field[0, 3]]));
    constraint (not all_equal([field[0, 0], field[2, 0], field[2, 1], field[0, 1]]));
    constraint (not all_equal([field[0, 1], field[2, 1], field[2, 2], field[0, 2]]));
    constraint (not all_equal([field[0, 2], field[2, 2], field[2, 3], field[0, 3]]));
    constraint (not all_equal([field[0, 0], field[1, 0], field[1, 3], field[0, 3]]));
    constraint (not all_equal([field[1, 0], field[2, 0], field[2, 3], field[1, 3]]));
    constraint (not all_equal([field[0, 0], field[1, 0], field[1, 2], field[0, 2]]));
    constraint (not all_equal([field[0, 1], field[1, 1], field[1, 3], field[0, 3]]));
    constraint (not all_equal([field[1, 0], field[2, 0], field[2, 2], field[1, 2]]));
    constraint (not all_equal([field[1, 1], field[2, 1], field[2, 3], field[1, 3]]));
    constraint (not all_equal([field[0, 0], field[1, 0], field[1, 1], field[0, 1]]));
    constraint (not all_equal([field[0, 1], field[1, 1], field[1, 2], field[0, 2]]));
    constraint (not all_equal([field[0, 2], field[1, 2], field[1, 3], field[0, 3]]));
    constraint (not all_equal([field[1, 0], field[2, 0], field[2, 1], field[1, 1]]));
    constraint (not all_equal([field[1, 1], field[2, 1], field[2, 2], field[1, 2]]));
    constraint (not all_equal([field[1, 2], field[2, 2], field[2, 3], field[1, 3]]));
    solve satisfy;

Solution
--------

The solution can differ from version to version, we've got the following:

.. image:: ../../_static/img/guides/coloring/dynamic_grid_coloring/grid_colored.png
  :width: 400
  :alt: Grid Coloring Solution
