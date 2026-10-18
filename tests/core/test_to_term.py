"""Conversion of Python values into terms at the API boundary, and back (`to_python`)."""

from decimal import Decimal

import pytest

from tuprolog.core import (
    FALSE,
    TRUE,
    atom,
    integer,
    logic_list,
    logic_list_from,
    logic_tuple,
    real,
    struct,
    to_python,
    to_term,
    var,
)
from tuprolog.core.parsing import parse_term


@pytest.mark.parametrize(
    "value, expected",
    [
        ("abc", atom("abc")),
        (True, TRUE),
        (False, FALSE),
        (42, integer(42)),
        (2**80, integer(2**80)),
        (1.5, real("1.5")),
        (Decimal("2.25"), real("2.25")),
        ([1, "a", [True]], logic_list(integer(1), atom("a"), logic_list(TRUE))),
        ([], logic_list()),
        (("a", 1, 2.5), logic_tuple(atom("a"), integer(1), real("2.5"))),
        (("a",), atom("a")),
    ],
    ids=[
        "str",
        "true",
        "false",
        "int",
        "big_int",
        "float",
        "decimal",
        "list",
        "empty",
        "tuple",
        "1-tuple",
    ],
)
def test_to_term(value, expected):
    assert to_term(value) == expected


def test_to_term_keeps_terms():
    x = var("X")
    assert to_term(x) is x


@pytest.mark.parametrize("value", [object(), None, (), {"a": 1}])
def test_to_term_rejects_other_values(value):
    with pytest.raises(TypeError, match="Cannot convert"):
        to_term(value)


def test_factories_convert_python_values():
    assert struct("f", "a", 1) == struct("f", atom("a"), integer(1))
    assert logic_list("a", 1) == logic_list(atom("a"), integer(1))
    assert logic_list_from(["a"], "b") == logic_list_from([atom("a")], atom("b"))
    assert logic_tuple("a", 1, True) == logic_tuple(atom("a"), integer(1), TRUE)


def test_a_logic_list_is_a_single_argument():
    items = logic_list(atom("a"), atom("b"))
    assert struct("f", items).arity == 1
    assert list(items) == [atom("a"), atom("b")]


@pytest.mark.parametrize(
    "text, expected",
    [
        ("abc", "abc"),
        ("'hello world'", "hello world"),
        ('"text"', "text"),
        ("true", True),
        ("false", False),
        ("fail", False),
        ("42", 42),
        ("123456789012345678901234567890", 123456789012345678901234567890),
        ("-1.5", -1.5),
        ("[]", []),
        ("[1, [a, 2.5], (x, y)]", [1, ["a", 2.5], ("x", "y")]),
        ("(a, b, c)", ("a", "b", "c")),
    ],
)
def test_to_python(text, expected):
    value = to_python(parse_term(text))
    assert value == expected
    assert type(value) is type(expected)


@pytest.mark.parametrize("text", ["X", "f(a)", "[a | T]", "'$VAR'(1)"])
def test_to_python_keeps_other_terms(text):
    term = parse_term(text)
    assert to_python(term) is term or to_python(term) == term


def test_to_python_inside_lists_keeps_other_terms():
    assert to_python(parse_term("[f(a)]")) == [struct("f", atom("a"))]


@pytest.mark.parametrize("value", [1, "a", True, 2.5, [1, ["a"]], ("a", [1, (2, 3)]), []])
def test_to_python_inverts_to_term(value):
    assert to_python(to_term(value)) == value


def test_trailing_nested_tuples_flatten():
    # (a, (b, c)) is (a, b, c) in Prolog, as ','/2 is right-associative
    assert to_python(to_term(("a", ("b", "c")))) == ("a", "b", "c")
