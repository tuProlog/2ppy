from tuprolog.core import atom, var
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error.instantiation import (
    InstantiationError,
    instantiation_error_for_argument,
    instantiation_error_for_goal,
)


def assert_instantiation_error(error, culprit, message):
    assert isinstance(error, InstantiationError)
    assert isinstance(error, LogicError)
    assert error.culprit == culprit
    assert error.message == message
    assert error.extra_data == atom(message)
    assert error.getType() == atom("instantiation_error")
    assert str(error.error_struct) == f"error(instantiation_error, '{message}')"


def test_instantiation_error_for_argument_without_index(context, procedure):
    x = var("X")
    error = instantiation_error_for_argument(context, procedure, x)
    assert_instantiation_error(
        error, x, "The argument `X` of foo/2 is unexpectedly not instantiated"
    )


def test_instantiation_error_for_goal(context, procedure):
    x = var("X")
    error = instantiation_error_for_goal(context, procedure, x)
    assert_instantiation_error(error, x, "Uninstantiated subgoal X in procedure foo/2")


def test_instantiation_error_for_argument_with_index(context, procedure):
    x = var("X")
    error = instantiation_error_for_argument(context, procedure, x, 2)
    assert_instantiation_error(
        error, x, "The 2-th argument `X` of foo/2 is unexpectedly not instantiated"
    )
