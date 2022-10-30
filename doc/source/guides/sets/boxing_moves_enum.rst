Boxing Moves (Enum)
===================

In :ref:`the previous file <boxing-moves-int>` we've seen how to use set of integers,
but it is not the most readable and useful way to represent available decisions.

Zython also support python's enums, lets rewrite the model.

.. note::

    In Minizinc 2.6.x there were changes with enums
    so it recommended to use 2.5.x version

Python Model
------------

.. testcode::

    import enum
    import zython as zn


    class Moves(enum.Enum):
        jab = enum.auto()
        cross = enum.auto()
        hook = enum.auto()
        uppercut = enum.auto()
        slip = enum.auto()


    class Model(zn.Model):
        def __init__(self, moves, time_available, money_available, power, time, money):
            self.time_available = time_available
            self.money_available = money_available
            self.power = zn.Array(power)
            self.time = zn.Array(time)
            self.money = zn.Array(money)
            self.to_learn = zn.Set(zn.var(moves))
            self.constraints = [
                zn.sum(self.to_learn, lambda move: self.time[move]) < self.time_available,
                zn.sum(self.to_learn, lambda move: self.money[move]) < self.money_available,
            ]


    model = Model(Moves, 5, 10, [1, 2, 1, 2, 3], [1, 2, 1, 3, 1], [3, 4, 3, 2, 1])
    result = model.solve_maximize(zn.sum(model.to_learn, lambda move: model.power[move]))
    moves = sorted(result['to_learn'], key=lambda x: x.value)
    print(f"Moves to learn: {moves}, power: {result['objective']}")

.. testoutput::

    Moves to learn: [<Moves.jab: 1>, <Moves.cross: 2>, <Moves.uppercut: 4>], power: 6
