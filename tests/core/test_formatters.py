import unittest
from uuid import uuid4

import pytest

from tuprolog.core import (
    DEFAULT_TAGS_FORMATTING_OPTIONS,
    Atom,
    Integer,
    TagsFormattingOptions,
    TermFormatter,
    Var,
    canonical_formatter,
    default_formatter,
    integer,
    pretty_expressions_formatter,
    pretty_variables_formatter,
    readable_formatter,
    struct,
)
from tuprolog.core.impl import DefaultTermFormatter
from tuprolog.core.operators import EMPTY_OPERATORS


class TestFormatters(unittest.TestCase):
    def test_term_formatter(self):
        formatter = DefaultTermFormatter()
        for term in [Atom.of("a"), Integer.of(1), Var.of("X")]:
            self.assertEqual(formatter.format(term), str(term))


X, Y = Var.of("X"), Var.of("_Y")
EXPRESSION = struct("+", X, struct("*", integer(1), Y))


@pytest.mark.parametrize(
    "formatter, expected",
    [
        (pretty_expressions_formatter(), "X + 1 * _Y"),
        (pretty_expressions_formatter(operators=EMPTY_OPERATORS), "'+'(X, '*'(1, _Y))"),
        (pretty_variables_formatter(), "'+'(X, '*'(1, _Y))"),
        (readable_formatter(), "X + 1 * _Y"),
    ],
    ids=["pretty_expressions", "pretty_expressions_no_ops", "pretty_variables", "readable"],
)
def test_formatter_factories(formatter, expected):
    assert isinstance(formatter, TermFormatter)
    assert formatter.format(EXPRESSION) == expected


def test_pretty_expressions_formatter_without_pretty_variables():
    formatted = str(pretty_expressions_formatter(pretty_variables=False).format(EXPRESSION))
    assert formatted.startswith("X_") and " + 1 * _Y_" in formatted


def test_default_formatter_uses_the_given_operators():
    assert " + 1 * " in default_formatter().format(EXPRESSION)
    assert str(default_formatter(EMPTY_OPERATORS).format(EXPRESSION)).startswith("+(")


def test_formatter_factories_accept_tags_options():
    tags = TagsFormattingOptions()
    assert tags == DEFAULT_TAGS_FORMATTING_OPTIONS
    assert pretty_expressions_formatter(tags=tags).format(EXPRESSION) == "X + 1 * _Y"


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt 3.0.1's TermFormatter.canonical() prints variables as '_' + their per-name "
    "counter, so variables with different names and equal counters collide (f(X_0, Y_0) -> f(_0, _0))",
)
def test_canonical_formatter_keeps_distinct_variables_apart():
    # fresh names, so that both variables get the same per-name counter (0)
    x, y = Var.of(f"X{uuid4().hex}"), Var.of(f"Y{uuid4().hex}")
    formatted = str(canonical_formatter().format(struct("f", x, y, x)))
    first, second, third = formatted[2:-1].split(", ")
    assert first == third != second
