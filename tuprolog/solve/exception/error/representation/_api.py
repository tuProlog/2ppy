from typing import Any

from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature

from ._definitions import Limit, RepresentationError

__all__ = ["limit", "representation_error"]


def representation_error(
    context: ExecutionContext, procedure: Signature, limit: Limit, cause: Any = None
) -> RepresentationError:
    return RepresentationError.of(context, procedure, limit, cause)


def limit(name: str | Term) -> Limit:
    if isinstance(name, str):
        return Limit.of(name)
    else:
        return Limit.fromTerm(name)
