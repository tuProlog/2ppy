# noinspection PyUnresolvedReferences
import jpype.imports
from tuprolog import logger
from tuprolog.solve import ExecutionContext
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.exception.error as errors
from tuprolog.solve.exception import LogicError


SystemError = errors.SyntaxError


def syntax_error(context: ExecutionContext, message: str, exception) -> SystemError:
    if isinstance(exception, LogicError):
        return SystemError.forUncaughtError(context, message, exception)
    return SystemError.forUncaughtException(context, message, exception)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.SystemError.*")
