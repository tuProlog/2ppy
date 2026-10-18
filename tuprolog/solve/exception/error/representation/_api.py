from typing import Any

from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature

from ._definitions import Limit, RepresentationError

__all__ = ["limit", "representation_error"]


def representation_error(
    context: ExecutionContext, procedure: Signature, limit: Limit, cause: Any = None
) -> RepresentationError:
    """Creates a representation error.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        procedure: the signature of the predicate raising the error (e.g. a request's `signature`).
        limit: the exceeded limit (e.g. `LIMIT_MAX_ARITY`).
        cause: the exception causing this one, if any.

    Returns:
        The error, thrown as `error(representation_error(Limit), Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> representation_error(context, signature("functor", 3), LIMIT_MAX_ARITY).type
        representation_error(max_arity)
    """
    return RepresentationError.of(context, procedure, limit, cause)


def limit(name: str | Term) -> Limit:
    """The `Limit` named by a string or an atom.

    Args:
        name: the name, as a string (case-insensitive) or a `tuprolog.core.Term` (as in the error
            terms, e.g. `atom("max_arity")`).

    Returns:
        The matching `Limit`; `None` for terms other than atoms.

    Raises:
        java.lang.IllegalArgumentException: if no `Limit` has that name.

    Examples:
        >>> from tuprolog.solve.exception.error.representation import *
        >>> limit("max_arity") == LIMIT_MAX_ARITY
        True
    """
    if isinstance(name, str):
        return Limit.of(name)
    else:
        return Limit.fromTerm(name)
