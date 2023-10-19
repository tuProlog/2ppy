from tuprolog.core import Var
from tuprolog.solve import ExecutionContext, Signature
from ._definitions import InstantiationError


def instantiation_error_for_argument(
        context: ExecutionContext,
        procedure: Signature,
        variable: Var,
        index: int = None
) -> InstantiationError:
    return InstantiationError.forArgument(context, procedure, variable, index)


def instantiation_error_for_goal(
        context: ExecutionContext,
        procedure: Signature,
        variable: Var
) -> InstantiationError:
    return InstantiationError.forGoal(context, procedure, variable)
