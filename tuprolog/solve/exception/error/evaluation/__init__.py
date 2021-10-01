from typing import Union
from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.exception.error as errors
from tuprolog.core import Term, atom
from tuprolog.solve import ExecutionContext

EvaluationError = errors.EvaluationError

ErrorType = EvaluationError.Type

ERROR_INT_OVERFLOW = ErrorType.INT_OVERFLOW

ERROR_FLOAT_OVERFLOW = ErrorType.FLOAT_OVERFLOW

ERROR_UNDERFLOW = ErrorType.UNDERFLOW

ERROR_ZERO_DIVISOR = ErrorType.ZERO_DIVISOR

ERROR_UNDEFINED = ErrorType.UNDEFINED


def evaluation_error(
        context: ExecutionContext,
        type: ErrorType,
        message: str
) -> EvaluationError:
    return EvaluationError(message, None, context, type, atom(message))


def error_type(name: Union[str, Term]) -> ErrorType:
    if isinstance(name, str):
        return ErrorType.valueOf(name)
    else:
        return ErrorType.fromTerm(name)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.EvaluationError.*")
