import it.unibo.tuprolog.solve.exception.error as errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "ERROR_FLOAT_OVERFLOW",
    "ERROR_INT_OVERFLOW",
    "ERROR_UNDEFINED",
    "ERROR_UNDERFLOW",
    "ERROR_ZERO_DIVISOR",
    "ErrorType",
    "EvaluationError",
]


EvaluationError = errors.EvaluationError


ErrorType = EvaluationError.Type


ERROR_INT_OVERFLOW = ErrorType.INT_OVERFLOW


ERROR_FLOAT_OVERFLOW = ErrorType.FLOAT_OVERFLOW


ERROR_UNDERFLOW = ErrorType.UNDERFLOW


ERROR_ZERO_DIVISOR = ErrorType.ZERO_DIVISOR


ERROR_UNDEFINED = ErrorType.UNDEFINED


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.EvaluationError.*")
