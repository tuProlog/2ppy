import importlib

import pytest

from tuprolog.core import atom, integer, struct
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error.permission import (
    Operation,
    Permission,
    PermissionError,
    operation,
    permission_error,
    permission_type,
)

module = importlib.import_module("tuprolog.solve.exception.error.permission")

OPERATION_NAMES = [
    "ACCESS",
    "ADD_ALIAS",
    "CLOSE",
    "CREATE",
    "INPUT",
    "INVOKE",
    "MODIFY",
    "OPEN",
    "OUTPUT",
    "REPOSITION",
]

PERMISSION_NAMES = [
    "BINARY_STREAM",
    "FLAG",
    "OPERATOR",
    "PAST_END_OF_STREAM",
    "PRIVATE_PROCEDURE",
    "SOURCE_SINK",
    "STATIC_PROCEDURE",
    "OOP_METHOD",
    "STREAM",
    "TEXT_STREAM",
]


def test_enums_are_the_permission_error_ones():
    assert Operation is PermissionError.Operation
    assert Permission is PermissionError.Permission
    assert {str(o.name()) for o in Operation.values()} == set(OPERATION_NAMES)
    assert {str(p.name()) for p in Permission.values()} == set(PERMISSION_NAMES)


@pytest.mark.parametrize("name", OPERATION_NAMES)
def test_operation_values(name):
    expected = getattr(Operation, name)
    assert getattr(module, f"OPERATION_{name}") == expected
    assert operation(name.lower()) == expected
    assert operation(atom(name.lower())) == expected
    assert expected.operation == name.lower()
    assert expected.toTerm() == atom(name.lower())


@pytest.mark.parametrize("name", PERMISSION_NAMES)
def test_permission_values(name):
    expected = getattr(Permission, name)
    assert getattr(module, f"PERMISSION_{name}") == expected
    assert permission_type(name.lower()) == expected
    assert permission_type(atom(name.lower())) == expected
    assert expected.permission == name.lower()
    assert expected.toTerm() == atom(name.lower())


def test_operation_and_permission_from_non_atom_terms_are_none():
    assert operation(integer(1)) is None
    assert permission_type(integer(1)) is None


def test_permission_error(context, procedure):
    culprit = atom("bar")
    error = permission_error(
        context, procedure, Operation.MODIFY, Permission.STATIC_PROCEDURE, culprit
    )
    message = (
        "Permission error while executing foo/2: "
        "operation of type `modify` is not possible on static_procedure: bar"
    )
    assert isinstance(error, PermissionError)
    assert isinstance(error, LogicError)
    assert error.operation == Operation.MODIFY
    assert error.permission == Permission.STATIC_PROCEDURE
    assert error.culprit == culprit
    assert error.message == message
    assert error.extra_data == atom(message)
    assert error.getType() == struct(
        "permission_error", atom("modify"), atom("static_procedure"), culprit
    )
    assert error.error_struct == struct("error", error.getType(), atom(message))
