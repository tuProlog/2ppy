from tuprolog.core import Term, atom
from tuprolog.solve import ExecutionContext

from ._definitions import ErrorType, EvaluationError

__all__ = ["error_type", "evaluation_error"]


def evaluation_error(context: ExecutionContext, type: ErrorType, message: str) -> EvaluationError:
    """Creates an evaluation error.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        type: the kind of error (e.g. `ERROR_ZERO_DIVISOR`).
        message: the error message, also the error term's extra data.

    Returns:
        The error, thrown as `error(evaluation_error(Type), Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> evaluation_error(context, ERROR_ZERO_DIVISOR, "division by zero").error_struct
        error(evaluation_error(zero_divisor), 'division by zero')
    """
    return EvaluationError(message, None, context, type, atom(message))


def error_type(name: str | Term) -> ErrorType:
    """The `ErrorType` named by a string or an atom.

    Args:
        name: the name, as a string (case-insensitive) or a `tuprolog.core.Term` (as in the error
            terms, e.g. `atom("zero_divisor")`).

    Returns:
        The matching `ErrorType`; `None` for terms other than atoms.

    Raises:
        java.lang.IllegalArgumentException: if no `ErrorType` has that name.

    Examples:
        >>> from tuprolog.core import atom
        >>> from tuprolog.solve.exception.error.evaluation import *
        >>> error_type("zero_divisor") == error_type(atom("zero_divisor")) == ERROR_ZERO_DIVISOR
        True
    """
    if isinstance(name, str):
        return ErrorType.valueOf(name.upper())
    else:
        return ErrorType.fromTerm(name)
