from tuprolog import logger
from tuprolog.core import Var
from tuprolog.solve import ExecutionContext, Signature
import jpype.imports
import it.unibo.tuprolog.solve.exception.error as _errors # type: ignore


InstantiationError = _errors.InstantiationError


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


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.InstantiationError.*")
