# mypy: disable-error-code="call-arg"
# (JPype's metaclass takes the `internal` keyword)
"""Python exception classes for 2P-Kt's exceptions.

Each class is injected as a base of the matching JVM exception class: JVM exceptions are raised and
caught as they are, and `except` clauses can name either these classes or Python's built-in ones,
e.g. a logic `type_error` is both a `PrologTypeError` and a `TypeError`.
These classes only classify JVM exceptions: instantiate the JVM classes, not them.
"""

from _jpype import _JClass, _JException  # type: ignore
from jpype import JImplementationFor

__all__ = [
    "HaltError",
    "LibraryError",
    "ParsingError",
    "PrologDomainError",
    "PrologError",
    "PrologEvaluationError",
    "PrologExistenceError",
    "PrologInstantiationError",
    "PrologMessageError",
    "PrologPermissionError",
    "PrologRepresentationError",
    "PrologSyntaxError",
    "PrologSystemError",
    "PrologTypeError",
    "PrologWarning",
    "ResolutionError",
    "SubstitutionError",
    "TimeOutError",
    "TuPrologError",
    "UnificationError",
]

_CORE = "it.unibo.tuprolog.core."
_SOLVE = "it.unibo.tuprolog.solve."
_ERROR = _SOLVE + "exception.error."


_CLASSIFICATIONS: set[type] = set()

_jpype_subclasscheck = _JClass.__subclasscheck__


def _subclasscheck(cls, subclass):
    # JPype compares Java classes, and the classes in this module have no Java peer: use their MRO
    if cls in _CLASSIFICATIONS:
        return type.__subclasscheck__(cls, subclass)
    return _jpype_subclasscheck(cls, subclass)


_JClass.__subclasscheck__ = _subclasscheck

_jpype_doc = _JClass.__dict__["__doc__"]


def _doc(cls):
    # JPype documents classes from their Java peer, which the classes in this module (and JPype's
    # own bases) lack: they keep their docstring
    if cls not in _CLASSIFICATIONS:
        try:
            return _jpype_doc.__get__(cls)
        except TypeError:
            pass
    return cls.__dict__.get("__doc__")


_JClass.__doc__ = property(_doc, _jpype_doc.__set__)


def _repr(self) -> str:
    return f"{type(self).__name__}({self.message!r})"


def _base_of(*jvm_classes: str):
    def decorator(cls):
        _CLASSIFICATIONS.add(cls)
        cls.__repr__ = _repr  # on each class, as built-in exceptions' one may precede it in the MRO
        for jvm_class in jvm_classes:
            JImplementationFor(jvm_class, base=True)(cls)
        return cls

    return decorator


@_base_of(_CORE + "exception.TuPrologException")
class TuPrologError(_JException, internal=True):  # JPype's base keeps JPype building instances
    """Any exception raised by 2P-Kt."""


@_base_of(_CORE + "exception.SubstitutionException")
class SubstitutionError(TuPrologError, ValueError, internal=True):
    """A substitution could not be built or applied."""


@_base_of(
    _CORE + "parsing.ParseException", "it.unibo.tuprolog.parser.exceptions.PrologSyntaxException"
)
class ParsingError(TuPrologError, ValueError, internal=True):
    """Some text is not valid Prolog."""


@_base_of("it.unibo.tuprolog.unify.exception.NoUnifyException")
class UnificationError(TuPrologError, ValueError, internal=True):
    """Two terms do not unify."""


@_base_of(_SOLVE + "library.exception.LibraryException")
class LibraryError(TuPrologError, internal=True):
    """A library could not be found or loaded."""


@_base_of(_SOLVE + "exception.ResolutionException")
class ResolutionError(TuPrologError, internal=True):
    """Something went wrong while solving a query."""

    @property
    def context(self):
        return self.getContext()

    @property
    def logic_stack_trace(self) -> list:
        return list(self.getLogicStackTrace())


@_base_of(_SOLVE + "exception.HaltException")
class HaltError(ResolutionError, internal=True):
    """A query halted the solver, e.g. via `halt/1`."""

    @property
    def exit_status(self) -> int:
        return int(self.getExitStatus())


@_base_of(_SOLVE + "exception.TimeOutException")
class TimeOutError(ResolutionError, internal=True):
    """A query ran out of time."""


@_base_of(_SOLVE + "exception.Warning")
class PrologWarning(ResolutionError, Warning, internal=True):
    """A warning issued while solving, e.g. for a missing predicate."""


@_base_of(_SOLVE + "exception.LogicError")
class PrologError(ResolutionError, internal=True):
    """An ISO Prolog error, i.e. the exception thrown as `error(Type, Extra)`."""

    @property
    def type(self):
        """The error type, e.g. `type_error(atom, 1)`."""
        return self.getType()

    @property
    def extra_data(self):
        return self.getExtraData()

    @property
    def error_struct(self):
        """The thrown term, i.e. `error(Type, Extra)`."""
        return self.getErrorStruct()


@_base_of(_ERROR + "TypeError")
class PrologTypeError(PrologError, TypeError, internal=True):
    pass


@_base_of(_ERROR + "DomainError")
class PrologDomainError(PrologError, ValueError, internal=True):
    pass


@_base_of(_ERROR + "RepresentationError")
class PrologRepresentationError(PrologError, ValueError, internal=True):
    pass


@_base_of(_ERROR + "InstantiationError")
class PrologInstantiationError(PrologError, ValueError, internal=True):
    pass


@_base_of(_ERROR + "EvaluationError")
class PrologEvaluationError(PrologError, ArithmeticError, internal=True):
    pass


@_base_of(_ERROR + "ExistenceError")
class PrologExistenceError(PrologError, LookupError, internal=True):
    pass


@_base_of(_ERROR + "PermissionError")
class PrologPermissionError(PrologError, internal=True):
    pass


@_base_of(_ERROR + "SyntaxError")
class PrologSyntaxError(PrologError, ValueError, internal=True):
    pass


@_base_of(_ERROR + "SystemError")
class PrologSystemError(PrologError, RuntimeError, internal=True):
    pass


@_base_of(_ERROR + "MessageError")
class PrologMessageError(PrologError, internal=True):
    pass
