from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.utils as _utils  # type: ignore

Castable = _utils.Castable

Taggable = _utils.Taggable

logger.debug("Loaded JVM classes from it.unibo.tuprolog.utils.*")
