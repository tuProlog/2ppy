from jpype import JInt

from tuprolog.core import Var
from tuprolog.solve import ExecutionContext, Signature

from ._definitions import InstantiationError

__all__ = ["instantiation_error_for_argument", "instantiation_error_for_goal"]


def instantiation_error_for_argument(
    context: ExecutionContext, procedure: Signature, variable: Var, index: int | None = None
) -> InstantiationError:
    """Creates the instantiation error for an unbound argument of a predicate.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        procedure: the signature of the predicate raising the error (e.g. a request's `signature`).
        variable: the unbound variable.
        index: the (0-based) position of the offending argument, if known (it only changes the
            message).

    Returns:
        The error, thrown as `error(instantiation_error, Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> from tuprolog.core import var
        >>> error = instantiation_error_for_argument(context, signature("foo", 2), var("X"), 0)
        >>> error.type
        instantiation_error
        >>> error.message
        'The 0-th argument `X` of foo/2 is unexpectedly not instantiated'
    """
    return InstantiationError.forArgument(
        context, procedure, variable, None if index is None else JInt(index)
    )


def instantiation_error_for_goal(
    context: ExecutionContext, procedure: Signature, variable: Var
) -> InstantiationError:
    """Creates the instantiation error for an unbound sub-goal of a predicate (e.g. `call(X)`).

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        procedure: the signature of the predicate raising the error (e.g. a request's `signature`).
        variable: the unbound sub-goal.

    Returns:
        The error, thrown as `error(instantiation_error, Message)`.
    """
    return InstantiationError.forGoal(context, procedure, variable)
