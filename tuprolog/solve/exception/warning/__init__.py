from tuprolog import logger
from tuprolog.core import Struct
from tuprolog.solve import ExecutionContext, ResolutionException, Signature
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.exception.warning as _warnings  # type: ignore

InitializationIssue = _warnings.InitializationIssue

MissingPredicate = _warnings.MissingPredicate


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


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.warning.*")
