Boxing Moves (Integer)
======================

.. _boxing-moves-int:

Let's imagine you've should to fight against Mike Tyson (don't worry, you have a week to prepare). You should learn
several boxing moves, each of them has strength, but you should invest some time to learn it and some money to hire
a coach.

.. list-table:: Boxing Moves
   :header-rows: 1

   * - Move
     - power
     - Time to learn
     - Money to learn
   * - jab
     - 1
     - 1
     - 3
   * - cross
     - 2
     - 2
     - 3
   * - uppercut
     - 1
     - 1
     - 3
   * - overhand
     - 2
     - 2
     - 2
   * - hook
     - 3
     - 1
     - 1

.. note::

    This is not a boxing (or any other sport/fighting) advice. The example is used to represent zython's syntax.
    All number are fictional, do not use them in a real world. Please consult with your coach if you really should
    fight to Mike Tyson.

Python Model
------------

.. testcode::

    import zython as zn


    class Model(zn.Model):
        def __init__(self, time_available, money_available, power, time, money):
            self.time_available = time_available
            self.money_available = money_available
            self.power = zn.Array(power)
            self.time = zn.Array(time)
            self.money = zn.Array(money)
            self.to_learn = zn.Set(zn.var(zn.range(5)))
            self.constraints = [
                zn.sum(self.to_learn, lambda move: self.time[move]) < self.time_available,
                zn.sum(self.to_learn, lambda move: self.money[move]) < self.money_available,
            ]


    model = Model(5, 10, [1, 2, 1, 2, 3], [1, 2, 1, 3, 1], [3, 4, 3, 2, 1])
    result = model.solve_maximize(zn.sum(model.to_learn, lambda move: model.power[move]))
    print(f"Moves to learn: {result['to_learn']}, power: {result['objective']}")

.. testoutput::

    Moves to learn: {0, 1, 4}, power: 6
