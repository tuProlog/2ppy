from tuprolog.solve import ExecutionContext
from tuprolog.solve.exception import LogicError
from ._definitions import SystemError


def syntax_error(context: ExecutionContext, message: str, exception) -> SystemError:
    if isinstance(exception, LogicError):
        return SystemError.forUncaughtError(context, message, exception)
    return SystemError.forUncaughtException(context, message, exception)
