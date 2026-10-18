# Handle errors

Logic programs fail in two ways: a goal may simply have no solutions (a *no*), or an *error* may
stop the resolution, e.g. `X is foo + 1` raises a `type_error`, because `foo` is not a number. This
guide shows how to handle errors in Prolog code and in Python code.

## How errors look

ISO Prolog errors are terms `error(Type, Extra)`: `Type` says what went wrong (e.g.
`type_error(evaluable, foo/0)`, `instantiation_error`, `existence_error(procedure, p/0)`) and
`Extra` adds details, such as a message. The [exceptions reference](../reference/exceptions.md)
lists the error types.

In Python, each error is an exception, classified by the classes in `tuprolog.errors` and by
Python's built-in exceptions: e.g. a `type_error` is a `PrologTypeError` and a `TypeError`, and
every error raised by 2P-Kt is a `TuPrologError`.

## Catch errors in Python

`solver.query` raises errors as exceptions:

```pycon
>>> from tuprolog.errors import PrologError, PrologTypeError
>>> from tuprolog.solve.prolog import prolog_solver
>>> solver = prolog_solver()
>>> try:
...     list(solver.query("X is foo + 1"))
... except PrologTypeError as error:
...     print(error.type)
type_error(evaluable, foo/0)
>>> try:
...     list(solver.query("atom_length(1, N)"))
... except TypeError as error:  # Python's built-in classification works too
...     print(error.type)
type_error(atom, 1)

```

Errors carry the error `type`, the `extra_data`, a human-readable `message`, and the
`logic_stack_trace`, i.e. the goals being solved when the error occurred:

```pycon
>>> try:
...     list(solver.query("atom_length(X, N)"))
... except PrologError as error:
...     print(error.type)
...     print(error.message)
...     print(error.logic_stack_trace[0])
instantiation_error
The 0-th argument `X` of atom_length/2 is unexpectedly not instantiated
atom_length(X_..., N_...)

```

Other exceptions: a query running past its timeout raises a `TimeOutError`, `halt/0,1` raises a
`HaltError` (with its `exit_status`), and invalid Prolog text raises a `ParsingError` (a
`ValueError`).

## Inspect halted solutions

`solve` and `solve_once` do not raise: an error ends the resolution with a *halt* solution,
carrying the exception. Call `raise_error()` to raise it:

```pycon
>>> solution = solver.solve_once("X is 1 / 0")
>>> solution.is_halt, solution.exception.type
(True, evaluation_error(zero_divisor))
>>> try:
...     solution.raise_error()
... except ArithmeticError:
...     print("division by zero")
division by zero

```

## Catch errors in Prolog

`catch(Goal, Catcher, Recovery)` runs `Goal`; if it raises an error unifying with `Catcher`,
`Recovery` runs instead. `throw/1` raises any term:

```pycon
>>> solver.solve_once("catch(X is 1 / 0, error(E, _), true)")["E"]
evaluation_error(zero_divisor)
>>> solver.solve_once("catch(throw(out_of_stock(apples)), out_of_stock(Item), true)")["Item"]
apples

```

An uncaught `throw/1` of a non-error term halts the resolution with a `system_error`:

```pycon
>>> solver.solve_once("throw(oops)").exception.type
system_error

```

## Make undefined predicates fail, or raise errors

By default, calling an undefined predicate prints a warning and fails. Set the `unknown` flag to
`error` to raise an `existence_error` instead (see [Query solvers](query-solvers.md#set-flags)):

```pycon
>>> from tuprolog.solve.flags import DEFAULT_FLAG_STORE, flag_store
>>> strict = prolog_solver(flags=flag_store(DEFAULT_FLAG_STORE, unknown="error"))
>>> strict.solve_once("catch(no_such_predicate, error(E, _), true)")["E"]
existence_error(procedure, no_such_predicate/0)

```

## Errors from Python code

Exceptions raised by predicates and functions written in Python become `system_error`s; primitives
can raise the standard ISO errors instead. See
[Define predicates in Python](define-predicates-in-python.md#report-errors).

## See also

- [Exceptions reference](../reference/exceptions.md).
- API: `tuprolog.errors` ([reference](../api/tuprolog/errors.md)),
  `tuprolog.solve.exception` ([reference](../api/tuprolog/solve/exception.md)).
- 2P-Kt's [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
