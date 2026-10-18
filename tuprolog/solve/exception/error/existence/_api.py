from tuprolog.core import Atom, Term
from tuprolog.solve import ExecutionContext, Signature

from ._definitions import ExistenceError, ObjectType

__all__ = [
    "existence_error",
    "existence_error_for_procedure",
    "existence_error_for_resource",
    "existence_error_for_source_sink",
    "existence_error_for_stream",
    "object_type",
]


def existence_error(
    context: ExecutionContext, type: ObjectType, culprit: Term, message: str
) -> ExistenceError:
    """Creates an existence error for any kind of object, with a custom message.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        type: the kind of the missing object (e.g. `OBJECT_OOP_METHOD`).
        culprit: the term naming the missing object.
        message: the error message.

    Returns:
        The error, thrown as `error(existence_error(Type, Culprit), Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> from tuprolog.core import atom
        >>> existence_error(context, OBJECT_OOP_METHOD, atom("foo"), "no method foo").type
        existence_error(oop_method, foo)
    """
    return ExistenceError.of(context, type, culprit, message)


def existence_error_for_source_sink(context: ExecutionContext, alias: Atom | str) -> ExistenceError:
    """Creates the existence error for a stream alias no stream has.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        alias: the alias, as an atom or a string.

    Returns:
        The error, thrown as `error(existence_error(source_sink, Alias), Message)`.
    """
    return ExistenceError.forSourceSink(context, alias)


def existence_error_for_procedure(
    context: ExecutionContext, procedure: Signature
) -> ExistenceError:
    """Creates the existence error for an undefined predicate.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        procedure: the signature of the undefined predicate.

    Returns:
        The error, thrown as `error(existence_error(procedure, Name/Arity), Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> existence_error_for_procedure(context, signature("foo", 1)).type
        existence_error(procedure, foo/1)
    """
    return ExistenceError.forProcedure(context, procedure)


def existence_error_for_stream(context: ExecutionContext, stream: Term) -> ExistenceError:
    """Creates the existence error for a stream that does not exist (e.g. a closed one).

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        stream: the term denoting the stream.

    Returns:
        The error, thrown as `error(existence_error(stream, Stream), Message)`.
    """
    return ExistenceError.forStream(context, stream)


def existence_error_for_resource(context: ExecutionContext, name: str) -> ExistenceError:
    """Creates the existence error for a missing resource.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        name: the name of the resource.

    Returns:
        The error, thrown as `error(existence_error(resource, Name), Message)`.
    """
    return ExistenceError.forResource(context, name)


def object_type(name: str | Term) -> ObjectType:
    # 2P-Kt's ObjectType.of/fromTerm, unlike other error enums, reject lower-case (Prolog) names
    """The `ObjectType` named by a string or an atom.

    Args:
        name: the name, as a string or an atom (case-insensitive, e.g. `"procedure"`), or another
            `tuprolog.core.Term`.

    Returns:
        The matching `ObjectType`; `None` for terms other than atoms.

    Raises:
        java.lang.IllegalArgumentException: if no `ObjectType` has that name.

    Note:
        Unlike the other error enumerations, 2P-Kt's `ObjectType.of` and `fromTerm` only accept
        upper-case names: this function upper-cases strings and atoms first.

    Examples:
        >>> from tuprolog.core import atom
        >>> from tuprolog.solve.exception.error.existence import *
        >>> object_type("procedure") == object_type(atom("procedure")) == OBJECT_PROCEDURE
        True
    """
    if isinstance(name, Atom):
        name = str(name.value)
    if isinstance(name, str):
        return ObjectType.of(name.upper())
    return ObjectType.fromTerm(name)
