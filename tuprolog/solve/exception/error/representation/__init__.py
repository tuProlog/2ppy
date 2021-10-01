from typing import Union
# noinspection PyUnresolvedReferences
import jpype.imports

from tuprolog import logger
from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature

# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.exception.error as errors

RepresentationError = errors.RepresentationError

Limit = RepresentationError.Limit

LIMIT_CHARACTER = Limit.CHARACTER

LIMIT_CHARACTER_CODE = Limit.CHARACTER_CODE

LIMIT_IN_CHARACTER_CODE = Limit.IN_CHARACTER_CODE

LIMIT_MAX_ARITY = Limit.MAX_ARITY

LIMIT_MAX_INTEGER = Limit.MAX_INTEGER

LIMIT_MIN_INTEGER = Limit.MIN_INTEGER

LIMIT_OOP_OBJECT = Limit.OOP_OBJECT

LIMIT_TOO_MANY_VARIABLES = Limit.TOO_MANY_VARIABLES


def representation_error(
        context: ExecutionContext,
        procedure: Signature,
        limit: Limit,
        cause=None
) -> RepresentationError:
    return RepresentationError.of(context, procedure, limit, cause)


def limit(name: Union[str, Term]) -> Limit:
    if isinstance(name, str):
        return Limit.of(name)
    else:
        return Limit.fromTerm(name)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.RepresentationError.*")
