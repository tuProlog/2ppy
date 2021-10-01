# noinspection PyUnresolvedReferences
import jpype.imports
from tuprolog import logger
from tuprolog.core import Term
from tuprolog.solve import ExecutionContext
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.exception.error as errors


MessageError = errors.MessageError


def message_error(content: Term, context: ExecutionContext, cause=None) -> MessageError:
    return MessageError.of(content, context, cause)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.MessageError.*")
