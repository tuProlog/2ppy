from typing import Union
from tuprolog.core import Term, Atom
from tuprolog.solve import ExecutionContext, Signature
from ._definitions import ExistenceError, ObjectType


def existence_error(
        context: ExecutionContext,
        type: ObjectType,
        culprit: Term,
        message: str
) -> ExistenceError:
    return ExistenceError.of(context, type, culprit, message)


def existence_error_for_source_sink(
        context: ExecutionContext,
        alias: Union[Atom, str]
) -> ExistenceError:
    return ExistenceError.forSourceSink(context, alias)


def existence_error_for_procedure(
        context: ExecutionContext,
        procedure: Signature
) -> ExistenceError:
    return ExistenceError.forProcedure(context, procedure)


def existence_error_for_stream(
        context: ExecutionContext,
        stream: Term
) -> ExistenceError:
    return ExistenceError.forStream(context, stream)


def existence_error_for_resource(
        context: ExecutionContext,
        name: str
) -> ExistenceError:
    return ExistenceError.forResource(context, name)


def object_type(name: Union[str, Term]) -> ObjectType:
    if isinstance(name, str):
        return ObjectType.of(name)
    else:
        return ObjectType.fromTerm(name)
