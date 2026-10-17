import importlib

import pytest

from tuprolog.core import atom, integer, struct
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error.evaluation import (
    ErrorType,
    EvaluationError,
    error_type,
    evaluation_error,
)

module = importlib.import_module("tuprolog.solve.exception.error.evaluation")

TYPE_NAMES = ["INT_OVERFLOW", "FLOAT_OVERFLOW", "UNDERFLOW", "ZERO_DIVISOR", "UNDEFINED"]


def test_error_type_is_the_type_enum():
    assert ErrorType is EvaluationError.Type
    assert {str(t.name()) for t in ErrorType.values()} == set(TYPE_NAMES)


@pytest.mark.parametrize("name", TYPE_NAMES)
def test_error_type_values(name):
    expected = getattr(ErrorType, name)
    assert getattr(module, f"ERROR_{name}") == expected
    assert error_type(name) == expected
    assert error_type(atom(name.lower())) == expected
    assert str(expected) == name.lower()
    assert expected.toTerm() == atom(name.lower())


def test_error_type_from_non_atom_or_unknown_term_is_none():
    assert error_type(integer(0)) is None
    assert error_type(atom("not_an_error_type")) is None


@pytest.mark.parametrize("name", TYPE_NAMES)
def test_evaluation_error(context, name):
    kind = getattr(ErrorType, name)
    error = evaluation_error(context, kind, "something went wrong")
    assert isinstance(error, EvaluationError)
    assert isinstance(error, LogicError)
    assert error.error_type == kind
    assert error.message == "something went wrong"
    assert error.extra_data == atom("something went wrong")
    assert error.cause is None
    assert error.context == context
    assert error.getType() == struct("evaluation_error", atom(name.lower()))
    assert error.error_struct == struct(
        "error", struct("evaluation_error", atom(name.lower())), atom("something went wrong")
    )
