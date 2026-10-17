from tuprolog.core import integer
from tuprolog.solve.function import Compute, ComputeResponse, compute_response


def test_compute_response_type_is_compute_response():
    assert ComputeResponse is Compute.Response


def test_compute_response_wraps_result():
    response = compute_response(integer(42))
    assert isinstance(response, Compute.Response)
    assert response.result == integer(42)
