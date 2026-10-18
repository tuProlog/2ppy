"""Evaluation errors: an arithmetic expression cannot be evaluated, e.g. a division by zero.

ISO Prolog's `evaluation_error(Error)` error, thrown as `error(evaluation_error(Error), Extra)`,
means that evaluating an arithmetic expression (e.g. by `is/2` or `</2`) failed because of
`Error`: `zero_divisor`, `undefined` (e.g. `0 / 0`), `int_overflow`, `float_overflow`, or
`underflow`. Expressions containing non-evaluable terms raise type errors instead (e.g.
`type_error(evaluable, foo/0)`).

The error is an `EvaluationError`, and the kinds of errors are the values of the `ErrorType`
enumeration (also available as the `ERROR_*` constants). Build errors with `evaluation_error`.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> prolog_solver().solve_once("catch(X is 1 / 0, error(E, _), true)")["E"]
    evaluation_error(zero_divisor)

See Also:
    `tuprolog.solve.function`, for arithmetic functions defined in Python;
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._api import *
from ._definitions import *

__all__ = [
    "ERROR_FLOAT_OVERFLOW",
    "ERROR_INT_OVERFLOW",
    "ERROR_UNDEFINED",
    "ERROR_UNDERFLOW",
    "ERROR_ZERO_DIVISOR",
    "ErrorType",
    "EvaluationError",
    "error_type",
    "evaluation_error",
]
