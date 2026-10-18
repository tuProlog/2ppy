import importlib

import pytest

from tuprolog.core import atom, integer, struct
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error.type import (
    Type,
    TypeError,
    expected_type,
    type_error,
    type_error_for_argument,
    type_error_for_argument_list,
    type_error_for_goal,
    type_error_for_term,
)

from .helpers import solve_once, solver_raising

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


@pytest.mark.parametrize("name", TYPE_NAMES)
def test_type_values(name):
    expected = getattr(Type, name)
    assert expected_type(name.lower()) == expected
    assert expected_type(name) == expected
    assert expected_type(atom(name.lower())) == expected


def test_type_from_non_atom_term_is_none():
    assert expected_type(integer(1)) is None


def assert_type_error(error, expected, culprit, message):
    assert isinstance(error, TypeError)
    assert isinstance(error, LogicError)
    assert error.expected_type == expected
    assert error.culprit == culprit
    assert error.message == message
    assert error.extra_data == atom(message)
    assert error.getType() == struct("type_error", expected.toTerm(), culprit)
    assert error.error_struct == struct("error", error.getType(), atom(message))


def test_type_error(context):
    error = type_error(context, Type.INTEGER, atom("x"), "not an integer")
    assert_type_error(error, Type.INTEGER, atom("x"), "not an integer")


def test_type_error_raised_from_primitive_is_catchable():
    solver = solver_raising(te=lambda r: type_error(r.context, Type.ATOM, integer(1), "m"))
    caught = solve_once(solver, "catch(te, error(type_error(T, C), M), true)")
    assert caught.substitution.getByName("T") == atom("atom")
    assert caught.substitution.getByName("C") == integer(1)
    assert caught.substitution.getByName("M") == atom("m")


@pytest.mark.parametrize("index", [None, 0, 3])
def test_type_error_for_argument(context, procedure, index):
    error = type_error_for_argument(context, procedure, Type.ATOM, integer(1), index)
    prefix = "An argument" if index is None else f"The {index}-th argument"
    assert_type_error(
        error,
        Type.ATOM,
        integer(1),
        f"{prefix} of `foo/2` should be a `atom`, but `1` has been provided instead",
    )


@pytest.mark.parametrize("index", [None, 1])
def test_type_error_for_argument_list(context, procedure, index):
    error = type_error_for_argument_list(context, procedure, Type.ATOM, integer(1), index)
    prefix = "An argument" if index is None else f"The {index}-th argument"
    assert_type_error(
        error,
        Type.ATOM,
        integer(1),
        f"{prefix} of `foo/2` should be a list of `atom`, but `1` has been provided instead",
    )


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
