import it.unibo.tuprolog.collections as _collections  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "ClauseCollection",
    "ClauseMultiSet",
    "ClauseQueue",
    "MutableClauseCollection",
    "MutableClauseMultiSet",
    "MutableClauseQueue",
    "RetrieveResult",
]


ClauseCollection = _collections.ClauseCollection

MutableClauseCollection = _collections.MutableClauseCollection

ClauseMultiSet = _collections.ClauseMultiSet

MutableClauseMultiSet = _collections.MutableClauseMultiSet

ClauseQueue = _collections.ClauseQueue

MutableClauseQueue = _collections.MutableClauseQueue

RetrieveResult = _collections.RetrieveResult

logger.debug("Loaded JVM classes from it.unibo.tuprolog.collections.*")
