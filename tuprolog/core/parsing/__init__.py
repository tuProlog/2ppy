from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.core.parsing as _parsing
from tuprolog.core import Term, Struct, Constant, Var, Atom, Numeric, Integer, Real, Clause
from tuprolog.jvmutils import InputStream
from tuprolog.core.operators import OperatorSet, DEFAULT_OPERATORS
from typing import Union, Iterable
from ._ktadapt import *

TermParser = _parsing.TermParser

TermReader = _parsing.TermReader

ParseException = _parsing.ParseException

InvalidTermTypeException = _parsing.InvalidTermTypeException


def _factory(source, with_default_operators: bool = True, operators: OperatorSet = None):
    if operators is None:
        if with_default_operators:
            return source.withDefaultOperators()
        else:
            return source.withNoOperator()
    else:
        if with_default_operators:
            return source.withOperators(DEFAULT_OPERATORS.plus(operators))
        else:
            return source.withOperators(operators)


def term_parser(with_default_operators: bool = True, operators: OperatorSet = None) -> TermParser:
    return _factory(TermParser, with_default_operators, operators)


def term_reader(with_default_operators: bool = True, operators: OperatorSet = None) -> TermParser:
    return _factory(TermReader, with_default_operators, operators)


DEFAULT_TERM_PARSER = term_parser()

DEFAULT_TERM_READER = term_reader()


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


def read_term(input: Union[InputStream, str], operators: OperatorSet = None) -> Term:
    return DEFAULT_TERM_READER.read_term(input, operators)


def read_terms(input: Union[InputStream, str], operators: OperatorSet = None) -> Iterable[Term]:
    return DEFAULT_TERM_READER.read_terms(input, operators)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.parsing.*")
