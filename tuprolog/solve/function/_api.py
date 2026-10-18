from collections.abc import Callable, Iterable
from typing import Any

from jpype import JClass, JObject

from tuprolog.core import Term, to_python, to_term
from tuprolog.jvmutils import jlist
from tuprolog.solve import MAX_TIMEOUT, ExecutionContext, Signature, current_time_instant
from tuprolog.solve.primitive import SolveRequest

from ._definitions import (
    AbstractLogicFunction,
    ArithmeticUtilsKt,
    ComputeRequest,
    ComputeResponse,
    LogicFunction,
)

__all__ = [
    "compute_request",
    "compute_response",
    "eval_as_arithmetic_expression",
    "eval_as_expression",
    "function",
    "logic_function",
]


def logic_function(callable: Callable[[ComputeRequest], ComputeResponse]) -> LogicFunction:
    class CallableToLogicFunctionAdapter(AbstractLogicFunction):
        def compute(self, request: ComputeRequest) -> ComputeResponse:
            return callable(request)

    return JObject(CallableToLogicFunctionAdapter(), LogicFunction)


def function(callable: Callable) -> LogicFunction:
    """A logic function (for `is/2` and arithmetic comparisons) from a Python function taking
    its evaluated arguments as Python values, and returning a Python value (see
    `tuprolog.core.to_python` and `to_term`)."""

    def compute(request: ComputeRequest) -> ComputeResponse:
        result = callable(*(to_python(argument) for argument in request.arguments))
        return compute_response(to_term(result))

    return logic_function(compute)


def compute_request(
    signature: Signature,
    arguments: Iterable[Term],
    context: ExecutionContext,
    issuing_instant: int | None = None,
    max_duration: int = MAX_TIMEOUT,
) -> ComputeRequest:
    if issuing_instant is None:
        issuing_instant = current_time_instant()
    return ComputeRequest(signature, jlist(arguments), context, issuing_instant, max_duration)


def compute_response(result: Term) -> ComputeResponse:
    return ComputeResponse(result)


def _boxed_index(index: int | None) -> Any:
    return None if index is None else JObject(index, JClass("java.lang.Integer"))


def eval_as_expression(term: Term, request: SolveRequest, index: int | None = None) -> Term:
    return ArithmeticUtilsKt.evalAsExpression(term, request, _boxed_index(index))


def eval_as_arithmetic_expression(
    term: Term, request: SolveRequest, index: int | None = None
) -> Term:
    return ArithmeticUtilsKt.evalAsArithmeticExpression(term, request, _boxed_index(index))
