"""Representation errors: an implementation limit is exceeded, e.g. the maximum arity.

ISO Prolog's `representation_error(Limit)` error, thrown as `error(representation_error(Limit),
Extra)`, means that a value cannot be represented by the implementation, as it exceeds the limit
`Limit`: e.g. `functor(F, foo, N)` with `N` greater than the `max_arity` flag throws
`representation_error(max_arity)`, and `char_code(C, -1)` throws
`representation_error(character_code)`.

The error is a `RepresentationError`, and the limits are the values of the `Limit` enumeration
(also available as the `LIMIT_*` constants). Build errors with `representation_error`.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> prolog_solver().solve_once("catch(char_code(C, -1), error(E, _), true)")["E"]
    representation_error(character_code)

See Also:
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._api import *
from ._definitions import *

__all__ = [
    "LIMIT_CHARACTER",
    "LIMIT_CHARACTER_CODE",
    "LIMIT_IN_CHARACTER_CODE",
    "LIMIT_MAX_ARITY",
    "LIMIT_MAX_INTEGER",
    "LIMIT_MIN_INTEGER",
    "LIMIT_OOP_OBJECT",
    "LIMIT_TOO_MANY_VARIABLES",
    "Limit",
    "RepresentationError",
    "limit",
    "representation_error",
]
