"""Parsing terms and clauses from Prolog text.

*Parsing* turns text in Prolog syntax, e.g. `"parent(X, bart)"`, into terms. In one text, equally
named variables are the same variable (`_` excepted), and operators (see
`tuprolog.core.operators`) let expressions such as `X is 1 + 2` be read: parsers use the default
operator set, unless given another one.

This package offers:

- functions parsing one term from a string with the default parser, possibly checking its type:
  `parse_term`, `parse_struct`, `parse_atom`, `parse_var`, `parse_constant`, `parse_numeric`,
  `parse_integer`, `parse_real`, `parse_clause`;
- functions reading terms ending with `.` from streams: `read_term` and `read_terms`;
- parsers and readers with custom operators (`TermParser`, `TermReader`, `term_parser`,
  `term_reader`), and the default ones (`DEFAULT_TERM_PARSER`, `DEFAULT_TERM_READER`);
- the exceptions raised on errors: `ParseException` and `InvalidTermTypeException`.

Examples:
    >>> from tuprolog.core.parsing import parse_clause, parse_term
    >>> parse_term("parent(X, bart)")
    parent(X_..., bart)
    >>> clause = parse_clause("grandparent(X, Z) :- parent(X, Y), parent(Y, Z)")
    >>> clause.head, clause.body_size
    (grandparent(X_..., Z_...), 2)

See Also:
    `tuprolog.theory.parsing`, for parsing whole theories (sequences of clauses).
"""

import tuprolog.core.parsing._adapters as _

from ._api import *
from ._definitions import *

__all__ = [
    "DEFAULT_TERM_PARSER",
    "DEFAULT_TERM_READER",
    "InvalidTermTypeException",
    "ParseException",
    "TermParser",
    "TermReader",
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
