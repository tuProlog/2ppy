from tuprolog import logger
import jpype.imports
import it.unibo.tuprolog.solve.problog as _problog # type: ignore

Operators = _problog.Operators

ANNOTATION_OPERATOR = Operators.ANNOTATION_OPERATOR

PROBLOG_SPECIFIC_OPERATORS = Operators.PROBLOG_SPECIFIC_OPERATORS

PROBLOG_OPERATORS = Operators.PROBLOG_OPERATORS

logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.problog.operators")
