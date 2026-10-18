from typing import Any

from tuprolog.solve import ExecutionContext
from tuprolog.solve.exception import LogicError

from ._definitions import SystemError

__all__ = ["system_error"]


def system_error(context: ExecutionContext, exception: Any) -> SystemError:
    """Creates the system error wrapping an uncaught error, exception, or thrown term.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        exception: a `tuprolog.solve.exception.LogicError` left uncaught (its contexts are kept),
            a JVM exception (becoming the `cause`), or a thrown `tuprolog.core.Term`.

    Returns:
        The error, thrown as `error(system_error, Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> from tuprolog.core import atom
        >>> system_error(context, atom("oops")).message
        'Uncaught exception `oops`'
    """
    if isinstance(exception, LogicError):
        return SystemError.forUncaughtError(exception)
    return SystemError.forUncaughtException(context, exception)
