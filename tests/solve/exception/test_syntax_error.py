import pytest

from tuprolog.core import atom
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error.syntax import (
    SyntaxError,
    error_detector,
    syntax_error,
    syntax_error_while_parsing_clauses,
    syntax_error_while_parsing_term,
)


def assert_syntax_error(error, message):
    assert isinstance(error, SyntaxError)
    assert isinstance(error, LogicError)
    assert error.message == message
    assert error.extra_data == atom(message)
    assert error.getType() == atom("syntax_error")
    assert error.error_struct.functor == "error"
    assert error.error_struct[0] == atom("syntax_error")
    assert error.error_struct[1] == atom(message)


def test_syntax_error_is_the_logic_one():
    assert SyntaxError.class_.getName() == "it.unibo.tuprolog.solve.exception.error.SyntaxError"


def test_syntax_error(context):
    assert_syntax_error(syntax_error(context, "unexpected token"), "Syntax error: unexpected token")


def test_syntax_error_while_parsing_term(context):
    error = syntax_error_while_parsing_term(context, "f(", 1, 2, "missing )")
    assert_syntax_error(error, "Syntax error at 1:2 while parsing `f(`: missing )")


def test_syntax_error_while_parsing_clauses(context):
    error = syntax_error_while_parsing_clauses(context, "a.\nf(", 1, 2, 2, "missing )")
    assert_syntax_error(
        error,
        "Syntax error at 2:2 while parsing clause 1: missing )\n"
        "   1: ...\n"
        "   2: f(\n"
        "       ^ missing )",
    )


@pytest.mark.parametrize(
    "args, expected",
    [
        (("f(", 1, 2, "missing )"), "1: f(\n    ^ missing )"),
        (("f(", 1, 2), "1: f(\n    ^ "),
        (("a.\nf(", 2, 0, "here"), "1: ...\n2: f(\n  ^ here"),
        (("a.", 5, 0, "beyond"), "a."),
    ],
)
def test_error_detector(args, expected):
    assert error_detector(*args) == expected
