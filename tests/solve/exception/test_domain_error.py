import importlib

import pytest

from tuprolog.core import atom, integer, struct
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error.domain import (
    Domain,
    DomainError,
    domain,
    domain_error_for_argument,
    domain_error_for_flag_values,
    domain_error_for_goal,
    domain_error_for_term,
)

# `error.domain` is shadowed by the domain() factory: get the sub-package from sys.modules
module = importlib.import_module("tuprolog.solve.exception.error.domain")

DOMAIN_NAMES = [
    "ATOM_PROPERTY",
    "BUFFERING_MODE",
    "CHARACTER_CODE_LIST",
    "CLOSE_OPTION",
    "DATE_TIME",
    "EOF_ACTION",
    "FLAG_VALUE",
    "FORMAT_CONTROL_SEQUENCE",
    "IO_MODE",
    "WELL_FORMED_LIST",
    "NON_EMPTY_LIST",
    "NOT_LESS_THAN_ZERO",
    "OPERATOR_PRIORITY",
    "OPERATOR_SPECIFIER",
    "ORDER",
    "OS_FILE_PERMISSION",
    "OS_FILE_PROPERTY",
    "OS_PATH",
    "PREDICATE_PROPERTY",
    "FLAG",
    "READ_OPTION",
    "SELECTABLE_ITEM",
    "SOCKET_ADDRESS",
    "SOCKET_DOMAIN",
    "SOURCE_SINK",
    "STREAM",
    "STREAM_OPTION",
    "STREAM_OR_ALIAS",
    "STREAM_POSITION",
    "STREAM_PROPERTY",
    "STREAM_SEEK_METHOD",
    "STREAM_TYPE",
    "TERM_STREAM_OR_ALIAS",
    "VAR_BINDING_OPTION",
    "WRITE_OPTION",
    "CLAUSE",
    "RULE",
    "FACT",
    "DIRECTIVE",
]


def test_domain_is_the_expected_enum():
    assert Domain is DomainError.Expected
    assert {str(d.name()) for d in Domain.values()} == set(DOMAIN_NAMES)


@pytest.mark.parametrize("name", DOMAIN_NAMES)
def test_domain_values(name):
    expected = getattr(Domain, name)
    assert domain(name.lower()) == expected
    assert domain(name) == expected
    assert domain(atom(name.lower())) == expected
    assert str(expected) == name.lower()
    assert expected.domain == name.lower()
    assert expected.toTerm() == atom(name.lower())


@pytest.mark.parametrize("name", DOMAIN_NAMES)
def test_domain_constants(name):
    assert getattr(module, f"DOMAIN_{name}") == getattr(Domain, name)


def test_domain_from_non_atom_term_is_none():
    assert domain(struct("order", atom("x"))) is None
    assert domain(integer(1)) is None


def test_domain_of_unknown_name_raises():
    with pytest.raises(Exception, match="No enum constant"):
        domain("not_a_domain")


def assert_domain_error(error, expected, culprit, message):
    assert isinstance(error, DomainError)
    assert isinstance(error, LogicError)
    assert isinstance(error, Exception)
    assert error.expected_domain == expected
    assert error.culprit == culprit
    assert error.message == message
    assert error.extra_data == atom(message)
    assert error.getType() == struct("domain_error", expected.toTerm(), culprit)
    assert error.error_struct == struct("error", error.getType(), atom(message))
    assert str(error) == str(error.error_struct)


def test_domain_error_for_term(context):
    error = domain_error_for_term(context, Domain.ORDER, atom("x"))
    assert_domain_error(error, Domain.ORDER, atom("x"), "Term `x` is not a valid order")
    assert error.context == context


def test_domain_error_for_goal(context, procedure):
    error = domain_error_for_goal(context, procedure, Domain.CLAUSE, integer(1))
    assert_domain_error(error, Domain.CLAUSE, integer(1), "Subgoal `1` of foo/2 is not clause term")


def test_domain_error_for_flag_values_without_index(context, procedure):
    error = domain_error_for_flag_values(
        context, procedure, [atom("on"), atom("off")], atom("maybe")
    )
    assert error.expected_domain == Domain.FLAG_VALUE
    assert error.culprit == atom("maybe")
    assert "should be one of {`on`, `off`} but `maybe` has been provided instead" in error.message
    assert error.getType() == struct("domain_error", atom("flag_value"), atom("maybe"))


def test_domain_error_for_argument_without_index(context, procedure):
    error = domain_error_for_argument(context, procedure, Domain.ORDER, atom("x"))
    assert error.expected_domain == Domain.ORDER
    assert "should be `order`, but `x` has been provided instead" in error.message


def test_domain_error_for_flag_values_with_index(context, procedure):
    error = domain_error_for_flag_values(
        context, procedure, [atom("on"), atom("off")], atom("maybe"), 1
    )
    assert error.expected_domain == Domain.FLAG_VALUE
    assert str(error.message).startswith("The 1-th argument")
    assert error.getType() == struct("domain_error", atom("flag_value"), atom("maybe"))


def test_domain_error_for_argument_with_index(context, procedure):
    error = domain_error_for_argument(context, procedure, Domain.ORDER, atom("x"), 0)
    assert error.expected_domain == Domain.ORDER
    assert str(error.message).startswith("The 0-th argument")
    assert error.getType() == struct("domain_error", atom("order"), atom("x"))


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt DomainError.forArgument/forFlagValues messages lack a space: 'An argumentof'",
)
def test_domain_error_for_argument_message_is_well_spaced(context, procedure):
    error = domain_error_for_argument(context, procedure, Domain.ORDER, atom("x"))
    assert error.message.startswith("An argument of `foo/2`")


def test_domain_error_contexts(context):
    error = domain_error_for_term(context, Domain.ORDER, atom("x"))
    assert list(error.contexts) == [context]
    pushed = error.push_context(context)
    assert isinstance(pushed, DomainError)
    assert len(pushed.contexts) == 2
    assert pushed.error_struct == error.error_struct
    assert isinstance(error.update_context(context), DomainError)
    assert isinstance(error.update_last_context(context), DomainError)


def test_domain_error_type_property_is_the_overridden_one(context):
    error = domain_error_for_term(context, Domain.ORDER, atom("x"))
    assert error.type == error.getType()
