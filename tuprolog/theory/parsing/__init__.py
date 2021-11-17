from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.theory.parsing as _parsing
from tuprolog.core import Clause
from tuprolog.core.parsing import _factory
from tuprolog.theory import Theory
from tuprolog.jvmutils import InputStream
from tuprolog.core.operators import OperatorSet
from typing import Union, Iterable
from ._ktadapt import *


ClausesParser = _parsing.ClausesParser

ClausesReader = _parsing.ClausesReader


def clauses_parser(with_default_operators: bool = True, operators: OperatorSet = None) -> ClausesParser:
    return _factory(ClausesParser, with_default_operators, operators)


def clauses_reader(with_default_operators: bool = True, operators: OperatorSet = None) -> ClausesReader:
    return _factory(ClausesReader, with_default_operators, operators)


DEFAULT_CLAUSES_PARSER = clauses_parser()

DEFAULT_CLAUSES_READER = clauses_reader()


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


logger.debug("Loaded JVM classes from it.unibo.tuprolog.theory.parsing.*")
