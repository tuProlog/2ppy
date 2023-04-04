from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype
import jpype.imports
from tuprolog.core import TermFormatter
import it.unibo.tuprolog.core.impl as _impl

DefaultTermFormatter = _impl.SimpleTermFormatter

logger.debug("Loaded compatibility layer for JVM subtypes of " + str(TermFormatter.class_.getName()))
