import importlib

import pytest

from tuprolog.core import atom, integer, struct
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error.type import (
    Type,
    TypeError,
    type_error_for_goal,
    type_error_for_term,
)

# `error.type` is shadowed by the type() factory: get the sub-package from sys.modules
module = importlib.import_module("tuprolog.solve.exception.error.type")

TYPE_NAMES = [
    "ATOM",
    "ATOMIC",
    "BOOLEAN",
    "BYTE",
    "CALLABLE",
    "CHARACTER",
    "COMPOUND",
    "DEALIASING_EXPRESSION",
    "EVALUABLE",
    "FLOAT",
    "INTEGER",
    "IN_CHARACTER",
    "LIST",
    "NUMBER",
    "OBJECT_REFERENCE",
    "PAIR",
    "PREDICATE_INDICATOR",
    "REFERENCE",
    "TYPE_REFERENCE",
    "URL",
    "VARIABLE",
]


def test_type_is_the_expected_enum():
    assert Type is TypeError.Expected
    assert {str(t.name()) for t in Type.values()} == set(TYPE_NAMES)


def test_type_error_is_the_logic_one():
    assert TypeError.class_.getName() == "it.unibo.tuprolog.solve.exception.error.TypeError"


@pytest.mark.parametrize("name", TYPE_NAMES)
def test_type_constants(name):
    expected = getattr(Type, name)
    assert getattr(module, f"TYPE_{name}") == expected
    assert str(expected) == name.lower()
    assert expected.toTerm() == atom(name.lower())


def assert_type_error(error, expected, culprit, message):
    assert isinstance(error, TypeError)
    assert isinstance(error, LogicError)
    assert error.expected_type == expected
    assert error.culprit == culprit
    assert error.message == message
    assert error.extra_data == atom(message)
    assert error.getType() == struct("type_error", expected.toTerm(), culprit)
    assert error.error_struct == struct("error", error.getType(), atom(message))


def test_type_error_for_goal(context, procedure):
    error = type_error_for_goal(context, procedure, Type.CALLABLE, integer(1))
    assert_type_error(
        error, Type.CALLABLE, integer(1), "Subgoal `1` of foo/2 is not a callable term"
    )


@pytest.mark.xfail(
    strict=True,
    reason="type_error_for_term wraps TypeError.forTerm, which 2P-Kt does not define "
    "(neither in 0.31.16 nor later)",
)
def test_type_error_for_term(context):
    error = type_error_for_term(context, Type.ATOM, integer(1))
    assert isinstance(error, TypeError)
    assert error.getType() == struct("type_error", atom("atom"), integer(1))
