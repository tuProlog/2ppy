from typing import Any

from tuprolog.core import Struct
from tuprolog.solve import ExecutionContext, Signature
from tuprolog.solve.exception import ResolutionException

from ._definitions import InitializationIssue, MissingPredicate

__all__ = ["initialization_issue", "missing_predicate"]


def initialization_issue(
    goal: Struct, context: ExecutionContext, cause: ResolutionException = None
) -> InitializationIssue:
    """Creates the warning that an initialization goal did not succeed.

    Args:
        goal: the initialization goal (e.g. a directive's).
        context: the execution context in which the goal was solved.
        cause: the error the goal raised, or `None` if it failed.

    Returns:
        The warning.
    """
    return InitializationIssue(goal, cause, context)


def missing_predicate(
    signature: Signature, context: ExecutionContext, cause: Any = None
) -> MissingPredicate:
    """Creates the warning that a goal called an undefined predicate.

    Args:
        signature: the signature of the missing predicate.
        context: the execution context of the call.
        cause: the exception causing this warning, if any.

    Returns:
        The warning, whose message names the missing predicate.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> from tuprolog.solve.exception.warning import missing_predicate
        >>> context = prolog_solver().current_context
        >>> missing_predicate(signature("foo", 1), context).message
        'No such a predicate: foo/1'
    """
    return MissingPredicate(cause, context, signature)
