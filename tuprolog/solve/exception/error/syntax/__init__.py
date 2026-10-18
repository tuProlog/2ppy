"""Syntax errors: some text being read is not valid Prolog.

ISO Prolog's `syntax_error` error, thrown as `error(syntax_error, Extra)`, means that a sequence
of characters being read does not conform to Prolog's grammar: e.g. reading `f(` by `read/1`, or
converting it to a term by `term_to_atom/2`. Errors of Python code parsing text (see
`tuprolog.core.parsing`) are `tuprolog.errors.ParsingError`s instead, not logic errors.

The error is a `SyntaxError` (the JVM class: import it explicitly, as it shadows Python's
built-in name). Build errors with `syntax_error`, `syntax_error_while_parsing_term`, or
`syntax_error_while_parsing_clauses`; `error_detector` points at the offending character of a
text.

Examples:
    >>> from tuprolog.solve import signature
    >>> from tuprolog.solve.exception.error import *
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> context = prolog_solver().current_context
    >>> syntax_error_while_parsing_term(context, "f(", 1, 3, "unexpected end").error_struct
    error(syntax_error, 'Syntax error at 1:3 while parsing `f(`: unexpected end')

See Also:
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._api import *
from ._definitions import *
from ._definitions import SyntaxError  # not in __all__, as star-imports would shadow the builtin

__all__ = [
    "error_detector",
    "syntax_error",
    "syntax_error_while_parsing_clauses",
    "syntax_error_while_parsing_term",
]
