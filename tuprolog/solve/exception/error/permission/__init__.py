"""Permission errors: an operation is not allowed on some object, e.g. changing a static predicate.

ISO Prolog's `permission_error(Operation, Kind, Culprit)` error, thrown as
`error(permission_error(Operation, Kind, Culprit), Extra)`, means that `Operation` (e.g.
`modify`, `access`, `input`) is not allowed on `Culprit`, an object of kind `Kind` (e.g.
`private_procedure`, `stream`): e.g. `assertz(atom(x))` throws
`permission_error(modify, private_procedure, atom/1)`, as library predicates cannot be changed.

The error is a `PermissionError` (the JVM class: import it explicitly, as it shadows Python's
built-in name), the operations are the values of the `Operation` enumeration (also available as
the `OPERATION_*` constants), and the kinds of objects those of the `Permission` enumeration (also
available as the `PERMISSION_*` constants). Build errors with `permission_error`.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> prolog_solver().solve_once("catch(assertz(atom(x)), error(E, _), true)")["E"]
    permission_error(modify, private_procedure, atom/1)

See Also:
    `tuprolog.solve.primitive.ensuring_procedure_has_permission`, raising these errors;
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._api import *
from ._definitions import *
from ._definitions import (
    PermissionError,  # not in __all__, as star-imports would shadow the builtin
)

__all__ = [
    "OPERATION_ACCESS",
    "OPERATION_ADD_ALIAS",
    "OPERATION_CLOSE",
    "OPERATION_CREATE",
    "OPERATION_INPUT",
    "OPERATION_INVOKE",
    "OPERATION_MODIFY",
    "OPERATION_OPEN",
    "OPERATION_OUTPUT",
    "OPERATION_REPOSITION",
    "PERMISSION_BINARY_STREAM",
    "PERMISSION_FLAG",
    "PERMISSION_OOP_METHOD",
    "PERMISSION_OPERATOR",
    "PERMISSION_PAST_END_OF_STREAM",
    "PERMISSION_PRIVATE_PROCEDURE",
    "PERMISSION_SOURCE_SINK",
    "PERMISSION_STATIC_PROCEDURE",
    "PERMISSION_STREAM",
    "PERMISSION_TEXT_STREAM",
    "Operation",
    "Permission",
    "operation",
    "permission_error",
    "permission_type",
]
