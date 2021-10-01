from typing import Union
from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.exception.error as errors
from tuprolog.core import Term, Atom
from tuprolog.solve import ExecutionContext, Signature

ExistenceError = errors.ExistenceError

ObjectType = ExistenceError.ObjectType

OBJECT_PROCEDURE = ObjectType.PROCEDURE

OBJECT_SOURCE_SINK = ObjectType.SOURCE_SINK

OBJECT_RESOURCE = ObjectType.RESOURCE

OBJECT_STREAM = ObjectType.STREAM

OBJECT_OOP_ALIAS = ObjectType.OOP_ALIAS

OBJECT_OOP_METHOD = ObjectType.OOP_METHOD

OBJECT_OOP_CONSTRUCTOR = ObjectType.OOP_CONSTRUCTOR

OBJECT_OOP_PROPERTY = ObjectType.OOP_PROPERTY


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


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.ExistenceError.*")
