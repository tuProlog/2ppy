from typing import Union
from tuprolog.core import Term, atom
from tuprolog.solve import ExecutionContext
from ._definitions import EvaluationError, ErrorType


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
