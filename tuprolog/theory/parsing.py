from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.theory.parsing as _parsing
from tuprolog.core import Clause
from tuprolog.theory import Theory
from tuprolog.jvmutils import InputStream, ensure_input_steam
from tuprolog.core.operators import OperatorSet, DEFAULT_OPERATORS
from typing import Union, Iterable


ClausesParser = _parsing.ClausesParser

ClausesReader = _parsing.ClausesReader


def clauses_parser(with_default_operators: bool = True, operators: OperatorSet = None) -> ClausesParser:
    if operators is None:
        if with_default_operators:
            return ClausesParser.getWithDefaultOperators()
        else:
            return ClausesParser.getWithNoOperator()
    else:
        if with_default_operators:
            return ClausesParser.withOperators(DEFAULT_OPERATORS.plus(operators))
        else:
            return ClausesParser.withOperators(operators)


def clauses_reader(with_default_operators: bool = True, operators: OperatorSet = None) -> ClausesReader:
    if operators is None:
        if with_default_operators:
            return ClausesReader.getWithDefaultOperators()
        else:
            return ClausesReader.getWithNoOperator()
    else:
        if with_default_operators:
            return ClausesReader.withOperators(DEFAULT_OPERATORS.plus(operators))
        else:
            return ClausesReader.withOperators(operators)


DEFAULT_CLAUSES_PARSER = clauses_parser()

DEFAULT_CLAUSES_READER = clauses_reader()


def parse_theory(string: str, operators: OperatorSet = None) -> Theory:
    if operators is None:
        return DEFAULT_CLAUSES_PARSER.parseTheory(string)
    else:
        return DEFAULT_CLAUSES_PARSER.parseTheory(string, operators)


def parse_clauses(string: str, operators: OperatorSet = None, lazy: bool = True) -> Iterable[Clause]:
    if lazy:
        if operators is None:
            return DEFAULT_CLAUSES_PARSER.parseClausesLazily(string)
        else:
            return DEFAULT_CLAUSES_PARSER.parseClausesLazily(string, operators)
    else:
        if operators is None:
            return DEFAULT_CLAUSES_PARSER.parseClauses(string)
        else:
            return DEFAULT_CLAUSES_PARSER.parseClauses(string, operators)


def read_theory(input: Union[InputStream, str], operators: OperatorSet = None) -> Theory:
    input = ensure_input_steam(input)
    if operators is None:
        return DEFAULT_CLAUSES_READER.readTheory(input)
    else:
        return DEFAULT_CLAUSES_READER.readTheory(input, operators)


def read_clauses(input: Union[InputStream, str], operators: OperatorSet = None, lazy: bool = True) -> Iterable[Clause]:
    input = ensure_input_steam(input)
    if lazy:
        if operators is None:
            return DEFAULT_CLAUSES_READER.readClausesLazily(input)
        else:
            return DEFAULT_CLAUSES_READER.readClausesLazily(input, operators)
    else:
        if operators is None:
            return DEFAULT_CLAUSES_READER.readClauses(input)
        else:
            return DEFAULT_CLAUSES_READER.readClauses(input, operators)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.theory.parsing.*")
