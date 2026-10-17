import inspect

import pytest

from tests.solve.primitive._support import RequestCapturer
from tuprolog.core import atom, integer
from tuprolog.solve import MAX_TIMEOUT, current_time_instant, signature
from tuprolog.solve.primitive import SolveRequest, solve_request


@pytest.fixture(scope="module")
def capturer() -> RequestCapturer:
    return RequestCapturer()


@pytest.fixture
def context(capturer):
    return capturer.request().context


@pytest.mark.parametrize("arguments", [[atom("a")], (atom("a"),), iter([atom("a")])])
def test_solve_request_accepts_python_iterables(context, arguments):
    request = solve_request(signature("f", 1), arguments, context)
    assert isinstance(request, SolveRequest)
    assert list(request.arguments) == [atom("a")]
    assert request.signature == signature("f", 1)
    assert request.context == context
    assert str(request.query) == "f(a)"


def test_solve_request_explicit_instant_and_duration(context):
    request = solve_request(signature("f", 0), [], context, 10, 20)
    assert request.start_time == 10
    assert request.max_duration == 20


def test_solve_request_defaults(context):
    before = current_time_instant()
    request = solve_request(signature("f", 0), [], context)
    after = current_time_instant()
    assert before <= request.start_time <= after
    assert request.max_duration == MAX_TIMEOUT


def test_solve_request_issuing_instant_is_not_frozen_at_import_time():
    assert inspect.signature(solve_request).parameters["issuing_instant"].default is None


def test_solve_request_vararg_signature_accepts_more_arguments(context):
    request = solve_request(signature("f", 1, True), [atom("a"), integer(2)], context)
    assert len(request.arguments) == 2
