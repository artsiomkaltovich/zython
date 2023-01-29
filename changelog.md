### 0.3.1

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
#### changed
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
- Sets support enums

### 0.2.1
#### Added
- Integer sets
#### Changed
- Refactor some code

## 0.2
#### Changed
- zython doesn't redefine builtin range function, 
  use ``zn.range`` for float, zython's var/par types.
#### Python interpreters support
- drop 3.6 CPython
- add 3.10 CPython

### 0.1.5
#### Added
- Possibility to choose solver
- Float fields support
- Float ranges support

### 0.1.4
#### Changed
- An error about minizinc wasn't found in $PATH was changed to warning


### 0.1.3
#### Added
- check for minizinc in $PATH for startup
- documentation page about model parts
#### Changed
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

#### Changed:
- project description in readme.md
- link to the html doc

## 0.1.0

- initial release
