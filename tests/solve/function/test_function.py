import pytest

from tests.solve.primitive._support import RequestCapturer
from tuprolog.core import integer, var
from tuprolog.core.parsing import parse_term
from tuprolog.solve import MAX_TIMEOUT, current_time_instant, signature
from tuprolog.solve.exception.error import InstantiationError, TypeError
from tuprolog.solve.function import (
    Compute,
    ComputeRequest,
    ComputeResponse,
    compute_request,
    compute_response,
    eval_as_arithmetic_expression,
    eval_as_expression,
)


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
