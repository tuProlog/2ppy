from jpype import JImplements, JOverride
from tuprolog import logger
import jpype.imports
import it.unibo.tuprolog.core as _core # type: ignore




logger.debug("Loaded compatibility layer for JVM subtypes of " + str(TermVisitor.class_.getName()))
