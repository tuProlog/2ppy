from tuprolog import logger
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports
import it.unibo.tuprolog.core.visitors as _visitors

DefaultTermVisitor = _visitors.DefaultTermVisitor

logger.debug("Loaded compatibility layer for JVM subtypes of " + str(DefaultTermVisitor.class_.getName()))
