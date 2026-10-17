from typing import Union, Iterable
from tuprolog.core import Clause
from tuprolog.core.parsing import parser_factory
from tuprolog.theory import Theory
from tuprolog.jvmioutils import InputStream
from tuprolog.core.operators import OperatorSet
from ._definitions import ClausesParser, ClausesReader, DEFAULT_CLAUSES_PARSER, DEFAULT_CLAUSES_READER


def clauses_parser(with_default_operators: bool = True, operators: OperatorSet = None) -> ClausesParser:
    return parser_factory(ClausesParser, with_default_operators, operators)


def clauses_reader(with_default_operators: bool = True, operators: OperatorSet = None) -> ClausesReader:
    return parser_factory(ClausesReader, with_default_operators, operators)


def parse_theory(string: str, operators: OperatorSet = None) -> Theory:
    return DEFAULT_CLAUSES_PARSER.parse_theory(string, operators)


def parse_clauses(string: str, operators: OperatorSet = None, lazy: bool = True) -> Iterable[Clause]:
    if lazy:
        return DEFAULT_CLAUSES_PARSER.parse_clauses_lazily(string, operators)
    else:
        return DEFAULT_CLAUSES_PARSER.parse_clauses(string, operators)


def read_theory(input: Union[InputStream, str], operators: OperatorSet = None) -> Theory:
    return DEFAULT_CLAUSES_READER.read_theory(input, operators)


def read_clauses(input: Union[InputStream, str], operators: OperatorSet = None, lazy: bool = True) -> Iterable[Clause]:
    if lazy:
        return DEFAULT_CLAUSES_READER.read_clauses_lazily(input, operators)
    else:
        return DEFAULT_CLAUSES_READER.read_clauses(input, operators)
