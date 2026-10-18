"""Type errors: an argument does not have the expected type, e.g. a number where an atom is due.

ISO Prolog's `type_error(Type, Culprit)` error, thrown as `error(type_error(Type, Culprit), Extra)`,
means that `Culprit` should have been of type `Type` (e.g. `integer`, `atom`, `callable`, `list`),
and it is not: e.g. `atom_length(f, a)` throws `type_error(integer, a)`. Unbound arguments raise
instantiation errors instead (see `tuprolog.solve.exception.error.instantiation`), and values of
the right type outside the admissible ones raise domain errors (see
`tuprolog.solve.exception.error.domain`).

The error is a `TypeError` (the JVM class: import it explicitly, as it shadows Python's built-in
name, though it is also a Python `TypeError`, see `tuprolog.errors`), and the expected types are
the values of the `Type` enumeration (also available as the `TYPE_*` constants). Build errors with
`type_error_for_argument` (the usual case, for primitives' arguments),
`type_error_for_argument_list`, `type_error_for_goal`, `type_error_for_term`, or `type_error`.

Examples:
    >>> from tuprolog.solve import signature
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> context = prolog_solver().current_context
    >>> from tuprolog.core import atom
    >>> error = type_error_for_argument(context, signature("foo", 2), TYPE_INTEGER, atom("a"), 1)
    >>> error.type
    type_error(integer, a)
    >>> error.message
    'The 1-th argument of `foo/2` should be a `integer`, but `a` has been provided instead'
    >>> prolog_solver().solve_once("catch(atom_length(f, a), error(E, _), true)")["E"]
    type_error(integer, a)

See Also:
    `tuprolog.solve.primitive`, whose `ensuring_argument_is_*` checks raise these errors;
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._api import *
from ._definitions import *
from ._definitions import TypeError  # not in __all__, as star-imports would shadow the builtin

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
    "expected_type",
    "type_error",
    "type_error_for_argument",
    "type_error_for_argument_list",
    "type_error_for_goal",
    "type_error_for_term",
]
