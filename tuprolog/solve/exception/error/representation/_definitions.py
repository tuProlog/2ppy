import it.unibo.tuprolog.solve.exception.error as _errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

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
]


RepresentationError = _errors.RepresentationError
"""The representation error: a limit is exceeded, thrown as `error(representation_error(Limit), _)`.

The JVM class (also a Python `ValueError` and a `tuprolog.errors.PrologRepresentationError`).
Members (snake_case aliases as well): `limit`, the exceeded `Limit`; besides those of
`tuprolog.solve.exception.LogicError` (e.g. `type`, `error_struct`, `message`).
"""


Limit = RepresentationError.Limit
"""The enumeration of the limits of representation errors (2P-Kt's `RepresentationError.Limit`).

Each value (also available as a `LIMIT_*` constant) is the `Limit` of a
`representation_error(Limit)` term: `to_term()` gives it as an atom (e.g. `max_arity`), and
`limit` as a string. `Limit.of(name)` and `Limit.fromTerm(term)` look a value up (see `limit`).
"""


LIMIT_CHARACTER = Limit.CHARACTER
"""`character`: the exceeded limit is the set of characters."""


LIMIT_CHARACTER_CODE = Limit.CHARACTER_CODE
"""`character_code`: the exceeded limit is the range of character codes (0 to 65535)."""


LIMIT_IN_CHARACTER_CODE = Limit.IN_CHARACTER_CODE
"""`in_character_code`: the exceeded limit is the range of input character codes.

That is, character codes, or -1 for the end of file.
"""


LIMIT_MAX_ARITY = Limit.MAX_ARITY
"""`max_arity`: the exceeded limit is the maximum arity of compound terms (the `max_arity` flag)."""


LIMIT_MAX_INTEGER = Limit.MAX_INTEGER
"""`max_integer`: the exceeded limit is the greatest integer (the `max_integer` flag)."""


LIMIT_MIN_INTEGER = Limit.MIN_INTEGER
"""`min_integer`: the exceeded limit is the least integer (the `min_integer` flag)."""


LIMIT_OOP_OBJECT = Limit.OOP_OBJECT
"""`oop_object`: the exceeded limit is the objects a term can be converted into, through OOPLib.

See `tuprolog.solve.libs`.
"""


LIMIT_TOO_MANY_VARIABLES = Limit.TOO_MANY_VARIABLES
"""`too_many_variables`: the exceeded limit is the number of variables a term may contain."""


logger.debug(
    "Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.RepresentationError.*"
)
