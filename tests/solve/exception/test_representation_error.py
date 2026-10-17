import importlib

import pytest

from tuprolog.core import atom, integer, struct
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error.representation import (
    Limit,
    RepresentationError,
    limit,
    representation_error,
)

module = importlib.import_module("tuprolog.solve.exception.error.representation")

LIMIT_NAMES = [
    "CHARACTER",
    "CHARACTER_CODE",
    "IN_CHARACTER_CODE",
    "MAX_ARITY",
    "MAX_INTEGER",
    "MIN_INTEGER",
    "OOP_OBJECT",
    "TOO_MANY_VARIABLES",
]


def test_limit_is_the_limit_enum():
    assert Limit is RepresentationError.Limit
    assert {str(lim.name()) for lim in Limit.values()} == set(LIMIT_NAMES)


@pytest.mark.parametrize("name", LIMIT_NAMES)
def test_limit_values(name):
    expected = getattr(Limit, name)
    assert getattr(module, f"LIMIT_{name}") == expected
    assert limit(name.lower()) == expected
    assert limit(name) == expected
    assert limit(atom(name.lower())) == expected
    assert expected.limit == name.lower()
    assert expected.toTerm() == atom(name.lower())


def test_limit_from_non_atom_term_is_none():
    assert limit(integer(1)) is None


def test_representation_error(context, procedure):
    error = representation_error(context, procedure, Limit.MAX_ARITY)
    assert isinstance(error, RepresentationError)
    assert isinstance(error, LogicError)
    assert error.limit == Limit.MAX_ARITY
    assert error.cause is None
    assert str(error.message).startswith(
        "Reached representation limit while executing `foo/2`: max_arity"
    )
    assert error.extra_data == atom(error.message)
    assert error.getType() == struct("representation_error", atom("max_arity"))
    assert error.error_struct == struct("error", error.getType(), atom(error.message))


def test_representation_error_with_cause(context, procedure):
    cause = representation_error(context, procedure, Limit.MAX_INTEGER)
    error = representation_error(context, procedure, Limit.MAX_ARITY, cause)
    assert error.cause == cause
    assert str(error.message).endswith(f". {cause.message}")


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt RepresentationError.of() appends 'null' to the message when there is no cause",
)
def test_representation_error_message_without_cause(context, procedure):
    error = representation_error(context, procedure, Limit.MAX_ARITY)
    assert error.message == "Reached representation limit while executing `foo/2`: max_arity"
