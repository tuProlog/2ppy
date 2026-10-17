from typing import Any

from tuprolog.solve import ExecutionContext
from tuprolog.solve.exception import LogicError

from ._definitions import SystemError


def system_error(context: ExecutionContext, exception: Any) -> SystemError:
    """Wraps an uncaught LogicError, JVM Throwable, or error Term into a SystemError."""
    if isinstance(exception, LogicError):
        return SystemError.forUncaughtError(exception)
    return SystemError.forUncaughtException(context, exception)
