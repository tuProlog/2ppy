import inspect

from tuprolog.solve.channel import input_store, output_store, std_in, std_out
from tuprolog.solve.exception import error
from tuprolog.solve.exception.error.syntax import syntax_error
from tuprolog.solve.exception.error.system import system_error
from tuprolog.solve.function import compute_request


def test_input_store_with_channels():
    store = input_store(std_in(), {"foo": std_in()})
    assert {"foo", "stdin"} <= {str(alias) for alias in store.keySet()}


def test_output_store_with_channels():
    store = output_store(std_out(), channels={"foo": std_out()})
    assert {"foo", "stdout", "stderr"} <= {str(alias) for alias in store.keySet()}


def test_syntax_error_is_not_shadowed_by_system_error():
    assert error.syntax_error is syntax_error
    assert error.system_error is system_error
    assert list(inspect.signature(error.syntax_error).parameters) == ["context", "message"]


def test_compute_request_issuing_instant_defaults_to_now():
    assert inspect.signature(compute_request).parameters["issuing_instant"].default is None
