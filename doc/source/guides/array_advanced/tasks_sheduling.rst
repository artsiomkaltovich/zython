Tasks Scheduling
================

The disjunctive constraint takes an array of start times for each task and
an array of their durations, ensuring that only one task is active at
any given time.

.. note::

    It is recommended to use ranges and sequences of ranges instead of integers,
    because MiniZinc can return unexpected results when any argument is an integer.

Model
-----

We will recreate the example of the task scheduling problem from the
`MiniZinc <https://www.minizinc.org/doc-2.7.6/en/predicates.html#ex-jobshop3>`_
documentation.

The model consists of several jobs, which can be divided into several
steps. The following restrictions apply:

- To complete a job, all steps must be executed.
- Different steps are independent:
    If there is a job on the first step, another job can be processed on the second step
    without waiting.
- If there is an active task on any step, no other job can be executed
    on that step and must wait.

You can think of this as a conveyor with `n_jobs` lines,
one part on every line, and
`n_steps` independent machines that are shared between lines.
Each machine can complete only one operation with any part
and must work with a part processed by the previous machine.
We are searching for the fastest way to process all the parts.

Python Model
------------

.. testcode::

    import zython as zn


    durations = [
        [1, 4, 5, 3, 6],
        [3, 2, 7, 1, 2],
        [4, 4, 4, 4, 4],
        [1, 1, 1, 6, 8],
        [7, 3, 2, 2, 1],
    ]


    class MyModel(zn.Model):
        def __init__(self, durations):
            self.durations = zn.Array(durations)
            self.n_jobs = len(durations)
            self.n_tasks = len(durations[0])
            self.total = zn.sum(self.durations)
            self.end = zn.var(zn.range(self.total + 1))
            self.start = zn.Array(
                zn.var(zn.range(self.total + 1)), shape=(self.n_jobs, self.n_tasks)
            )
            self.constraints = [self.in_sequence(), self.no_overlap()]

        def no_overlap(self):
            return zn.forall(
                zn.range(self.n_tasks),
                lambda j: zn.disjunctive(
                    [self.start[i, j] for i in range(self.n_jobs)],
                    [self.durations[i, j] for i in range(self.n_jobs)],
                )
            )

        def in_sequence(self):
            return zn.forall(
                range(self.n_jobs),
                lambda i: zn.forall(
                        zn.range(self.n_tasks - 1),
                        lambda j: self.start[i, j] + self.durations[i, j] <= self.start[i, j + 1],
                    ) & (
                        self.start[i, self.n_tasks - 1] + self.durations[i, self.n_tasks - 1] <= self.end
                    )
            )


    model = MyModel(durations)
    result = model.solve_minimize(model.end)
    print(result)


.. testoutput::

    Solution(objective=30, total=86, end=30, start=[[8, 9, 13, 18, 21], [5, 13, 18, 25, 27], [1, 5, 9, 13, 17], [0, 1, 2, 3, 9], [9, 16, 25, 27, 29]])


Strict Mode
-----------

The strict mode is specified by setting the `strict` argument to True. In this mode, there is a significant difference:

- Tasks with a duration of 0 CANNOT be scheduled at any time but only when no other task is running.
