import it.unibo.tuprolog.solve.exception.error as errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

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
]


ExistenceError = errors.ExistenceError
"""The existence error, thrown as `error(existence_error(Kind, Culprit), _)`.

It means that there is no object `Culprit` of kind `Kind`.

The JVM class (also a Python `LookupError` and a `tuprolog.errors.PrologExistenceError`).
Members (snake_case aliases as well): `expected_object`, the `ObjectType`; `culprit`, the term
naming the missing object; besides those of `tuprolog.solve.exception.LogicError` (e.g. `type`,
`error_struct`, `message`).
"""


ObjectType = ExistenceError.ObjectType
"""The enumeration of the kinds of objects of existence errors (2P-Kt's `ObjectType`).

Each value (also available as an `OBJECT_*` constant) is the `Kind` of an
`existence_error(Kind, Culprit)` term: `to_term()` gives it as an atom (e.g. `procedure`).
`ObjectType.of(NAME)` (upper-case names only) and `ObjectType.fromTerm(term)` look a value up
(see `object_type`, accepting any case).
"""


OBJECT_PROCEDURE = ObjectType.PROCEDURE
"""`procedure`: a predicate (the culprit is its indicator, e.g. `foo/1`)."""


OBJECT_SOURCE_SINK = ObjectType.SOURCE_SINK
"""`source_sink`: a source or sink of streams, e.g. a file, or a stream alias."""


OBJECT_RESOURCE = ObjectType.RESOURCE
"""`resource`: a resource, e.g. one to load."""


OBJECT_STREAM = ObjectType.STREAM
"""`stream`: a stream."""


OBJECT_OOP_ALIAS = ObjectType.OOP_ALIAS
"""`oop_alias`: an OOPLib alias (`$Alias`) or type name (see `tuprolog.solve.libs`)."""


OBJECT_OOP_METHOD = ObjectType.OOP_METHOD
"""`oop_method`: a method or attribute of an object, called through OOPLib."""


OBJECT_OOP_CONSTRUCTOR = ObjectType.OOP_CONSTRUCTOR
"""`oop_constructor`: a constructor of a type, called through OOPLib."""


OBJECT_OOP_PROPERTY = ObjectType.OOP_PROPERTY
"""`oop_property`: a property of an object, accessed through OOPLib."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.ExistenceError.*")
