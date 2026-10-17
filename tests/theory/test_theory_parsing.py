import re

import pytest
from jpype import JClass

from tuprolog.core import atom, directive, fact, indicator, rule, struct, var
from tuprolog.core.operators import DEFAULT_OPERATORS, operator, operator_set, specifier
from tuprolog.core.parsing import ParseException
from tuprolog.jvmutils import Sequence
from tuprolog.theory.parsing import (
    ClausesReader,
    clauses_parser,
    clauses_reader,
)

SOURCE = """
% a comment
p(a). p(b).
q(X) :- p(X).
:- dynamic(r/1).
"""


EXPECTED = [
    fact(struct("p", atom("a"))),
    fact(struct("p", atom("b"))),
    rule(struct("q", var("X")), struct("p", var("X"))),
    directive(struct("dynamic", indicator("r", 1))),
]


LIKES = operator_set(operator("likes", specifier("xfx"), 700))


def strings(clauses):
    # variables' complete names carry unique, run-dependent suffixes (e.g. X_42)
    return [re.sub(r"\b([A-Z_]\w*?)_\d+\b", r"\1", str(c)) for c in clauses]


def expected_strings():
    return strings(EXPECTED)


@pytest.fixture
def source_file(tmp_path):
    path = tmp_path / "theory.pl"
    path.write_text(SOURCE)
    return path


def byte_stream(text):
    return JClass("java.io.ByteArrayInputStream")(text.encode())


def test_clauses_parser_without_default_operators():
    parser = clauses_parser(with_default_operators=False)
    assert parser.default_operator_set.size() == 0
    with pytest.raises(ParseException):
        parser.parse_theory("a :- b.")
    assert strings(parser.parse_theory("':-'(a, b).")) == ["a :- b"]


def test_clauses_parser_with_extra_operators():
    parser = clauses_parser(operators=LIKES)
    assert parser.default_operator_set == DEFAULT_OPERATORS.plus(LIKES)
    assert strings(parser.parse_theory("a likes b :- c, d.")) == ["likes(a, b) :- (c, d)"]


def test_clauses_parser_with_only_custom_operators():
    parser = clauses_parser(False, LIKES)
    assert parser.default_operator_set == LIKES
    assert strings(parser.parse_theory("a likes b.")) == ["likes(a, b) :- true"]


def test_clauses_parser_methods():
    parser = clauses_parser()
    assert strings(parser.parse_theory(SOURCE)) == expected_strings()
    assert strings(parser.parse_theory("a likes b.", LIKES)) == ["likes(a, b) :- true"]
    lazy = parser.parse_clauses_lazily(SOURCE)
    assert isinstance(lazy, Sequence)
    assert strings(lazy) == expected_strings()
    eager = parser.parse_clauses(SOURCE)
    assert isinstance(eager, list)
    assert strings(eager) == expected_strings()
    assert strings(parser.parse_clauses("a likes b.", LIKES)) == ["likes(a, b) :- true"]


def test_clauses_reader_factory(source_file):
    reader = clauses_reader()
    assert isinstance(reader, ClausesReader)
    assert reader.default_operator_set == DEFAULT_OPERATORS
    assert strings(reader.read_theory(str(source_file))) == expected_strings()
    assert strings(reader.read_clauses(str(source_file))) == expected_strings()
    assert isinstance(reader.read_clauses(str(source_file)), list)
    assert isinstance(reader.read_clauses_lazily(str(source_file)), Sequence)


def test_clauses_reader_without_default_operators():
    reader = clauses_reader(False)
    assert reader.default_operator_set.size() == 0
    with pytest.raises(ParseException):
        reader.read_theory(byte_stream("a :- b."))


def test_clauses_reader_with_operators():
    reader = clauses_reader(operators=LIKES)
    assert strings(reader.read_theory(byte_stream("a likes b."))) == ["likes(a, b) :- true"]
    reader = clauses_reader(False, LIKES)
    assert reader.default_operator_set == LIKES
