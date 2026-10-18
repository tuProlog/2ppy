from typing import Any

from tuprolog.core import Term
from tuprolog.solve import ExecutionContext

from ._definitions import MessageError

__all__ = ["message_error"]


def message_error(content: Term, context: ExecutionContext, cause: Any = None) -> MessageError:
    # MessageError.of is not @JvmStatic: MessageError.of would resolve to the static LogicError.of,
    # and JPype resolves MessageError.Companion to the companion class, not to its instance
    """Creates the error throwing an arbitrary term.

    Args:
        content: the term to throw; Prolog's `catch/3` unifies its catcher with it.
        context: the execution context in which the error occurs (e.g. a request's `context`).
        cause: the exception causing this one, if any.

    Returns:
        The error.

    Note:
        Calls 2P-Kt's `MessageError.Companion.of`, which (not being static on the JVM) is not
        reachable as `MessageError.of`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> from tuprolog.core import atom
        >>> message_error(atom("hello"), context).content
        hello
    """
    companion = MessageError.class_.getField("Companion").get(None)
    return companion.of(content, context, cause)
