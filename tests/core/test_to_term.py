"""Conversion of Python values into terms at the API boundary."""

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
    to_term,
    var,
)


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
    ],
    ids=["str", "true", "false", "int", "big_int", "float", "decimal"],
)
def test_to_term(value, expected):
    assert to_term(value) == expected


def test_to_term_keeps_terms():
    x = var("X")
    assert to_term(x) is x


def test_to_term_rejects_other_values():
    with pytest.raises(TypeError, match="Cannot convert"):
        to_term(object())


def test_factories_convert_python_values():
    assert struct("f", "a", 1) == struct("f", atom("a"), integer(1))
    assert logic_list("a", 1) == logic_list(atom("a"), integer(1))
    assert logic_list_from(["a"], "b") == logic_list_from([atom("a")], atom("b"))
    assert logic_tuple("a", 1, True) == logic_tuple(atom("a"), integer(1), TRUE)


def test_a_logic_list_is_a_single_argument():
    items = logic_list(atom("a"), atom("b"))
    assert struct("f", items).arity == 1
    assert list(items) == [atom("a"), atom("b")]
