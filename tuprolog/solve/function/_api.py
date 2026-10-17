from collections.abc import Callable

from tuprolog.core import Term
from tuprolog.solve import MAX_TIMEOUT, ExecutionContext, Signature, current_time_instant
from tuprolog.solve.primitive import SolveRequest

from ._definitions import (
    AbstractLogicFunction,
    ArithmeticUtilsKt,
    ComputeRequest,
    ComputeResponse,
    LogicFunction,
)


def logic_function(callable: Callable[[ComputeRequest], ComputeResponse]) -> LogicFunction:
    class CallableToLogicFunctionAdapter(AbstractLogicFunction):
        def compute(self, request: ComputeRequest) -> ComputeResponse:
            return callable(request)

    return CallableToLogicFunctionAdapter()


def compute_request(
    signature: Signature,
    arguments: list[Term],
    context: ExecutionContext,
    issuing_instant: int = current_time_instant,  # type: ignore[assignment]
    max_duration: int = MAX_TIMEOUT,
) -> ComputeRequest:
    return ComputeRequest(signature, arguments, context, issuing_instant, max_duration)


def compute_response(result: Term) -> ComputeResponse:
    return ComputeResponse(result)


def eval_as_expression(term: Term, request: SolveRequest, index: int | None = None) -> Term:
    return ArithmeticUtilsKt.evalAsExpression(term, request, index)


def eval_as_arithmetic_expression(
    term: Term, request: SolveRequest, index: int | None = None
) -> Term:
    return ArithmeticUtilsKt.evalAsArithmeticExpression(term, request, index)
