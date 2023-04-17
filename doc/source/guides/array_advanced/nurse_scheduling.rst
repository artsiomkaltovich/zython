Nurse Scheduling Problem
========================

`Nurse Scheduling Problem <https://en.wikipedia.org/wiki/Nurse_scheduling_problem>`_ is a famous constraint programming
model. The solver should find the schedule which satisfied every constraint. In the following example we specify some
obvious constraint, like nurse shouldn't work 2 shifts in a row and so on, and try to minimize the differences between
number of shifts per week, so the work will be spread more or less evenly.

Python Model
------------

.. testcode::

    import zython as zn


    class NSPModel(zn.Model):
        def __init__(self, n_nurses):
            self.n_nurses = zn.par(n_nurses)
            self.shifts = zn.Array(zn.var(zn.range(self.n_nurses)), shape=(2, 7))
            self.constraints = [self.only_1_shift_in_day(), self.no_morning_shift_after_night(),
                                self.no_2_shifts_on_weekend()]

        def only_1_shift_in_day(self):
            return zn.forall(range(7), lambda i: zn.alldifferent(self.shifts[:, i]))

        def no_morning_shift_after_night(self):
            return zn.forall(range(6), lambda i: self.shifts[1, i] != self.shifts[0, i + 1])

        def no_2_shifts_on_weekend(self):
            return zn.alldifferent(self.shifts[:, 5:])

        def shifts_diff(self):
            return (zn.max(zn.range(self.n_nurses), lambda nurse: zn.count(self.shifts, nurse))
                    - zn.min(zn.range(self.n_nurses), lambda nurse: zn.count(self.shifts, nurse)))

    n_nurses = 4
    model = NSPModel(n_nurses)
    result = model.solve_minimize(model.shifts_diff())
    shifts = result["shifts"]
    for nurse in range(n_nurses):
        for day in range(7):
            assert sum(shifts[i][day] == nurse for i in range(2)) <= 1, "2 shifts per day"
    for day in range(6):
        assert shifts[1][day] != shifts[0][day + 1], "morning shift after night"
    assert len({shifts[i][j] for i in range(2) for j in range(5, 7)}) == 4, "2 or more shifts on the weekend"
    print("all checks pass")

.. testoutput::

    all checks pass

Solutions
---------

The actual solution can depend on solver version, this is what we got (blue - night shift, orange - morning shift):

.. image:: ../../_static/img/guides/array_advanced/nurses_scheduling/nurses_scheduling.png
  :width: 600
  :alt: Nurses schedule

