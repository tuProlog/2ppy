from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature

from ._definitions import Operation, Permission, PermissionError

__all__ = ["operation", "permission_error", "permission_type"]


def permission_error(
    context: ExecutionContext,
    procedure: Signature,
    operation: Operation,
    permission: Permission,
    culprit: Term,
) -> PermissionError:
    """Creates a permission error.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        procedure: the signature of the predicate raising the error (e.g. a request's `signature`).
        operation: the attempted operation (e.g. `OPERATION_MODIFY`).
        permission: the kind of the object (e.g. `PERMISSION_STATIC_PROCEDURE`).
        culprit: the object.

    Returns:
        The error, thrown as `error(permission_error(Operation, Permission, Culprit), Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> from tuprolog.core import indicator
        >>> error = permission_error(
        ...     context,
        ...     signature("assertz", 1),
        ...     OPERATION_MODIFY,
        ...     PERMISSION_STATIC_PROCEDURE,
        ...     indicator("foo", 2),
        ... )
        >>> error.type
        permission_error(modify, static_procedure, foo/2)
    """
    return PermissionError.of(context, procedure, operation, permission, culprit)


def operation(name: str | Term) -> Operation:
    """The `Operation` named by a string or an atom.

    Args:
        name: the name, as a string (case-insensitive) or a `tuprolog.core.Term` (as in the error
            terms, e.g. `atom("modify")`).

    Returns:
        The matching `Operation`; `None` for terms other than atoms.

    Raises:
        java.lang.IllegalArgumentException: if no `Operation` has that name.

    Examples:
        >>> from tuprolog.core import atom
        >>> from tuprolog.solve.exception.error.permission import *
        >>> operation("modify") == operation(atom("modify")) == OPERATION_MODIFY
        True
    """
    if isinstance(name, str):
        return Operation.of(name)
    else:
        return Operation.fromTerm(name)


def permission_type(name: str | Term) -> Permission:
    """The `Permission` named by a string or an atom.

    Args:
        name: the name, as a string (case-insensitive) or a `tuprolog.core.Term` (as in the error
            terms, e.g. `atom("static_procedure")`).

    Returns:
        The matching `Permission`; `None` for terms other than atoms.

    Raises:
        java.lang.IllegalArgumentException: if no `Permission` has that name.

    Examples:
        >>> from tuprolog.solve.exception.error.permission import *
        >>> permission_type("static_procedure") == PERMISSION_STATIC_PROCEDURE
        True
    """
    if isinstance(name, str):
        return Permission.of(name)
    else:
        return Permission.fromTerm(name)
