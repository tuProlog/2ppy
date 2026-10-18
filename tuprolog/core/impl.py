import it.unibo.tuprolog.core.impl as _impl  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger
from tuprolog.core import TermFormatter

__all__ = ["DefaultTermFormatter"]


DefaultTermFormatter = _impl.SimpleTermFormatter

logger.debug(
    "Loaded compatibility layer for JVM subtypes of " + str(TermFormatter.class_.getName())
)
