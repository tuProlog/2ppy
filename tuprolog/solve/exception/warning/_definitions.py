from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.exception.warning as _warnings  # type: ignore


InitializationIssue = _warnings.InitializationIssue


MissingPredicate = _warnings.MissingPredicate


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.warning.*")
