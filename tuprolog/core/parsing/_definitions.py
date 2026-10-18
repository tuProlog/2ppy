import it.unibo.tuprolog.core.parsing as _parsing  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "DEFAULT_TERM_PARSER",
    "DEFAULT_TERM_READER",
    "InvalidTermTypeException",
    "ParseException",
    "TermParser",
    "TermReader",
]


TermParser = _parsing.TermParser
"""A parser of terms from strings, holding a default operator set.

Each method parses one term (without the final `.`), checks that it has the requested type, and
raises `ParseException` on syntax errors (`InvalidTermTypeException` on type mismatches).
Variables with the same name in one string are the same variable; `_` is anonymous.

Build parsers with `tuprolog.core.parsing.term_parser`, or use `DEFAULT_TERM_PARSER`. Members:
`default_operator_set`, and the methods `parse_term`, `parse_struct`, `parse_constant`,
`parse_var`, `parse_atom`, `parse_numeric`, `parse_integer`, `parse_real`, `parse_clause` (each
taking a string and, optionally, an operator set), plus `parse` (an alias of `parse_term`).

Examples:
    >>> from tuprolog.core.parsing import term_parser
    >>> parser = term_parser()
    >>> parser.parse_clause("ancestor(X, Y) :- parent(X, Y)")
    ancestor(X_..., Y_...) :- parent(X_..., Y_...)

Note:
    2P-Kt's `it.unibo.tuprolog.core.parsing.TermParser`.
"""


TermReader = _parsing.TermReader
"""A reader of terms from streams, i.e. of Prolog text made of terms each ending with `.`, holding a
default operator set.

Build readers with `tuprolog.core.parsing.term_reader`, or use `DEFAULT_TERM_READER`. Members:
`default_operator_set`, `read_term(input, operators=None)` (the next term, or `None` at the end),
`read_terms(input, operators=None)` (all terms, lazily), and their aliases `read` and `read_all`.
The input is a JVM `InputStream`, a Python stream (binary or text), or a file path; it is closed
once read.

Examples:
    >>> import io
    >>> from tuprolog.core.parsing import term_reader
    >>> list(term_reader().read_terms(io.StringIO("parent(homer, bart). parent(abe, homer).")))
    [parent(homer, bart), parent(abe, homer)]

Note:
    2P-Kt's `it.unibo.tuprolog.core.parsing.TermReader`.
"""


ParseException = _parsing.ParseException
"""Raised when parsing fails because the text is not valid Prolog syntax.

Members: `input` (the parsed text, or the name of the source), `offending_symbol` (the text where
parsing failed, when known), `line` and `column` (where parsing failed, from 1).

Examples:
    >>> from tuprolog.core.parsing import parse_term
    >>> try:
    ...     parse_term("f(a")
    ... except ParseException as e:
    ...     print(e.line, e.column)
    1 4

Note:
    2P-Kt's `it.unibo.tuprolog.core.parsing.ParseException`.
"""


InvalidTermTypeException = _parsing.InvalidTermTypeException
"""Raised when parsing succeeds, but gives a term of another type than the requested one (e.g.
`parse_atom("f(x)")`). A `ParseException`.

Members: `term` (the parsed term), `type` (the requested type), and those of `ParseException`.

Note:
    2P-Kt's `it.unibo.tuprolog.core.parsing.InvalidTermTypeException`.
"""


DEFAULT_TERM_PARSER = TermParser.withDefaultOperators()
"""The term parser with the default operators (see `DEFAULT_OPERATORS`), used by the `parse_*`
functions."""


DEFAULT_TERM_READER = TermReader.withDefaultOperators()
"""The term reader with the default operators (see `DEFAULT_OPERATORS`), used by `read_term` and
`read_terms`."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.parsing.*")
