from typing import Union
from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature
from ._definitions import RepresentationError, Limit


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
