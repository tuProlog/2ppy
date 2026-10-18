from jpype import JInt

from tuprolog.core import Var
from tuprolog.solve import ExecutionContext, Signature

from ._definitions import InstantiationError

__all__ = ["instantiation_error_for_argument", "instantiation_error_for_goal"]


def instantiation_error_for_argument(
    context: ExecutionContext, procedure: Signature, variable: Var, index: int | None = None
) -> InstantiationError:
    return InstantiationError.forArgument(
        context, procedure, variable, None if index is None else JInt(index)
    )


def instantiation_error_for_goal(
    context: ExecutionContext, procedure: Signature, variable: Var
) -> InstantiationError:
    return InstantiationError.forGoal(context, procedure, variable)
