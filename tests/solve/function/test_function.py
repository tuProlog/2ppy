import pytest

from tests.solve.primitive._support import RequestCapturer
from tuprolog.core import integer
from tuprolog.solve import MAX_TIMEOUT, current_time_instant, signature
from tuprolog.solve.function import (
    Compute,
    ComputeRequest,
    ComputeResponse,
    compute_request,
    compute_response,
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
