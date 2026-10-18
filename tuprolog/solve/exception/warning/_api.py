from tuprolog.core import Struct
from tuprolog.solve import ExecutionContext, Signature
from tuprolog.solve.exception import ResolutionException

from ._definitions import InitializationIssue, MissingPredicate

__all__ = ["initialization_issue", "missing_predicate"]


def initialization_issue(
    goal: Struct, context: ExecutionContext, cause: ResolutionException = None
) -> InitializationIssue:
    return InitializationIssue(goal, cause, context)


def missing_predicate(
    signature: Signature, context: ExecutionContext, cause=None
) -> MissingPredicate:
    return MissingPredicate(cause, context, signature)
