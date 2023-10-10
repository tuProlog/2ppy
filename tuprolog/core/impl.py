from tuprolog import logger
from tuprolog.core import TermFormatter
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.core.impl as _impl  # type: ignore

DefaultTermFormatter = _impl.SimpleTermFormatter

logger.debug("Loaded compatibility layer for JVM subtypes of " + str(TermFormatter.class_.getName()))
