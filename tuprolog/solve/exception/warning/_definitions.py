import it.unibo.tuprolog.solve.exception.warning as _warnings  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["InitializationIssue", "MissingPredicate"]


InitializationIssue = _warnings.InitializationIssue


MissingPredicate = _warnings.MissingPredicate


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.warning.*")
