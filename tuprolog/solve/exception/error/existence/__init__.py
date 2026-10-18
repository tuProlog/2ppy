"""Existence errors: an operation refers to something that does not exist, e.g. a predicate.

ISO Prolog's `existence_error(Kind, Culprit)` error, thrown as
`error(existence_error(Kind, Culprit), Extra)`, means that the object `Culprit`, of the kind
`Kind`, does not exist: e.g. calling an undefined predicate `foo/1` throws
`existence_error(procedure, foo/1)` (when the `unknown` flag is `error`; by default it only
warns, see `tuprolog.solve.exception.warning`), and reading from a stream alias never opened
throws `existence_error(stream, Alias)`.

The error is an `ExistenceError`, and the kinds of objects are the values of the `ObjectType`
enumeration (also available as the `OBJECT_*` constants), including OOPLib's aliases, methods,
constructors, and properties (see `tuprolog.solve.libs`). Build errors with
`existence_error_for_procedure`, `existence_error_for_stream`, `existence_error_for_source_sink`,
`existence_error_for_resource`, or `existence_error`.

Examples:
    >>> from tuprolog.solve import signature
    >>> from tuprolog.solve.exception.error import *
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> context = prolog_solver().current_context
    >>> existence_error_for_procedure(context, signature("foo", 1)).error_struct
    error(existence_error(procedure, foo/1), 'Procedure `foo/1` does not exist')

See Also:
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._api import *
from ._definitions import *

__all__ = [
    "OBJECT_OOP_ALIAS",
    "OBJECT_OOP_CONSTRUCTOR",
    "OBJECT_OOP_METHOD",
    "OBJECT_OOP_PROPERTY",
    "OBJECT_PROCEDURE",
    "OBJECT_RESOURCE",
    "OBJECT_SOURCE_SINK",
    "OBJECT_STREAM",
    "ExistenceError",
    "ObjectType",
    "existence_error",
    "existence_error_for_procedure",
    "existence_error_for_resource",
    "existence_error_for_source_sink",
    "existence_error_for_stream",
    "object_type",
]
