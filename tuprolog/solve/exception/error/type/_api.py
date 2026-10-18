from jpype import JInt

from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature

from ._definitions import Type, TypeError

__all__ = [
    "expected_type",
    "type_error",
    "type_error_for_argument",
    "type_error_for_argument_list",
    "type_error_for_goal",
    "type_error_for_term",
]


def type_error(context: ExecutionContext, expected: Type, actual: Term, message: str) -> TypeError:
    """Creates a type error with a custom message.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        expected: the expected type (e.g. `TYPE_ATOM`).
        actual: the offending term.
        message: the error message.

    Returns:
        The error, thrown as `error(type_error(Expected, Actual), Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> from tuprolog.core import integer
        >>> type_error(context, TYPE_ATOM, integer(1), "not an atom").error_struct
        error(type_error(atom, 1), 'not an atom')
    """
    return TypeError.of(context, expected, actual, message)


def type_error_for_argument_list(
    context: ExecutionContext,
    procedure: Signature,
    expected: Type,
    actual: Term,
    index: int | None = None,
) -> TypeError:
    """Creates the type error for an argument that should be a list of items of some type.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        procedure: the signature of the predicate raising the error (e.g. a request's `signature`).
        expected: the type the items should have.
        actual: the offending argument.
        index: the (0-based) position of the offending argument, if known (it only changes the
            message).

    Returns:
        The error, thrown as `error(type_error(Expected, Actual), Message)`.
    """
    return TypeError.forArgumentList(
        context, procedure, expected, actual, None if index is None else JInt(index)
    )


def type_error_for_argument(
    context: ExecutionContext,
    procedure: Signature,
    expected: Type,
    actual: Term,
    index: int | None = None,
) -> TypeError:
    """Creates the type error for an argument of a predicate not having the expected type.

    The usual way of reporting that a primitive received an argument of a wrong type.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        procedure: the signature of the predicate raising the error (e.g. a request's `signature`).
        expected: the expected type (e.g. `TYPE_INTEGER`).
        actual: the offending argument.
        index: the (0-based) position of the offending argument, if known (it only changes the
            message).

    Returns:
        The error, thrown as `error(type_error(Expected, Actual), Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> from tuprolog.core import atom
        >>> procedure = signature("foo", 2)
        >>> error = type_error_for_argument(context, procedure, TYPE_INTEGER, atom("a"), 0)
        >>> error.type
        type_error(integer, a)
        >>> error.message
        'The 0-th argument of `foo/2` should be a `integer`, but `a` has been provided instead'
    """
    return TypeError.forArgument(
        context, procedure, expected, actual, None if index is None else JInt(index)
    )


def type_error_for_term(
    context: ExecutionContext,
    expected: Type,
    actual_value: Term,
) -> TypeError:
    # 2P-Kt has no TypeError.forTerm (unlike DomainError.forTerm): its message format is mirrored
    """Creates the type error for a term not having the expected type.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        expected: the expected type.
        actual_value: the offending term.

    Returns:
        The error, thrown as `error(type_error(Expected, ActualValue), Message)`.

    Note:
        2P-Kt has no `TypeError.forTerm` (unlike `DomainError.forTerm`): this mirrors its message.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> from tuprolog.core import integer
        >>> type_error_for_term(context, TYPE_CALLABLE, integer(1)).message
        'Term `1` is not a valid callable term'
    """
    return TypeError.of(
        context, expected, actual_value, f"Term `{actual_value}` is not a valid {expected} term"
    )


def type_error_for_goal(
    context: ExecutionContext,
    procedure: Signature,
    expected: Type,
    actual: Term,
) -> TypeError:
    """Creates the type error for a sub-goal of a predicate not having the expected type.

    E.g. for `call/1` invoked with a non-callable goal.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        procedure: the signature of the predicate raising the error (e.g. a request's `signature`).
        expected: the expected type (usually `TYPE_CALLABLE`).
        actual: the offending sub-goal.

    Returns:
        The error, thrown as `error(type_error(Expected, Actual), Message)`.
    """
    return TypeError.forGoal(context, procedure, expected, actual)


def expected_type(name: str | Term) -> Type:
    """The `Type` named by a string or an atom.

    Args:
        name: the name, as a string (case-insensitive) or a `tuprolog.core.Term` (as in the error
            terms, e.g. `atom("integer")`).

    Returns:
        The matching `Type`; `None` for terms other than atoms.

    Raises:
        java.lang.IllegalArgumentException: if no `Type` has that name.

    Examples:
        >>> from tuprolog.core import atom
        >>> from tuprolog.solve.exception.error.type import *
        >>> expected_type("integer") == expected_type(atom("integer")) == TYPE_INTEGER
        True
    """
    if isinstance(name, str):
        return Type.of(name)
    else:
        return Type.fromTerm(name)
