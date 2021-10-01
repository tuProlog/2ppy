from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.exception.warning as warnings
from tuprolog.core import Struct
from tuprolog.solve import ExecutionContext, ResolutionException, Signature

InitializationIssue = warnings.InitializationIssue

MissingPredicate = warnings.MissingPredicate


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
