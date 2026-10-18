import importlib

import pytest

from tuprolog.core import atom, indicator, integer, struct
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error.existence import (
    ExistenceError,
    ObjectType,
    existence_error,
    existence_error_for_procedure,
    existence_error_for_resource,
    existence_error_for_source_sink,
    existence_error_for_stream,
    object_type,
)

module = importlib.import_module("tuprolog.solve.exception.error.existence")

OBJECT_TYPE_NAMES = [
    "PROCEDURE",
    "SOURCE_SINK",
    "RESOURCE",
    "STREAM",
    "OOP_ALIAS",
    "OOP_METHOD",
    "OOP_CONSTRUCTOR",
    "OOP_PROPERTY",
]


def test_object_type_is_the_object_type_enum():
    assert ObjectType is ExistenceError.ObjectType
    assert {str(t.name()) for t in ObjectType.values()} == set(OBJECT_TYPE_NAMES)


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_object_type_values(name):
    expected = getattr(ObjectType, name)
    assert getattr(module, f"OBJECT_{name}") == expected
    assert object_type(name) == expected
    assert str(expected) == name.lower()
    assert expected.toTerm() == atom(name.lower())


# 2P-Kt's ObjectType.of() lacks uppercase(), unlike all other error enums: object_type() adds it
@pytest.mark.parametrize("name", ["procedure", atom("procedure")], ids=["str", "atom"])
def test_object_type_from_lower_case_name(name):
    assert object_type(name) == ObjectType.PROCEDURE


def test_object_type_from_non_atom_term_is_none():
    assert object_type(integer(1)) is None


def assert_existence_error(error, expected, culprit, message):
    assert isinstance(error, ExistenceError)
    assert isinstance(error, LogicError)
    assert error.expected_object == expected
    assert error.culprit == culprit
    assert error.message == message
    assert error.extra_data == atom(message)
    assert error.getType() == struct("existence_error", expected.toTerm(), culprit)
    assert error.error_struct == struct("error", error.getType(), atom(message))


def test_existence_error(context):
    error = existence_error(context, ObjectType.OOP_METHOD, atom("m"), "no such method")
    assert_existence_error(error, ObjectType.OOP_METHOD, atom("m"), "no such method")


def test_existence_error_for_procedure(context, procedure):
    error = existence_error_for_procedure(context, procedure)
    assert_existence_error(
        error, ObjectType.PROCEDURE, indicator("foo", 2), "Procedure `foo/2` does not exist"
    )


@pytest.mark.parametrize("alias", ["out", atom("out")], ids=["str", "atom"])
def test_existence_error_for_source_sink(context, alias):
    error = existence_error_for_source_sink(context, alias)
    assert_existence_error(
        error, ObjectType.SOURCE_SINK, atom("out"), "There exists no stream whose alias is `out`"
    )


def test_existence_error_for_stream(context):
    stream = struct("stream", integer(3))
    error = existence_error_for_stream(context, stream)
    assert_existence_error(error, ObjectType.STREAM, stream, "No such a stream exists: stream(3)")


def test_existence_error_for_resource(context):
    error = existence_error_for_resource(context, "file.pl")
    assert_existence_error(
        error, ObjectType.RESOURCE, atom("file.pl"), "There exists no such a resource `file.pl`"
    )
