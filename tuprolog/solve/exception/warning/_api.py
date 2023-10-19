from tuprolog.core import Struct
from tuprolog.solve import ExecutionContext, ResolutionException, Signature
from ._definitions import InitializationIssue, MissingPredicate


def initialization_issue(
        goal: Struct,
        context: ExecutionContext,
        cause: ResolutionException = None
) -> InitializationIssue:
    return InitializationIssue(goal, cause, context)


def missing_predicate(
        signature: Signature,
        context: ExecutionContext,
        cause=None
) -> MissingPredicate:
    return MissingPredicate(cause, context, signature)
