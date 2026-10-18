"""Exceptions raised while solving queries: ISO Prolog errors, halts, timeouts, and warnings.

Prolog programs signal problems by **throwing** terms (`throw/1`), which callers may **catch**
(`catch(Goal, Catcher, Recovery)` runs `Recovery` if `Goal` throws a term unifying with
`Catcher`). The ISO standard fixes the shape of the terms built-in predicates throw:
`error(Type, Extra)`, where `Type` says what went wrong (e.g. `type_error(integer, a)`: an integer
was expected, `a` was found) and `Extra` carries implementation-defined details (2P-Kt puts a
human-readable message there). See `tuprolog.solve.exception.error` for each kind of error.

In this library each such problem is a JVM exception (raised and caught as a Python exception)
descending from `ResolutionException`:

- `LogicError`: an ISO error, i.e. a thrown `error(Type, Extra)` term (subclasses in
  `tuprolog.solve.exception.error`);
- `HaltException`: the solver was stopped, e.g. by `halt/0,1`;
- `TimeOutException`: a query exceeded its time limit;
- `Warning` (import it explicitly, as it shadows Python's built-in name): a non-fatal problem,
  reported on the solver's warnings channel rather than stopping resolution (subclasses in
  `tuprolog.solve.exception.warning`).

Solvers do not raise these exceptions when solving: an error ends the solutions with a *halt*
solution carrying the exception (see `tuprolog.solve.Solution`), while `Solver.query` raises it.
Primitives written in Python raise them (or reply with them, see `tuprolog.solve.primitive`) to
signal errors. `tuprolog.errors` makes them also instances of Python classes (e.g. a logic
`type_error` is a `tuprolog.errors.PrologTypeError` and a built-in `TypeError`), for `except`.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> solver = prolog_solver()
    >>> solution = solver.solve_once("X is 1 / 0")
    >>> solution.is_halt
    True
    >>> error = solution.get_exception()
    >>> isinstance(error, LogicError), error.type
    (True, evaluation_error(zero_divisor))
    >>> solver.solve_once("catch(X is 1 / 0, error(E, _), true)")["E"]
    evaluation_error(zero_divisor)
    >>> try:
    ...     list(solver.query("atom_length(X, L)"))
    ... except ResolutionException as e:
    ...     print(e.error_struct.args[0])
    instantiation_error

See Also:
    `tuprolog.solve.exception.error` and `tuprolog.solve.exception.warning`, for the subclasses;
    `tuprolog.errors`, for the Python exception classes;
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._definitions import *
from ._definitions import Warning  # not in __all__, as star-imports would shadow the builtin

__all__ = ["HaltException", "LogicError", "ResolutionException", "TimeOutException"]
