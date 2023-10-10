from tuprolog import logger
from tuprolog.solve import ExecutionContext
from tuprolog.solve.exception import LogicError
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.exception.error as _errors  # type: ignore


SystemError = _errors.SyntaxError


def syntax_error(context: ExecutionContext, message: str, exception) -> SystemError:
    if isinstance(exception, LogicError):
        return SystemError.forUncaughtError(context, message, exception)
    return SystemError.forUncaughtException(context, message, exception)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.SystemError.*")
