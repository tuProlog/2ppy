from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.function import LogicFunction
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.function import Compute
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.function import ArithmeticUtilsKt

# noinspection PyUnresolvedReferences
from tuprolog.core import Term
# noinspection PyUnresolvedReferences
from tuprolog.solve import ExecutionContext, Signature, current_time_instant, MAX_TIMEOUT
# noinspection PyUnresolvedReferences
from tuprolog.solve.primitive import SolveRequest

from typing import List, Callable

ComputeRequest = Compute.Request

ComputeResponse = Compute.Request


@jpype.JImplements(LogicFunction)
class AbstractLogicFunction(object):
    @jpype.JOverride
    def compute(self, request: ComputeRequest) -> ComputeResponse:
        raise NotImplementedError()


def logic_function(callable: Callable[[ComputeRequest], ComputeResponse]) -> LogicFunction:
    class CallableToLogicFunctionAdapter(AbstractLogicFunction):
        def compute(self, request: ComputeRequest) -> ComputeResponse:
            return callable(request)

    return CallableToLogicFunctionAdapter()


def compute_request(
        signature: Signature,
        arguments: List[Term],
        context: ExecutionContext,
        issuing_instant: int = current_time_instant,
        max_duration: int = MAX_TIMEOUT
) -> ComputeRequest:
    return ComputeRequest(signature, arguments, context, issuing_instant, max_duration)


def compute_response(result: Term) -> ComputeResponse:
    return ComputeResponse(result)


def eval_as_expression(term: Term, request: SolveRequest, index: int = None) -> Term:
    return ArithmeticUtilsKt.evalAsExpression(term, request, index)


def eval_as_arithmetic_expression(term: Term, request: SolveRequest, index: int = None) -> Term:
    return ArithmeticUtilsKt.evalAsArithmeticExpression(term, request, index)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.function.*")
