"""Tests for `tuprolog.core.parsing` (API, definitions and TermParser/TermReader adapters)."""

import jpype
import pytest

from tuprolog.core import (
    Atom,
    Clause,
    Integer,
    Real,
    Rule,
    Var,
    atom,
    integer,
    logic_list,
    real,
    rule,
    struct,
)
from tuprolog.core.operators import DEFAULT_OPERATORS, XFX, operator, operator_set
from tuprolog.core.parsing import (
    DEFAULT_TERM_PARSER,
    DEFAULT_TERM_READER,
    InvalidTermTypeException,
    ParseException,
    TermParser,
    TermReader,
    parse_atom,
    parse_clause,
    parse_constant,
    parse_integer,
    parse_numeric,
    parse_real,
    parse_struct,
    parse_term,
    parse_var,
    parser_factory,
    read_term,
    read_terms,
    term_parser,
    term_reader,
)
from tuprolog.jvmioutils import open_file

ByteArrayInputStream = jpype.JClass("java.io.ByteArrayInputStream")


@pytest.fixture
def custom_ops():
    return operator_set(operator("++", XFX, 500))


@pytest.fixture
def theory_file(tmp_path):
    path = tmp_path / "theory.pl"
    path.write_text("f(a).\ng(X) :- f(X).\nh.\n")
    return path


def test_definitions_are_jvm_types():
    package = "it.unibo.tuprolog.core.parsing."
    assert TermParser == jpype.JClass(package + "TermParser")
    assert TermReader == jpype.JClass(package + "TermReader")
    assert ParseException == jpype.JClass(package + "ParseException")
    assert InvalidTermTypeException == jpype.JClass(package + "InvalidTermTypeException")
    assert issubclass(InvalidTermTypeException, ParseException)
    assert isinstance(DEFAULT_TERM_PARSER, TermParser)
    assert isinstance(DEFAULT_TERM_READER, TermReader)


# --- parse_* functions ----------------------------------------------------------------------------


def test_parse_term():
    term = parse_term("f(X, a, [1, 2.5])")
    assert term.functor == "f"
    assert term[0].is_var
    assert term[1] == atom("a")
    assert term[2] == logic_list(integer(1), real(2.5))


def test_parse_term_with_full_stop():
    assert parse_term("f(a).") == struct("f", atom("a"))


def test_parse_term_shares_variables_by_name():
    term = parse_term("f(X, X, Y)")
    assert term[0] == term[1]
    assert term[0] != term[2]


def test_parse_term_with_default_operators():
    assert parse_term("a + b * c") == struct("+", atom("a"), struct("*", atom("b"), atom("c")))


def test_parse_term_with_custom_operators(custom_ops):
    assert parse_term("a ++ b", custom_ops) == struct("++", atom("a"), atom("b"))


def test_parse_term_with_unknown_operator():
    with pytest.raises(ParseException):
        parse_term("a ++ b")


@pytest.mark.parametrize("text", ["f((", "", "f(a,)", "[a|]"])
def test_parse_term_syntax_errors(text):
    with pytest.raises(ParseException):
        parse_term(text)


def test_parse_exception_details():
    with pytest.raises(ParseException) as info:
        parse_term("f((")
    assert info.value.line == 1
    assert info.value.column > 0


def test_parse_struct():
    assert parse_struct("f(a)") == struct("f", atom("a"))
    assert parse_struct("a") == atom("a")


def test_parse_struct_rejects_other_terms():
    with pytest.raises(InvalidTermTypeException):
        parse_struct("X")


def test_parse_constant():
    assert parse_constant("1") == integer(1)
    assert parse_constant("a") == atom("a")
    with pytest.raises(InvalidTermTypeException):
        parse_constant("f(a)")


def test_parse_var():
    term = parse_var("X")
    assert isinstance(term, Var)
    assert term.name == "X"
    with pytest.raises(InvalidTermTypeException):
        parse_var("a")


def test_parse_atom():
    assert isinstance(parse_atom("a"), Atom)
    assert parse_atom("'hello world'") == atom("hello world")
    with pytest.raises(InvalidTermTypeException):
        parse_atom("1")


def test_parse_numeric():
    assert isinstance(parse_numeric("1"), Integer)
    assert isinstance(parse_numeric("1.5"), Real)
    with pytest.raises(InvalidTermTypeException):
        parse_numeric("a")


@pytest.mark.parametrize("text, value", [("15", 15), ("-15", -15), (str(2**80), 2**80)])
def test_parse_integer(text, value):
    assert parse_integer(text) == integer(value)


def test_parse_integer_rejects_reals():
    with pytest.raises(InvalidTermTypeException):
        parse_integer("1.5")


def test_parse_real():
    assert parse_real("1.5") == real("1.5")
    with pytest.raises(InvalidTermTypeException):
        parse_real("1")


def test_parse_clause():
    term = parse_clause("p(X) :- q(X), r")
    assert isinstance(term, Rule)
    assert term.head.functor == "p"
    assert term.body_size == 2


def test_parse_clause_rejects_non_clauses():
    with pytest.raises(InvalidTermTypeException):
        parse_clause("p(X)")


def test_parse_clause_with_custom_operators(custom_ops):
    term = parse_clause("p :- a ++ b", DEFAULT_OPERATORS + custom_ops)
    assert isinstance(term, Clause)
    assert term == rule(atom("p"), struct("++", atom("a"), atom("b")))


@pytest.mark.parametrize(
    "function",
    [
        parse_term,
        parse_struct,
        parse_constant,
        parse_var,
        parse_atom,
        parse_numeric,
        parse_integer,
        parse_real,
        parse_clause,
    ],
)
def test_parse_functions_accept_explicit_none_operators(function):
    with pytest.raises(ParseException):
        function("((", None)


# --- term_parser / parser_factory -----------------------------------------------------------------


def test_term_parser_default():
    parser = term_parser()
    assert isinstance(parser, TermParser)
    assert parser.default_operator_set == DEFAULT_OPERATORS
    assert parser.parse("a + b") == struct("+", atom("a"), atom("b"))


def test_term_parser_without_operators():
    parser = term_parser(with_default_operators=False)
    assert len(parser.default_operator_set) == 0
    assert parser.parse("+(a, b)") == struct("+", atom("a"), atom("b"))
    with pytest.raises(ParseException):
        parser.parse("a + b")


def test_term_parser_with_additional_operators(custom_ops):
    parser = term_parser(operators=custom_ops)
    assert parser.default_operator_set == DEFAULT_OPERATORS + custom_ops
    assert parser.parse("a ++ b") == struct("++", atom("a"), atom("b"))
    assert parser.parse("a + b") == struct("+", atom("a"), atom("b"))


def test_term_parser_with_only_custom_operators(custom_ops):
    parser = term_parser(False, custom_ops)
    assert parser.default_operator_set == custom_ops
    assert parser.parse("a ++ b") == struct("++", atom("a"), atom("b"))
    with pytest.raises(ParseException):
        parser.parse("a + b")


def test_term_parser_adapter_methods(custom_ops):
    parser = term_parser()
    assert parser.parse_term("f(a)") == struct("f", atom("a"))
    assert parser.parse_term("a ++ b", custom_ops) == struct("++", atom("a"), atom("b"))
    assert parser.parse_struct("f(a)") == struct("f", atom("a"))
    assert parser.parse_constant("a") == atom("a")
    assert parser.parse_var("X").name == "X"
    assert parser.parse_atom("a") == atom("a")
    assert parser.parse_numeric("1") == integer(1)
    assert parser.parse_integer("1") == integer(1)
    assert parser.parse_real("1.5") == real("1.5")
    assert parser.parse_clause("a :- b") == rule(atom("a"), atom("b"))


def test_parser_factory_works_for_readers(custom_ops):
    reader = parser_factory(TermReader, False, custom_ops)
    assert isinstance(reader, TermReader)
    assert reader.default_operator_set == custom_ops


# --- term_reader / read_term(s) -------------------------------------------------------------------


def test_term_reader_default():
    reader = term_reader()
    assert isinstance(reader, TermReader)
    assert reader.default_operator_set == DEFAULT_OPERATORS


def test_term_reader_without_operators():
    assert len(term_reader(False).default_operator_set) == 0


def test_term_reader_with_operators(custom_ops):
    assert term_reader(operators=custom_ops).default_operator_set == (
        DEFAULT_OPERATORS + custom_ops
    )


def test_read_term_from_path(theory_file):
    assert read_term(str(theory_file)) == struct("f", atom("a"))


def test_read_term_from_input_stream(theory_file):
    assert read_term(open_file(str(theory_file))) == struct("f", atom("a"))


def test_read_term_with_operators(tmp_path, custom_ops):
    path = tmp_path / "ops.pl"
    path.write_text("a ++ b.")
    assert read_term(str(path), custom_ops) == struct("++", atom("a"), atom("b"))


def test_read_term_from_missing_file(tmp_path):
    with pytest.raises(Exception, match="NoSuchFileException"):
        read_term(str(tmp_path / "missing.pl"))


def test_read_term_rejects_invalid_input():
    with pytest.raises(TypeError):
        read_term(42)


def test_term_reader_adapter_methods(theory_file):
    reader = term_reader()
    assert reader.read(str(theory_file)) == struct("f", atom("a"))
    assert reader.read_term(str(theory_file)) == struct("f", atom("a"))


def test_read_terms_single_unterminated_term():
    stream = ByteArrayInputStream(b"f(a)")
    assert list(read_terms(stream)) == [struct("f", atom("a"))]


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt 0.31.16's TermReader.readTerms fails on '.'-terminated terms "
    "('extraneous input .'); fixed upstream",
)
def test_read_terms_from_path(theory_file):
    terms = list(read_terms(str(theory_file)))
    assert len(terms) == 3
    assert terms[0] == struct("f", atom("a"))
    assert terms[2] == atom("h")


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt 0.31.16's TermReader.readTerms fails on '.'-terminated terms "
    "('extraneous input .'); fixed upstream",
)
def test_term_reader_read_all(theory_file):
    assert len(list(term_reader().read_all(str(theory_file)))) == 3
