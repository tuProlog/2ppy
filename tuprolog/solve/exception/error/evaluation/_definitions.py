import it.unibo.tuprolog.solve.exception.error as errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "ERROR_FLOAT_OVERFLOW",
    "ERROR_INT_OVERFLOW",
    "ERROR_UNDEFINED",
    "ERROR_UNDERFLOW",
    "ERROR_ZERO_DIVISOR",
    "ErrorType",
    "EvaluationError",
]


EvaluationError = errors.EvaluationError
"""The evaluation error, thrown as `error(evaluation_error(Error), _)`: an expression failed.

The JVM class (also a Python `ArithmeticError` and a `tuprolog.errors.PrologEvaluationError`).
Members (snake_case aliases as well): `error_type`, the `ErrorType`; besides those of
`tuprolog.solve.exception.LogicError` (e.g. `type`, `error_struct`, `message`).
"""


ErrorType = EvaluationError.Type
"""The enumeration of the kinds of evaluation errors (2P-Kt's `EvaluationError.Type`).

Each value (also available as an `ERROR_*` constant) is the `Error` of an
`evaluation_error(Error)` term: `to_term()` gives it as an atom (e.g. `zero_divisor`).
`ErrorType.valueOf(NAME)` and `ErrorType.fromTerm(term)` look a value up (see `error_type`).
"""


ERROR_INT_OVERFLOW = ErrorType.INT_OVERFLOW
"""`int_overflow`: an integer result is too large to be represented."""


ERROR_FLOAT_OVERFLOW = ErrorType.FLOAT_OVERFLOW
"""`float_overflow`: a floating-point result is too large to be represented."""


ERROR_UNDERFLOW = ErrorType.UNDERFLOW
"""`underflow`: a floating-point result is too small to be represented."""


ERROR_ZERO_DIVISOR = ErrorType.ZERO_DIVISOR
"""`zero_divisor`: a number is divided by zero."""


ERROR_UNDEFINED = ErrorType.UNDEFINED
"""`undefined`: the result is mathematically undefined (e.g. `0 / 0`, `log(0)`)."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.EvaluationError.*")
