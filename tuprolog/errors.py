# mypy: disable-error-code="call-arg"
# (JPype's metaclass takes the `internal` keyword)
"""Python exception classes for 2P-Kt's exceptions.

Each class is injected as a base of the matching JVM exception class: JVM exceptions are raised and
caught as they are, and `except` clauses can name either these classes or Python's built-in ones,
e.g. a logic `type_error` is both a `PrologTypeError` and a `TypeError`.
These classes only classify JVM exceptions: instantiate the JVM classes, not them.

Solving a query does not raise the errors of the query itself: in Prolog, errors are *thrown* as
terms (e.g. `error(type_error(atom, 1), Extra)`), and they are reported as the `exception` of the
solution they end (see `tuprolog.solve`). Parsing, unification and library loading, instead, raise
their errors as Python exceptions.

| Class | Python bases | Raised when |
| --- | --- | --- |
| `TuPrologError` | `Exception` | 2P-Kt raises any exception |
| `SubstitutionError` | `TuPrologError`, `ValueError` | a substitution is invalid |
| `ParsingError` | `TuPrologError`, `ValueError` | some text is not valid Prolog |
| `UnificationError` | `TuPrologError`, `ValueError` | two terms do not unify |
| `LibraryError` | `TuPrologError` | a library cannot be found or loaded |
| `ResolutionError` | `TuPrologError` | solving a query goes wrong |
| `HaltError` | `ResolutionError` | a query halts the solver |
| `TimeOutError` | `ResolutionError` | a query runs out of time |
| `PrologWarning` | `ResolutionError`, `Warning` | a warning is issued while solving |
| `PrologError` | `ResolutionError` | an ISO error term `error(Type, Extra)` is thrown |
| `PrologTypeError` | `PrologError`, `TypeError` | `type_error(Type, Culprit)` |
| `PrologDomainError` | `PrologError`, `ValueError` | `domain_error(Domain, Culprit)` |
| `PrologRepresentationError` | `PrologError`, `ValueError` | `representation_error(Limit)` |
| `PrologInstantiationError` | `PrologError`, `ValueError` | `instantiation_error` |
| `PrologEvaluationError` | `PrologError`, `ArithmeticError` | `evaluation_error(Error)` |
| `PrologExistenceError` | `PrologError`, `LookupError` | `existence_error(Type, Culprit)` |
| `PrologPermissionError` | `PrologError` | `permission_error(Action, Type, Culprit)` |
| `PrologSyntaxError` | `PrologError`, `ValueError` | `syntax_error(Message)` |
| `PrologSystemError` | `PrologError`, `RuntimeError` | `system_error` |
| `PrologMessageError` | `PrologError` | any other error |

Each class classifies the 2P-Kt class named alike, with `Exception` in place of `Error` (e.g.
`TuPrologError` classifies `TuPrologException`), except: `ParsingError` classifies
`ParseException` and `PrologSyntaxException`, `UnificationError` classifies `NoUnifyException`,
`PrologWarning` classifies `Warning`, `PrologError` classifies `LogicError`, and the subclasses of
`PrologError` classify the classes in 2P-Kt's `it.unibo.tuprolog.solve.exception.error` package
named without the `Prolog` prefix (e.g. `PrologTypeError` classifies `TypeError`). Every JVM
exception keeps its JVM bases too (e.g. `java.lang.RuntimeException`), and its `message`.

Examples:
    >>> from tuprolog.core.parsing import parse_struct
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> solution = next(iter(prolog_solver().solve(parse_struct("atom_length(1, N)"))))
    >>> error = solution.exception
    >>> isinstance(error, PrologTypeError), isinstance(error, TypeError)
    (True, True)
    >>> error.type
    type_error(atom, 1)
    >>> from tuprolog.theory.parsing import parse_theory
    >>> try:
    ...     parse_theory("a :- .")
    ... except ValueError as error:
    ...     print(isinstance(error, ParsingError))
    True

See Also:
    2P-Kt's reference on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
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
        """The execution context in which the error occurred.

        It holds the solver's state at that time: its libraries, flags, knowledge bases and
        current substitution, among other things.
        """
        return self.getContext()

    @property
    def logic_stack_trace(self) -> list:
        """The goals being executed when the error occurred, innermost first.

        Each one is a `tuprolog.core.Struct`; the last one is the query, as `'?-'(Query)`.
        """
        return list(self.getLogicStackTrace())


@_base_of(_SOLVE + "exception.HaltException")
class HaltError(ResolutionError, internal=True):
    """A query halted the solver, e.g. via `halt/1`."""

    @property
    def exit_status(self) -> int:
        """The exit status the query asked for, e.g. 3 for `halt(3)`."""
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
        """The second argument of the thrown `error/2` term (usually a description), or None."""
        return self.getExtraData()

    @property
    def error_struct(self):
        """The thrown term, i.e. `error(Type, Extra)`."""
        return self.getErrorStruct()


@_base_of(_ERROR + "TypeError")
class PrologTypeError(PrologError, TypeError, internal=True):
    """A value has the wrong type, e.g. an atom was expected but `1` was given.

    Its `type` is `type_error(Type, Culprit)`, where `Type` is the expected type (e.g. `atom`,
    `integer`, `callable`, `evaluable`).
    """


@_base_of(_ERROR + "DomainError")
class PrologDomainError(PrologError, ValueError, internal=True):
    """A value has the right type but is not admissible, e.g. a negative length.

    Its `type` is `domain_error(Domain, Culprit)`, where `Domain` names the admissible values.
    """


@_base_of(_ERROR + "RepresentationError")
class PrologRepresentationError(PrologError, ValueError, internal=True):
    """An implementation limit was exceeded, e.g. a too large character code.

    Its `type` is `representation_error(Limit)`.
    """


@_base_of(_ERROR + "InstantiationError")
class PrologInstantiationError(PrologError, ValueError, internal=True):
    """An argument is an unbound variable, while a value is needed.

    Its `type` is `instantiation_error`, e.g. for `atom_length(X, N)`.
    """


@_base_of(_ERROR + "EvaluationError")
class PrologEvaluationError(PrologError, ArithmeticError, internal=True):
    """An arithmetic evaluation failed, e.g. a division by zero.

    Its `type` is `evaluation_error(Error)`, e.g. `evaluation_error(zero_divisor)` for `X is 1/0`.
    """


@_base_of(_ERROR + "ExistenceError")
class PrologExistenceError(PrologError, LookupError, internal=True):
    """Something which should exist does not, e.g. a called predicate or a file.

    Its `type` is `existence_error(Type, Culprit)`, e.g. `existence_error(procedure, foo/0)`.
    """


@_base_of(_ERROR + "PermissionError")
class PrologPermissionError(PrologError, internal=True):
    """An operation is not allowed, e.g. modifying a built-in predicate.

    Its `type` is `permission_error(Action, Type, Culprit)`, e.g.
    `permission_error(modify, static_procedure, atom_length/2)`.
    """


@_base_of(_ERROR + "SyntaxError")
class PrologSyntaxError(PrologError, ValueError, internal=True):
    """Some text read while solving (e.g. by `read_term/2`) is not valid Prolog.

    Its `type` is `syntax_error(Message)`. Parsing text from Python raises `ParsingError`s instead.
    """


@_base_of(_ERROR + "SystemError")
class PrologSystemError(PrologError, RuntimeError, internal=True):
    """An internal problem occurred, e.g. an uncaught exception that is not an `error/2` term.

    Its `type` is `system_error`.
    """


@_base_of(_ERROR + "MessageError")
class PrologMessageError(PrologError, internal=True):
    """An error which no other class represents, carrying a message."""
