import it.unibo.tuprolog.solve.exception.error as _errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "TYPE_ATOM",
    "TYPE_ATOMIC",
    "TYPE_BOOLEAN",
    "TYPE_BYTE",
    "TYPE_CALLABLE",
    "TYPE_CHARACTER",
    "TYPE_COMPOUND",
    "TYPE_DEALIASING_EXPRESSION",
    "TYPE_EVALUABLE",
    "TYPE_FLOAT",
    "TYPE_INTEGER",
    "TYPE_IN_CHARACTER",
    "TYPE_LIST",
    "TYPE_NUMBER",
    "TYPE_OBJECT_REFERENCE",
    "TYPE_PAIR",
    "TYPE_PREDICATE_INDICATOR",
    "TYPE_REFERENCE",
    "TYPE_TYPE_REFERENCE",
    "TYPE_URL",
    "TYPE_VARIABLE",
    "Type",
]


TypeError = _errors.TypeError
"""The type error, thrown as `error(type_error(Type, Culprit), _)`.

It means that `Culprit` should have been of type `Type`.

The JVM class (also a Python `TypeError` and a `tuprolog.errors.PrologTypeError`). Members
(snake_case aliases as well): `expected_type`, the expected `Type`; `culprit`, the offending term;
besides those of `tuprolog.solve.exception.LogicError` (e.g. `type`, `error_struct`, `message`).
Not star-exported, as it would shadow Python's built-in `TypeError`: import it explicitly.
"""


Type = TypeError.Expected
"""The enumeration of the types a type error may expect (2P-Kt's `TypeError.Expected`).

Each value (also available as a `TYPE_*` constant) is the `Type` of a
`type_error(Type, Culprit)` term: `to_term()` gives it as an atom (e.g. `integer`).
`Type.of(name)` and `Type.fromTerm(term)` look a value up (see `expected_type`).

Examples:
    >>> Type.INTEGER.to_term()
    integer
"""


TYPE_ATOM = Type.ATOM
"""`atom`: the expected type is an atom, e.g. `foo`."""


TYPE_ATOMIC = Type.ATOMIC
"""`atomic`: the expected type is an atomic term, i.e. an atom or a number."""


TYPE_BOOLEAN = Type.BOOLEAN
"""`boolean`: the expected type is a boolean, i.e. `true` or `false`."""


TYPE_BYTE = Type.BYTE
"""`byte`: the expected type is a byte, i.e. an integer from 0 to 255."""


TYPE_CALLABLE = Type.CALLABLE
"""`callable`: the expected type is a callable term, i.e. an atom or a compound term (a goal)."""


TYPE_CHARACTER = Type.CHARACTER
"""`character`: the expected type is a character, i.e. an atom of length 1."""


TYPE_COMPOUND = Type.COMPOUND
"""`compound`: the expected type is a compound term, i.e. a structure with arguments."""


TYPE_DEALIASING_EXPRESSION = Type.DEALIASING_EXPRESSION
"""`dealiasing_expression`: the expected type is a de-aliasing expression of OOPLib.

That is, `$Alias` with an atom `Alias` (see `tuprolog.solve.libs`).
"""


TYPE_EVALUABLE = Type.EVALUABLE
"""`evaluable`: the expected type is an evaluable functor, i.e. one of an arithmetic function.

The culprit is the indicator of the functor, e.g. `foo/1`.
"""


TYPE_FLOAT = Type.FLOAT
"""`float`: the expected type is a floating-point number."""


TYPE_INTEGER = Type.INTEGER
"""`integer`: the expected type is an integer."""


TYPE_IN_CHARACTER = Type.IN_CHARACTER
"""`in_character`: the expected type is an input character, i.e. a character or `end_of_file`."""


TYPE_LIST = Type.LIST
"""`list`: the expected type is a list, e.g. `[a, b]`."""


TYPE_NUMBER = Type.NUMBER
"""`number`: the expected type is a number, i.e. an integer or a floating-point one."""


TYPE_OBJECT_REFERENCE = Type.OBJECT_REFERENCE
"""`object_reference`: the expected type is a reference to a Python object.

See OOPLib, in `tuprolog.solve.libs`.
"""


TYPE_PAIR = Type.PAIR
"""`pair`: the expected type is a pair, i.e. a `Key - Value` term."""


TYPE_PREDICATE_INDICATOR = Type.PREDICATE_INDICATOR
"""`predicate_indicator`: the expected type is a predicate indicator, i.e. a `Name/Arity` term."""


TYPE_REFERENCE = Type.REFERENCE
"""`reference`: the expected type is a reference to a Python object or type.

See OOPLib, in `tuprolog.solve.libs`.
"""


TYPE_TYPE_REFERENCE = Type.TYPE_REFERENCE
"""`type_reference`: the expected type is a reference to a Python type.

See OOPLib, in `tuprolog.solve.libs`.
"""


TYPE_URL = Type.URL
"""`url`: the expected type is a URL or a file path, e.g. for `open/3,4` or `consult/1`."""


TYPE_VARIABLE = Type.VARIABLE
"""`variable`: the expected type is an unbound variable."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.TypeError.*")
