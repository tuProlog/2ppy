import pytest

from tests.solve.primitive._support import RequestCapturer, bindings, python_int, solve_all
from tuprolog.core import integer, var
from tuprolog.core.parsing import parse_term
from tuprolog.solve import MAX_TIMEOUT, current_time_instant, signature
from tuprolog.solve.exception.error import InstantiationError, TypeError
from tuprolog.solve.function import (
    AbstractLogicFunction,
    Compute,
    ComputeRequest,
    ComputeResponse,
    LogicFunction,
    compute_request,
    compute_response,
    eval_as_arithmetic_expression,
    eval_as_expression,
    logic_function,
)
from tuprolog.solve.library import library
from tuprolog.solve.prolog import prolog_solver


def test_compute_response_type_is_compute_response():
    assert ComputeResponse is Compute.Response


def test_compute_response_wraps_result():
    response = compute_response(integer(42))
    assert isinstance(response, Compute.Response)
    assert response.result == integer(42)


@pytest.fixture(scope="module")
def capturer() -> RequestCapturer:
    return RequestCapturer()


@pytest.fixture
def context(capturer):
    return capturer.request().context


@pytest.mark.parametrize("arguments", [[integer(1)], (integer(1),), iter([integer(1)])])
def test_compute_request_accepts_python_iterables(context, arguments):
    request = compute_request(signature("f", 1), arguments, context)
    assert isinstance(request, ComputeRequest)
    assert list(request.arguments) == [integer(1)]
    assert request.signature == signature("f", 1)
    assert request.context == context


def test_compute_request_explicit_instant_and_duration(context):
    request = compute_request(signature("f", 0), [], context, 10, 20)
    assert request.request_issuing_instant == 10
    assert request.execution_max_duration == 20


def test_compute_request_defaults(context):
    before = current_time_instant()
    request = compute_request(signature("f", 0), [], context)
    after = current_time_instant()
    assert before <= request.request_issuing_instant <= after
    assert request.execution_max_duration == MAX_TIMEOUT


EXPRESSIONS = [("1 + 2 * 3", "7"), ("10 / 4", "2.5"), ("2 ** 3", "8.0"), ("abs(-3) - 1", "2")]


@pytest.mark.parametrize("index", [None, 0])
@pytest.mark.parametrize("expression, expected", EXPRESSIONS)
def test_eval_as_expression(capturer, expression, expected, index):
    request = capturer.request(parse_term(expression))
    result = eval_as_expression(request.arguments[0], request, index)
    assert str(result) == expected


@pytest.mark.parametrize("index", [None, 0])
@pytest.mark.parametrize("expression, expected", EXPRESSIONS)
def test_eval_as_arithmetic_expression(capturer, expression, expected, index):
    request = capturer.request(parse_term(expression))
    result = eval_as_arithmetic_expression(request.arguments[0], request, index)
    assert result.is_number
    assert str(result) == expected


def test_eval_as_expression_leaves_variables_alone(capturer):
    request = capturer.request(var("X"))
    assert eval_as_expression(request.arguments[0], request, 0).is_var


def test_eval_as_arithmetic_expression_of_variable_raises_instantiation_error(capturer):
    request = capturer.request(var("X"))
    with pytest.raises(InstantiationError):
        eval_as_arithmetic_expression(request.arguments[0], request, 0)


@pytest.mark.parametrize("evaluate", [eval_as_expression, eval_as_arithmetic_expression])
def test_eval_of_non_evaluable_raises_type_error(capturer, evaluate):
    request = capturer.request(parse_term("foo + 1"))
    with pytest.raises(TypeError) as info:
        evaluate(request.arguments[0], request, 0)
    assert "evaluable" in str(info.value.error_struct)


# --- logic functions implemented in Python, end to end ---


def _double(request):
    return compute_response(integer(python_int(request.arguments[0]) * 2))


def _solver_with_functions(**functions):
    lib = library(
        "lib.functions",
        functions={signature(name, arity): f for name, (arity, f) in functions.items()},
    )
    return prolog_solver(libraries=lib)


def test_logic_function_is_a_logic_function():
    assert isinstance(logic_function(_double), LogicFunction)


def test_abstract_logic_function_cannot_compute():
    with pytest.raises(NotImplementedError):
        AbstractLogicFunction().compute(None)


def test_logic_function_in_is():
    solver = _solver_with_functions(double=(1, logic_function(_double)))
    assert bindings(solve_all(solver, "X is double(21)"), "X") == ["42"]
    assert bindings(solve_all(solver, "X is double(1 + 2) * 2"), "X") == ["12"]
    assert bindings(solve_all(solver, "X is double(double(1))"), "X") == ["4"]


def test_logic_function_in_comparisons():
    solver = _solver_with_functions(double=(1, logic_function(_double)))
    assert solve_all(solver, "double(2) =:= 4")[0].is_yes
    assert solve_all(solver, "double(2) > 5")[0].is_no


def test_logic_function_receives_request():
    seen = []

    def spy(request):
        seen.append(request)
        return compute_response(integer(0))

    solver = _solver_with_functions(spy=(2, logic_function(spy)))
    assert solve_all(solver, "X is spy(1, 2)")[0].is_yes
    request = seen[-1]
    assert isinstance(request, ComputeRequest)
    assert request.signature == signature("spy", 2)
    assert [str(a) for a in request.arguments] == ["1", "2"]


def test_nullary_logic_function():
    solver = _solver_with_functions(
        forty_two=(0, logic_function(lambda r: compute_response(integer(42))))
    )
    assert bindings(solve_all(solver, "X is forty_two"), "X") == ["42"]


def test_logic_function_reply_with():
    solver = _solver_with_functions(one=(0, logic_function(lambda r: r.reply_with(integer(1)))))
    assert bindings(solve_all(solver, "X is one + 1"), "X") == ["2"]


def test_subclassing_abstract_logic_function():
    class Triple(AbstractLogicFunction):
        def compute(self, request):
            return compute_response(integer(python_int(request.arguments[0]) * 3))

    solver = _solver_with_functions(triple=(1, Triple()))
    assert bindings(solve_all(solver, "X is triple(3)"), "X") == ["9"]


def test_python_exceptions_in_logic_functions_propagate():
    def broken(request):
        raise ValueError("boom")

    solver = _solver_with_functions(broken=(0, logic_function(broken)))
    with pytest.raises(ValueError, match="boom"):
        solve_all(solver, "X is broken")
