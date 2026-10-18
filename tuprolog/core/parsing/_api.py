from collections.abc import Iterable
from typing import Any

from tuprolog.core import Atom, Clause, Constant, Integer, Numeric, Real, Struct, Term, Var
from tuprolog.core.operators import DEFAULT_OPERATORS, OperatorSet
from tuprolog.jvmioutils import InputStream

from ._definitions import DEFAULT_TERM_PARSER, DEFAULT_TERM_READER, TermParser, TermReader

__all__ = [
    "parse_atom",
    "parse_clause",
    "parse_constant",
    "parse_integer",
    "parse_numeric",
    "parse_real",
    "parse_struct",
    "parse_term",
    "parse_var",
    "parser_factory",
    "read_term",
    "read_terms",
    "term_parser",
    "term_reader",
]


def parser_factory(
    source: Any, with_default_operators: bool = True, operators: OperatorSet | None = None
) -> Any:
    if operators is None:
        if with_default_operators:
            return source.withDefaultOperators()
        else:
            return source.withNoOperator()
    else:
        if with_default_operators:
            return source.withOperators(DEFAULT_OPERATORS.plus(operators))  # type: ignore[attr-defined]
        else:
            return source.withOperators(operators)


def term_parser(with_default_operators: bool = True, operators: OperatorSet = None) -> TermParser:
    return parser_factory(TermParser, with_default_operators, operators)


def term_reader(with_default_operators: bool = True, operators: OperatorSet = None) -> TermParser:
    return parser_factory(TermReader, with_default_operators, operators)


def parse_term(string: str, operators: OperatorSet = None) -> Term:
    return DEFAULT_TERM_PARSER.parse_term(string, operators)


def parse_struct(string: str, operators: OperatorSet = None) -> Struct:
    return DEFAULT_TERM_PARSER.parse_struct(string, operators)


def parse_constant(string: str, operators: OperatorSet = None) -> Constant:
    return DEFAULT_TERM_PARSER.parse_constant(string, operators)


def parse_var(string: str, operators: OperatorSet = None) -> Var:
    return DEFAULT_TERM_PARSER.parse_var(string, operators)


def parse_atom(string: str, operators: OperatorSet = None) -> Atom:
    return DEFAULT_TERM_PARSER.parse_atom(string, operators)


def parse_numeric(string: str, operators: OperatorSet = None) -> Numeric:
    return DEFAULT_TERM_PARSER.parse_numeric(string, operators)


def parse_integer(string: str, operators: OperatorSet = None) -> Integer:
    return DEFAULT_TERM_PARSER.parse_integer(string, operators)


def parse_real(string: str, operators: OperatorSet = None) -> Real:
    return DEFAULT_TERM_PARSER.parse_real(string, operators)


def parse_clause(string: str, operators: OperatorSet = None) -> Clause:
    return DEFAULT_TERM_PARSER.parse_clause(string, operators)


def read_term(input: InputStream | str, operators: OperatorSet = None) -> Term:
    return DEFAULT_TERM_READER.read_term(input, operators)


def read_terms(input: InputStream | str, operators: OperatorSet = None) -> Iterable[Term]:
    return DEFAULT_TERM_READER.read_terms(input, operators)
