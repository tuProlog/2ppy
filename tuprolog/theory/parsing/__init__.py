import tuprolog.theory.parsing._adapters as _

from ._api import *
from ._definitions import *

__all__ = [
    "DEFAULT_CLAUSES_PARSER",
    "DEFAULT_CLAUSES_READER",
    "ClausesParser",
    "ClausesReader",
    "clauses_parser",
    "clauses_reader",
    "parse_clauses",
    "parse_theory",
    "read_clauses",
    "read_theory",
]
