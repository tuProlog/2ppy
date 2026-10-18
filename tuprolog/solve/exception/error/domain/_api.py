from collections.abc import Iterable

from jpype import JInt

from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature

from ._definitions import Domain, DomainError

__all__ = [
    "domain_error_for_argument",
    "domain_error_for_flag_values",
    "domain_error_for_goal",
    "domain_error_for_term",
    "expected_domain",
]


def domain_error_for_flag_values(
    context: ExecutionContext,
    procedure: Signature,
    flag_values: Iterable[Term],
    actual: Term,
    index: int | None = None,
) -> DomainError:
    """Creates the domain error for an argument that should be one of some values, e.g. of a flag.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        procedure: the signature of the predicate raising the error (e.g. a request's `signature`).
        flag_values: the admissible values.
        actual: the offending argument.
        index: the (0-based) position of the offending argument, if known (it only changes the
            message).

    Returns:
        The error, thrown as `error(domain_error(flag_value, Actual), Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> from tuprolog.core import atom
        >>> error = domain_error_for_flag_values(
        ...     context, signature("foo", 1), [atom("on"), atom("off")], atom("maybe"), 0
        ... )
        >>> error.type
        domain_error(flag_value, maybe)
    """
    return DomainError.forFlagValues(
        context, procedure, flag_values, actual, None if index is None else JInt(index)
    )


def domain_error_for_argument(
    context: ExecutionContext,
    procedure: Signature,
    expected: Domain,
    actual: Term,
    index: int | None = None,
) -> DomainError:
    """Creates the domain error for an argument of a predicate outside the expected domain.

    The usual way of reporting that a primitive received an argument of the right type but with an
    inadmissible value.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        procedure: the signature of the predicate raising the error (e.g. a request's `signature`).
        expected: the expected domain (e.g. `DOMAIN_NOT_LESS_THAN_ZERO`).
        actual: the offending argument.
        index: the (0-based) position of the offending argument, if known (it only changes the
            message).

    Returns:
        The error, thrown as `error(domain_error(Expected, Actual), Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> from tuprolog.core import integer
        >>> procedure = signature("foo", 2)
        >>> domain = DOMAIN_NOT_LESS_THAN_ZERO
        >>> error = domain_error_for_argument(context, procedure, domain, integer(-1), 1)
        >>> error.type
        domain_error(not_less_than_zero, -1)
    """
    return DomainError.forArgument(
        context, procedure, expected, actual, None if index is None else JInt(index)
    )


def domain_error_for_term(
    context: ExecutionContext,
    expected: Domain,
    actual_value: Term,
) -> DomainError:
    """Creates the domain error for a term outside the expected domain.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        expected: the expected domain.
        actual_value: the offending term.

    Returns:
        The error, thrown as `error(domain_error(Expected, ActualValue), Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> from tuprolog.core import atom
        >>> domain_error_for_term(context, DOMAIN_IO_MODE, atom("rw")).message
        'Term `rw` is not a valid io_mode'
    """
    return DomainError.forTerm(context, expected, actual_value)


def domain_error_for_goal(
    context: ExecutionContext,
    procedure: Signature,
    expected: Domain,
    actual: Term,
) -> DomainError:
    """Creates the domain error for a sub-goal of a predicate outside the expected domain.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        procedure: the signature of the predicate raising the error (e.g. a request's `signature`).
        expected: the expected domain (e.g. `DOMAIN_CLAUSE`).
        actual: the offending sub-goal.

    Returns:
        The error, thrown as `error(domain_error(Expected, Actual), Message)`.
    """
    return DomainError.forGoal(context, procedure, expected, actual)


def expected_domain(name: str | Term) -> Domain:
    """The `Domain` named by a string or an atom.

    Args:
        name: the name, as a string (case-insensitive) or a `tuprolog.core.Term` (as in the error
            terms, e.g. `atom("io_mode")`).

    Returns:
        The matching `Domain`; `None` for terms other than atoms.

    Raises:
        java.lang.IllegalArgumentException: if no `Domain` has that name.

    Examples:
        >>> from tuprolog.core import atom
        >>> from tuprolog.solve.exception.error.domain import *
        >>> expected_domain("io_mode") == expected_domain(atom("io_mode")) == DOMAIN_IO_MODE
        True
    """
    if isinstance(name, str):
        return Domain.of(name)
    else:
        return Domain.fromTerm(name)
