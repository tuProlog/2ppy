import logging
import jpype
import jpype.imports

from it.unibo.tuprolog.core.parsing import TermParser
from it.unibo.tuprolog.core.parsing import TermReader
from it.unibo.tuprolog.core.parsing import ParseException
from it.unibo.tuprolog.core.parsing import InvalidTermTypeException

from tuprolog.core import Term
from tuprolog.core import Struct
from tuprolog.core import Constant
from tuprolog.core import Var
from tuprolog.core import Atom
from tuprolog.core import Numeric
from tuprolog.core import Integer
from tuprolog.core import Real
from tuprolog.core import Clause
from tuprolog.jvmutils import open_file, InputStream

from tuprolog.core.operators import Operator, OperatorSet, DEFAULT_OPERATORS, EMPTY_OPERATORS

from collections.abc import Iterable
from typing import Union


logging.debug("Loaded JVM classes from it.unibo.tuprolog.core.parsing.*")


def term_parser(with_default_operators: bool=True, operators: OperatorSet=None) -> TermParser:
    if operators is None:
        if with_default_operators:
            return TermParser.getWithDefaultOperators()
        else:
            return TermParser.getWithNoOperator()
    else:
        if with_default_operators:
            return TermParser.withOperators(DEFAULT_OPERATORS.plus(operators))
        else:
            return TermParser.withOperators(operators)


def term_reader(with_default_operators: bool=True, operators: OperatorSet=None) -> TermParser:
    if operators is None:
        if with_default_operators:
            return TermReader.getWithDefaultOperators()
        else:
            return TermReader.getWithNoOperator()
    else:
        if with_default_operators:
            return TermReader.withOperators(DEFAULT_OPERATORS.plus(operators))
        else:
            return TermReader.withOperators(operators)


DEFAULT_TERM_PARSER = term_parser()


DEFAULT_TERM_READER = term_reader()


def parse_term(string: str, operators: OperatorSet=None) -> Term:
    if operators is None:
        return DEFAULT_TERM_PARSER.parseTerm(string)
    else:
        return DEFAULT_TERM_PARSER.parseTerm(string, operators)


def parse_struct(string: str, operators: OperatorSet=None) -> Struct:
    if operators is None:
        return DEFAULT_TERM_PARSER.parseStruct(string)
    else:
        return DEFAULT_TERM_PARSER.parseStruct(string, operators)


def parse_constant(string: str, operators: OperatorSet=None) -> Constant:
    if operators is None:
        return DEFAULT_TERM_PARSER.parseConstant(string)
    else:
        return DEFAULT_TERM_PARSER.parseConstant(string, operators)


def parse_var(string: str, operators: OperatorSet=None) -> Var:
    if operators is None:
        return DEFAULT_TERM_PARSER.parseVar(string)
    else:
        return DEFAULT_TERM_PARSER.parseVar(string, operators)


def parse_atom(string: str, operators: OperatorSet=None) -> Atom:
    if operators is None:
        return DEFAULT_TERM_PARSER.parseAtom(string)
    else:
        return DEFAULT_TERM_PARSER.parseAtom(string, operators)


def parse_numeric(string: str, operators: OperatorSet=None) -> Numeric:
    if operators is None:
        return DEFAULT_TERM_PARSER.parseNumeric(string)
    else:
        return DEFAULT_TERM_PARSER.parseNumeric(string, operators)


def parse_integer(string: str, operators: OperatorSet=None) -> Integer:
    if operators is None:
        return DEFAULT_TERM_PARSER.parseInteger(string)
    else:
        return DEFAULT_TERM_PARSER.parseInteger(string, operators)


def parse_real(string: str, operators: OperatorSet=None) -> Real:
    if operators is None:
        return DEFAULT_TERM_PARSER.parseReal(string)
    else:
        return DEFAULT_TERM_PARSER.parseReal(string, operators)


def parse_clause(string: str, operators: OperatorSet=None) -> Clause:
    if operators is None:
        return DEFAULT_TERM_PARSER.parseClause(string)
    else:
        return DEFAULT_TERM_PARSER.parseClause(string, operators)


def read_term(input: Union[InputStream, str], operators: OperatorSet=None) -> Term:
    input = ensure_input_steam(input)
    if operators is None:
        return DEFAULT_TERM_READER.readTerm(input)
    else:
        return DEFAULT_TERM_READER.readTerm(input, operators)


def read_terms(input: Union[InputStream, str], operators: OperatorSet=None) -> Iterable[Term]:
    input = ensure_input_steam(input)
    if operators is None:
        return DEFAULT_TERM_READER.readTerms(input)
    else:
        return DEFAULT_TERM_READER.readTerms(input, operators)
