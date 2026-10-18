import it.unibo.tuprolog.unify as _unify  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["DEFAULT_UNIFICATOR", "Unificator"]


Unificator = _unify.Unificator


DEFAULT_UNIFICATOR = Unificator.getDefault()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.unify.*")
