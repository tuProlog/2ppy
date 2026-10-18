import it.unibo.tuprolog.solve.exception.error as _errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["InstantiationError"]


InstantiationError = _errors.InstantiationError


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.InstantiationError.*")
