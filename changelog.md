## 0.5.0

#### Python interpreters support

- Add 3.13 CPython.

#### Added

- Introduce the ``strict`` argument to the ``disjunctive`` constraint.
- Add ``abs``, ``exp``, ``ln``, ``log``, ``log10``, ``log2``, and ``sqrt`` functions.
- Add ``product`` function to calculate product of all elements in the array.
- Add trigonometric functions: `acos`, `asin`, `atan`, `cos`, `sin`, `tan`.

#### Changed

- Array indexing must now specify all indices.

#### CI changes:

- Use minizinc 2.8.7 instead of 2.8.2

### 0.4.3

#### Added

- `disjunctive` constraint

#### Fixed

- array slices with upper slice as operations should compile correctly now

#### Documentation

- simplify and fix layout of ``count``, ``cumulative``
  ``table`` and ``max`` examples

### 0.4.2

#### CI changes

- use minizinc 2.7.6 as maximum version in CI (as in minizinc-python)
- use minizinc 2.6.0 as minimum version in CI (as in minizinc-python)

#### Python interpreters support

- add 3.12 CPython

### 0.4.1

#### Added

- ``table`` constraint
- ``contains`` method for arrays and sets, to check if elem presented
  in collection
- ``except_`` argument to ``all_different`` constraint

## 0.4.0

#### Added

- ``cumulative`` constraint
- ``forall`` constraint now supports enums which is not model's field

#### CI changes

- use minizinc 2.7.2 as maximum version in CI
- use minizinc 2.5.4 as minimum version in CI (as in minizinc-python)

### 0.3.1

#### Added

- var can be parametrized (you can assign values to them)

#### Fixed

- int fallback as a result of operation where both operands are float

#### CI changes

- use ruff for style checks

## 0.3

#### Syntax and compatibility

- some arguments are made positional only

#### Fixes

- fix enum doc example
- some minor fixes for internal code

#### Python interpreters support

- add 3.11 CPython
- drop 3.7 CPython
- drop pypy

### 0.2.4

#### Added

- available_solver_tags function to get available solvers
- optimization_level, n_processes, timeout and random_seed arg to solve

#### Fixed

- solve_maximize now correctly use solver arg

#### Changed

- add some type hints

### 0.2.3

#### Added

- validation for float ranges in some constraints, e.g. forall

#### Fixed

- ranges with float values correctly set bigger limit

#### Deleted

- check for minizinc executable is available,
as it seems, python-minizinc implement it by itself.

### 0.2.2

#### Added

- sets support enums

### 0.2.1

#### Added

- integer sets

#### Changed

- refactor some code

## 0.2

#### Changed

- zython doesn't redefine builtin range function,
  use ``zn.range`` for float, zython's var/par types.

#### Python interpreters support

- drop 3.6 CPython
- add 3.10 CPython

### 0.1.5

#### Added

- possibility to choose solver
- float fields support
- float ranges support

### 0.1.4

#### Changed

- an error about minizinc wasn't found in $PATH was changed to warning

### 0.1.3

#### Added

- check for minizinc in $PATH for startup
- documentation page about model parts

#### CI Changes

- Use minizinc 2.5.5 in CI.

### 0.1.2

#### Fixed

- some method of Operation and Constraint classes which were
  accessible by and visible for user are now hidden

#### Added

- ``increasing`` and ``decreasing`` constraints
  
### 0.1.1

#### Added

- ``allequal`` constraint
- ``ndistinct`` function
- ``except_0`` argument to ``alldifferent`` constraint

#### Changed

- project description in readme.md
- link to the html doc

## 0.1.0

- initial release
