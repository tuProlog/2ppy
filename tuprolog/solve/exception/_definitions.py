import it.unibo.tuprolog.solve.exception as _exceptions  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["HaltException", "LogicError", "ResolutionException", "TimeOutException"]


HaltException = _exceptions.HaltException
"""The exception stopping a solver, e.g. raised by `halt/0` and `halt/1`.

Members (snake_case aliases as well): `exit_status`, the integer status (`halt/1`'s argument,
0 by default), besides those of `ResolutionException`.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> error = prolog_solver().solve_once("halt(3)").get_exception()
    >>> isinstance(error, HaltException), error.exit_status
    (True, 3)
"""


LogicError = _exceptions.LogicError
"""An ISO Prolog error: the exception a predicate throws as the term `error(Type, Extra)`.

Subclasses (in `tuprolog.solve.exception.error`) model each family of ISO errors, telling them by
`Type`'s functor (e.g. `type_error/2` is a `TypeError`). Prolog code catches them with
`catch(Goal, error(Type, _), Recovery)`.

Members (snake_case aliases as well), besides those of `ResolutionException`:

- `type`: the error type, a `tuprolog.core.Struct` such as `type_error(integer, a)` or
  `instantiation_error`;
- `extra_data`: the extra data (a `tuprolog.core.Term`, usually the message as an atom), or
  `None`;
- `error_struct`: the thrown term, `error(Type, Extra)`.

`LogicError.of(...)` is 2P-Kt's factory building the subclass matching an error type; the
factories in `tuprolog.solve.exception.error` are the handier way to build errors.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> error = prolog_solver().solve_once("atom_length(f, a)").get_exception()
    >>> isinstance(error, LogicError)
    True
    >>> error.type
    type_error(integer, a)
    >>> error.error_struct.functor
    'error'
"""


ResolutionException = _exceptions.ResolutionException
"""The base of the exceptions that may occur while solving a query.

Members (snake_case aliases as well):

- `message`, `cause`: the description, and the exception causing this one (if any);
- `context`: the `tuprolog.solve.ExecutionContext` in which the exception occurred, and
  `contexts`, the stack of contexts, innermost first (one per nested resolution);
- `logic_stack_trace`: the goals being solved when the exception occurred, innermost first, as
  `tuprolog.core.Struct`s;
- `update_context(context, index)`, `update_last_context(context)`, `push_context(context)`:
  copies of the exception with a changed or extended stack of contexts (exceptions are
  immutable).

Subclasses: `LogicError`, `HaltException`, `TimeOutException`, and `Warning`.
"""


TimeOutException = _exceptions.TimeOutException
"""The exception ending a query that exceeded its time limit.

Members (snake_case aliases as well): `exceeded_duration`, the time limit exceeded (in
milliseconds), besides those of `ResolutionException`.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> error = prolog_solver().solve_once("repeat, fail", 50).get_exception()
    >>> isinstance(error, TimeOutException), error.exceeded_duration
    (True, 50)
"""


Warning = _exceptions.Warning
"""The base of non-fatal problems, reported rather than stopping resolution.

Solvers notify warnings on their warnings channel (see `tuprolog.solve.channel`), printing them
by default. Subclasses are in `tuprolog.solve.exception.warning`. This name shadows Python's
built-in `Warning`, so it is not star-exported: import it explicitly.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.*")
