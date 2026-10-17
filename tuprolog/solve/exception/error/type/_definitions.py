from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.exception.error as _errors  # type: ignore


TypeError = _errors.TypeError


Type = TypeError.Expected


TYPE_ATOM = Type.ATOM


TYPE_ATOMIC = Type.ATOMIC


TYPE_BOOLEAN = Type.BOOLEAN


TYPE_BYTE = Type.BYTE


TYPE_CALLABLE = Type.CALLABLE


TYPE_CHARACTER = Type.CHARACTER


TYPE_COMPOUND = Type.COMPOUND


TYPE_DEALIASING_EXPRESSION = Type.DEALIASING_EXPRESSION


TYPE_EVALUABLE = Type.EVALUABLE


TYPE_FLOAT = Type.FLOAT


TYPE_INTEGER = Type.INTEGER


TYPE_IN_CHARACTER = Type.IN_CHARACTER


TYPE_LIST = Type.LIST


TYPE_NUMBER = Type.NUMBER


TYPE_OBJECT_REFERENCE = Type.OBJECT_REFERENCE


TYPE_PAIR = Type.PAIR


TYPE_PREDICATE_INDICATOR = Type.PREDICATE_INDICATOR


TYPE_REFERENCE = Type.REFERENCE


TYPE_TYPE_REFERENCE = Type.TYPE_REFERENCE


TYPE_URL = Type.URL


TYPE_VARIABLE = Type.VARIABLE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.TypeError.*")
