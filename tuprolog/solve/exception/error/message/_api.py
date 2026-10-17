from tuprolog.core import Term
from tuprolog.solve import ExecutionContext
from ._definitions import MessageError


def message_error(content: Term, context: ExecutionContext, cause=None) -> MessageError:
    return MessageError.of(content, context, cause)
