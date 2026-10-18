import it.unibo.tuprolog.solve.exception.error as _errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

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
]


PermissionError = _errors.PermissionError
"""The permission error, thrown as `error(permission_error(Operation, Kind, Culprit), _)`.

The JVM class (also a `tuprolog.errors.PrologPermissionError`). Members (snake_case aliases as
well): `operation`, the attempted `Operation`; `permission`, the `Permission` (kind of object)
lacking; `culprit`, the object; besides those of `tuprolog.solve.exception.LogicError` (e.g.
`type`, `error_struct`, `message`). Not star-exported, as it would shadow Python's built-in
`PermissionError`: import it explicitly.
"""


Operation = PermissionError.Operation
"""The enumeration of the operations of permission errors (2P-Kt's `PermissionError.Operation`).

Each value (also available as an `OPERATION_*` constant) is the `Operation` of a
`permission_error(Operation, Kind, Culprit)` term: `to_term()` gives it as an atom (e.g.
`modify`), and `operation` as a string. `Operation.of(name)` and `Operation.fromTerm(term)` look
a value up (see `operation`).
"""


Permission = PermissionError.Permission
"""The enumeration of the kinds of objects of permission errors (2P-Kt's `Permission`).

Each value (also available as a `PERMISSION_*` constant) is the `Kind` of a
`permission_error(Operation, Kind, Culprit)` term: `to_term()` gives it as an atom (e.g.
`static_procedure`), and `permission` as a string. `Permission.of(name)` and
`Permission.fromTerm(term)` look a value up (see `permission_type`).
"""


OPERATION_ACCESS = Operation.ACCESS
"""`access`: the operation of accessing an object.

E.g. reading a private procedure's clauses, or a private attribute through OOPLib.
"""


OPERATION_ADD_ALIAS = Operation.ADD_ALIAS
"""`add_alias`: the operation of adding an alias (e.g. to a stream, or an OOPLib alias in use)."""


OPERATION_CLOSE = Operation.CLOSE
"""`close`: the operation of closing a stream."""


OPERATION_CREATE = Operation.CREATE
"""`create`: the operation of creating an object (e.g. an operator, or a flag)."""


OPERATION_INPUT = Operation.INPUT
"""`input`: the operation of reading from a stream."""


OPERATION_INVOKE = Operation.INVOKE
"""`invoke`: the operation of invoking a method through OOPLib."""


OPERATION_MODIFY = Operation.MODIFY
"""`modify`: the operation of modifying an object (e.g. asserting or retracting clauses)."""


OPERATION_OPEN = Operation.OPEN
"""`open`: the operation of opening a source or sink."""


OPERATION_OUTPUT = Operation.OUTPUT
"""`output`: the operation of writing on a stream."""


OPERATION_REPOSITION = Operation.REPOSITION
"""`reposition`: the operation of repositioning a stream."""


PERMISSION_BINARY_STREAM = Permission.BINARY_STREAM
"""`binary_stream`: the object is a binary stream."""


PERMISSION_FLAG = Permission.FLAG
"""`flag`: the object is a Prolog flag (e.g. a read-only one).

Also used by OOPLib for aliases already registered.
"""


PERMISSION_OPERATOR = Permission.OPERATOR
"""`operator`: the object is an operator (e.g. `,`, which cannot be redefined)."""


PERMISSION_PAST_END_OF_STREAM = Permission.PAST_END_OF_STREAM
"""`past_end_of_stream`: the object is a stream already past its end."""


PERMISSION_PRIVATE_PROCEDURE = Permission.PRIVATE_PROCEDURE
"""`private_procedure`: the object is a private procedure, i.e. a predicate defined by a library."""


PERMISSION_SOURCE_SINK = Permission.SOURCE_SINK
"""`source_sink`: the object is a source or sink of streams."""


PERMISSION_STATIC_PROCEDURE = Permission.STATIC_PROCEDURE
"""`static_procedure`: the object is a static procedure (of the static knowledge base)."""


PERMISSION_OOP_METHOD = Permission.OOP_METHOD
"""`oop_method`: the object is a method or attribute of an object, accessed through OOPLib."""


PERMISSION_STREAM = Permission.STREAM
"""`stream`: the object is a stream."""


PERMISSION_TEXT_STREAM = Permission.TEXT_STREAM
"""`text_stream`: the object is a text stream."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.PermissionError.*")
