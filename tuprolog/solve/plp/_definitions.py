from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve as _solve  # type: ignore


ProbExtensions = _solve.ProbExtensions


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.plp.*")
