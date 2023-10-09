from tuprolog import logger
import jpype.imports
import it.unibo.tuprolog.unify as _unify # type: ignore


Unificator = _unify.Unificator


DEFAULT_UNIFICATOR = Unificator.getDefault()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.unify.*")
