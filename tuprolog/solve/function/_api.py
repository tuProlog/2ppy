"""The factory functions of logic functions, re-exported by `tuprolog.solve.function`."""

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
    """Creates a logic function from a Python function on compute requests.

    Unlike `function`, the Python function sees the whole request, including the solver's
    context, and works on terms.

    Args:
        callable: A function taking a `ComputeRequest`, and returning a `ComputeResponse` (e.g.
            via `request.reply_with(result)`).

    Returns:
        The logic function.

    Examples:
        >>> from tuprolog.core import integer
        >>> from tuprolog.solve.library import library
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> def count_arguments(request):
        ...     return request.reply_with(integer(len(request.arguments)))
        >>> count = logic_function(count_arguments)
        >>> solver = prolog_solver(libraries=library("my.lib", functions={"count/2": count}))
        >>> solver.solve_once("X is count(1, 2) * 10")["X"]
        20
    """

    class CallableToLogicFunctionAdapter(AbstractLogicFunction):
        def compute(self, request: ComputeRequest) -> ComputeResponse:
            return callable(request)

    return JObject(CallableToLogicFunctionAdapter(), LogicFunction)


def function(callable: Callable) -> LogicFunction:
    """Creates a logic function from a Python function on Python values.

    Args:
        callable: A function taking the evaluated arguments, converted to Python values (see
            `tuprolog.core.to_python`), and returning a Python value or a term (converted by
            `tuprolog.core.to_term`).

    Returns:
        The logic function.

    Note:
        Exceptions raised by `callable` propagate, as Python exceptions, out of the solving
        method (e.g. `Solver.solve_once`), rather than ending the resolution with a *halt*
        solution: raise `tuprolog.solve.exception` errors from primitives to report logic errors.

    Examples:
        >>> from tuprolog.solve.library import library
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> solver = prolog_solver(
        ...     libraries=library("my.lib", functions={"twice/1": function(lambda x: 2 * x)})
        ... )
        >>> solver.solve_once("X is twice(21)")["X"]
        42
    """

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
    """Creates a compute request, e.g. to test logic functions.

    Args:
        signature: The signature of the function.
        arguments: The arguments, as many as the arity of `signature` (or more, if variadic).
        context: The execution context of the solver.
        issuing_instant: When the request is issued, in milliseconds (see
            `tuprolog.solve.current_time_instant`); now, by default.
        max_duration: The maximum duration of the computation, in milliseconds; none by default.

    Returns:
        The compute request.

    Raises:
        java.lang.IllegalArgumentException: If the number of arguments does not match the arity.
    """
    if issuing_instant is None:
        issuing_instant = current_time_instant()
    return ComputeRequest(signature, jlist(arguments), context, issuing_instant, max_duration)


def compute_response(result: Term) -> ComputeResponse:
    """Creates a compute response, holding the result of a logic function.

    Args:
        result: The result.

    Returns:
        The compute response.

    Examples:
        >>> from tuprolog.core import integer
        >>> compute_response(integer(1)).result
        1
    """
    return ComputeResponse(result)


def _boxed_index(index: int | None) -> Any:
    return None if index is None else JObject(index, JClass("java.lang.Integer"))


def eval_as_expression(term: Term, request: SolveRequest, index: int | None = None) -> Term:
    """Evaluates a term as an expression, with the functions of the solver, in a primitive.

    Variables are left as they are; any other non-evaluable term raises an error.

    Args:
        term: The term to evaluate, e.g. an argument of the request.
        request: The request of the primitive (see `tuprolog.solve.primitive`).
        index: The (0-based) index of the argument `term` comes from, mentioned by errors.

    Returns:
        The value of the expression.

    Raises:
        tuprolog.solve.exception.error.TypeError: If a sub-term is not evaluable.
    """
    return ArithmeticUtilsKt.evalAsExpression(term, request, _boxed_index(index))


def eval_as_arithmetic_expression(
    term: Term, request: SolveRequest, index: int | None = None
) -> Term:
    """Evaluates a term as an arithmetic expression, as `is/2` does, in a primitive.

    Args:
        term: The term to evaluate, e.g. an argument of the request.
        request: The request of the primitive (see `tuprolog.solve.primitive`).
        index: The (0-based) index of the argument `term` comes from, mentioned by errors.

    Returns:
        The number the expression evaluates to (a `tuprolog.core.Numeric`).

    Raises:
        tuprolog.solve.exception.LogicError: If the expression is not instantiated or not
            evaluable, or does not evaluate to a number.

    Examples:
        >>> from tuprolog.core import integer, substitution
        >>> from tuprolog.solve.library import library
        >>> from tuprolog.solve.primitive import primitive
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> @primitive
        ... def double(request):
        ...     value = eval_as_arithmetic_expression(request.arguments[0], request, 0)
        ...     result = integer(value.int_value * 2)
        ...     yield request.reply_success(substitution({request.arguments[1]: result}))
        >>> solver = prolog_solver(libraries=library("my.lib", primitives={"double/2": double}))
        >>> solver.solve_once("double(1 + 2, X)")["X"]
        6
    """
    return ArithmeticUtilsKt.evalAsArithmeticExpression(term, request, _boxed_index(index))
