import it.unibo.tuprolog.solve as _solve  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["ProbExtensions"]


ProbExtensions = _solve.ProbExtensions


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.plp.*")
