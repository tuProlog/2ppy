from tuprolog.core import Term
from tuprolog.solve import ExecutionContext

from ._definitions import MessageError


def message_error(content: Term, context: ExecutionContext, cause=None) -> MessageError:
    # MessageError.of is not @JvmStatic: MessageError.of would resolve to the static LogicError.of,
    # and JPype resolves MessageError.Companion to the companion class, not to its instance
    companion = MessageError.class_.getField("Companion").get(None)
    return companion.of(content, context, cause)
