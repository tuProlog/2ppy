import it.unibo.tuprolog.utils as _utils  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

Castable = _utils.Castable

Taggable = _utils.Taggable

logger.debug("Loaded JVM classes from it.unibo.tuprolog.utils.*")
