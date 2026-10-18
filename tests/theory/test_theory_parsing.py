import io
import re
from collections.abc import Iterable

import pytest
from jpype import JClass

from tuprolog.core import atom, directive, fact, indicator, rule, struct, var
from tuprolog.core.operators import DEFAULT_OPERATORS, operator, operator_set, specifier
from tuprolog.core.parsing import ParseException
from tuprolog.jvmutils import Sequence
from tuprolog.theory import Theory
from tuprolog.theory.parsing import (
    DEFAULT_CLAUSES_PARSER,
    DEFAULT_CLAUSES_READER,
    ClausesParser,
    ClausesReader,
    clauses_parser,
    clauses_reader,
    parse_clauses,
    parse_theory,
    read_clauses,
    read_theory,
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


def test_definitions():
    assert isinstance(DEFAULT_CLAUSES_PARSER, ClausesParser)
    assert isinstance(DEFAULT_CLAUSES_READER, ClausesReader)
    assert DEFAULT_CLAUSES_PARSER.default_operator_set == DEFAULT_OPERATORS
    assert DEFAULT_CLAUSES_READER.default_operator_set == DEFAULT_OPERATORS


def test_parse_theory():
    t = parse_theory(SOURCE)
    assert isinstance(t, Theory)
    assert strings(t) == expected_strings()


def test_parse_theory_variables_are_shared_within_clauses():
    (clause,) = parse_theory("q(X) :- p(X).")
    assert clause.head[0] == clause.body[0]


def test_parse_theory_empty_and_comments_only():
    assert len(parse_theory("")) == 0
    assert len(parse_theory("% nothing here\n")) == 0


def test_parse_clauses_is_lazy_by_default():
    clauses = parse_clauses(SOURCE)
    assert isinstance(clauses, Sequence)
    assert isinstance(clauses, Iterable)
    assert strings(clauses) == expected_strings()


def test_parse_clauses_eagerly():
    clauses = parse_clauses(SOURCE, lazy=False)
    assert isinstance(clauses, list)
    assert strings(clauses) == expected_strings()


def test_parse_errors():
    with pytest.raises(ParseException):
        parse_theory("p(a")
    with pytest.raises(ParseException):
        parse_clauses("p(a). p(b", lazy=False)


def test_lazy_parse_errors_are_deferred_to_iteration():
    clauses = parse_clauses("p(a). p(b")
    with pytest.raises(ParseException):
        list(clauses)


def test_parse_error_details():
    with pytest.raises(ParseException) as info:
        parse_theory("p(a).\nq(")
    assert info.value.line == 2


def test_parse_with_custom_operators():
    assert strings(parse_theory("john likes mary.", LIKES)) == ["likes(john, mary) :- true"]
    assert strings(parse_clauses("john likes mary.", LIKES)) == ["likes(john, mary) :- true"]
    assert strings(parse_clauses("john likes mary.", LIKES, lazy=False)) == [
        "likes(john, mary) :- true"
    ]


def test_custom_operators_replace_the_default_ones():
    # as in 2P-Kt, the operators passed to parse_* are the only ones in use
    with pytest.raises(ParseException):
        parse_theory("X likes Y :- X = Y.", LIKES)
    (clause,) = parse_theory("X likes Y :- X = Y.", DEFAULT_OPERATORS.plus(LIKES))
    assert clause.head.functor == "likes"
    assert clause.body.functor == "="


def test_parse_without_custom_operators_fails():
    with pytest.raises(ParseException):
        parse_theory("john likes mary.")


def test_op_directives_do_not_affect_parsing():
    # the parser does not execute directives: op/3 is retained as a clause
    clauses = parse_clauses(":- op(700, xfx, likes). a.", lazy=False)
    assert strings(clauses) == [":- op(700, xfx, likes)", "a :- true"]


def test_clauses_parser_factory_defaults():
    parser = clauses_parser()
    assert isinstance(parser, ClausesParser)
    assert parser.default_operator_set == DEFAULT_OPERATORS


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


def test_read_theory_from_path_string(source_file):
    t = read_theory(str(source_file))
    assert isinstance(t, Theory)
    assert strings(t) == expected_strings()


def test_read_clauses_from_path_string(source_file):
    lazy = read_clauses(str(source_file))
    assert isinstance(lazy, Sequence)
    assert strings(lazy) == expected_strings()
    eager = read_clauses(str(source_file), lazy=False)
    assert isinstance(eager, list)
    assert strings(eager) == expected_strings()


def test_read_from_java_input_stream():
    assert strings(read_theory(byte_stream(SOURCE))) == expected_strings()
    assert strings(read_clauses(byte_stream(SOURCE), lazy=False)) == expected_strings()


def test_read_with_custom_operators(tmp_path):
    path = tmp_path / "likes.pl"
    path.write_text("john likes mary.")
    assert strings(read_theory(str(path), LIKES)) == ["likes(john, mary) :- true"]
    assert strings(read_clauses(str(path), LIKES)) == ["likes(john, mary) :- true"]
    assert strings(read_theory(byte_stream("a likes b."), LIKES)) == ["likes(a, b) :- true"]


def test_read_missing_file(tmp_path):
    with pytest.raises(Exception, match="NoSuchFile"):
        read_theory(str(tmp_path / "missing.pl"))


def test_read_parse_error(tmp_path):
    path = tmp_path / "broken.pl"
    path.write_text("p(a")
    with pytest.raises(ParseException):
        read_theory(str(path))


def test_read_theory_from_pathlib_path(source_file):
    assert strings(read_theory(source_file)) == expected_strings()


PYTHON_STREAMS = {
    "text": lambda text: io.StringIO(text),
    "binary": lambda text: io.BytesIO(text.encode()),
}


@pytest.mark.parametrize("stream", PYTHON_STREAMS.values(), ids=PYTHON_STREAMS.keys())
def test_read_from_python_streams(stream):
    assert strings(read_theory(stream(SOURCE))) == expected_strings()
    assert strings(read_clauses(stream(SOURCE))) == expected_strings()
    assert strings(read_clauses(stream(SOURCE), lazy=False)) == expected_strings()
    assert strings(read_theory(stream("a likes b."), LIKES)) == ["likes(a, b) :- true"]


@pytest.mark.parametrize("stream", PYTHON_STREAMS.values(), ids=PYTHON_STREAMS.keys())
def test_read_non_ascii_from_python_streams(stream):
    assert strings(read_theory(stream("p('è€😀')."))) == ["p('è€😀') :- true"]


@pytest.mark.parametrize("mode", ["r", "rb"])
def test_read_from_python_files(source_file, mode):
    with open(source_file, mode) as file:
        assert strings(read_theory(file)) == expected_strings()
        assert not file.closed


def test_read_with_clauses_reader_from_python_streams():
    assert strings(DEFAULT_CLAUSES_READER.read_theory(io.StringIO(SOURCE))) == expected_strings()
    # Python text streams also convert implicitly to the JVM readers 2P-Kt methods expect
    assert strings(DEFAULT_CLAUSES_READER.readTheory(io.StringIO(SOURCE))) == expected_strings()
    assert (
        strings(DEFAULT_CLAUSES_READER.readTheory(io.BytesIO(SOURCE.encode())))
        == expected_strings()
    )


def test_read_theory_rejects_unsupported_inputs_with_a_clear_message():
    with pytest.raises(TypeError, match="Invalid type"):
        read_theory(42)  # type: ignore[arg-type]


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
