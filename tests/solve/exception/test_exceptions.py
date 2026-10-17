"""Base exceptions of tuprolog.solve.exception, tuprolog.solve.library.exception, and
tuprolog.unify.exception."""

import pytest

from tuprolog.core import atom, integer, struct, var
from tuprolog.core.exception import TuPrologException
from tuprolog.solve.exception import (
    HaltException,
    LogicError,
    ResolutionException,
    TimeOutException,
    Warning,
)
from tuprolog.solve.exception.error import (
    DomainError,
    EvaluationError,
    ExistenceError,
    InstantiationError,
    MessageError,
    PermissionError,
    RepresentationError,
    SyntaxError,
    TypeError,
)
from tuprolog.solve.exception.warning import InitializationIssue, MissingPredicate
from tuprolog.solve.library import libraries, library
from tuprolog.solve.library.exception import (
    AlreadyLoadedLibraryException,
    LibraryException,
    NoSuchALibraryException,
)
from tuprolog.solve.plp import solve_options
from tuprolog.solve.prolog import prolog_solver
from tuprolog.theory.parsing import parse_theory
from tuprolog.unify.exception import NoUnifyException, OccurCheckException

from .helpers import solve_once


@pytest.mark.parametrize(
    "subclass, superclass",
    [
        (ResolutionException, TuPrologException),
        (LogicError, ResolutionException),
        (Warning, ResolutionException),
        (HaltException, ResolutionException),
        (TimeOutException, ResolutionException),
        (DomainError, LogicError),
        (EvaluationError, LogicError),
        (ExistenceError, LogicError),
        (InstantiationError, LogicError),
        (MessageError, LogicError),
        (PermissionError, LogicError),
        (RepresentationError, LogicError),
        (SyntaxError, LogicError),
        (TypeError, LogicError),
        (InitializationIssue, Warning),
        (MissingPredicate, Warning),
        (AlreadyLoadedLibraryException, LibraryException),
        (NoSuchALibraryException, LibraryException),
        (LibraryException, TuPrologException),
        (OccurCheckException, NoUnifyException),
        (NoUnifyException, TuPrologException),
    ],
)
def test_hierarchy(subclass, superclass):
    assert issubclass(subclass, superclass)
    assert issubclass(subclass, Exception)


def test_resolution_exception(context):
    exception = ResolutionException("boom", None, context)
    assert exception.message == "boom"
    assert exception.context == context
    assert list(exception.contexts) == [context]
    assert list(exception.logic_stack_trace) == list(context.logic_stack_trace)
    assert len(exception.push_context(context).contexts) == 2
    with pytest.raises(ResolutionException):
        raise exception


@pytest.mark.parametrize(
    "error_type, expected_class",
    [
        (atom("instantiation_error"), InstantiationError),
        (atom("syntax_error"), SyntaxError),
        (struct("type_error", atom("atom"), integer(1)), TypeError),
        (struct("domain_error", atom("order"), atom("x")), DomainError),
        (struct("evaluation_error", atom("zero_divisor")), EvaluationError),
        (struct("representation_error", atom("max_arity")), RepresentationError),
        (
            struct("permission_error", atom("modify"), atom("flag"), atom("x")),
            PermissionError,
        ),
    ],
)
def test_logic_error_of_builds_the_right_subclass(context, error_type, expected_class):
    error = LogicError.of("msg", None, context, error_type, atom("extra"))
    assert isinstance(error, expected_class)
    assert error.getType() == error_type
    assert error.error_struct == struct("error", error_type, atom("extra"))


def test_logic_error_of_existence_error(context):
    # ObjectType.fromTerm only accepts upper-case names (see test_existence_error.py)
    error_type = struct("existence_error", atom("PROCEDURE"), atom("x"))
    error = LogicError.of("msg", None, context, error_type, atom("extra"))
    assert isinstance(error, ExistenceError)
    assert error.getType() == struct("existence_error", atom("procedure"), atom("x"))


def test_logic_error_of_custom_type(context):
    error = LogicError.of(None, None, context, struct("my_error", atom("x")), None)
    assert type(error) is not LogicError
    assert isinstance(error, LogicError)
    assert error.getType() == struct("my_error", atom("x"))
    assert error.error_struct == struct("error", struct("my_error", atom("x")), atom(""))


@pytest.mark.xfail(
    strict=True,
    reason="JVM strings are not converted: Throwable.message (tuprolog/jvmutils.py) returns a "
    "java.lang.String instead of a Python str",
)
def test_message_is_a_python_string(context):
    assert isinstance(ResolutionException("boom", None, context).message, str)


def test_halt_exception_from_solver():
    solution = solve_once(prolog_solver(), "halt(3)")
    assert solution.is_halt
    exception = solution.getException()
    assert isinstance(exception, HaltException)
    assert exception.exit_status == 3


def test_halt_exception(context):
    exception = HaltException(2, "bye", None, context)
    assert exception.exit_status == 2
    assert exception.message == "bye"
    assert isinstance(exception.push_context(context), HaltException)


def test_time_out_exception_from_solver():
    solver = prolog_solver(static_kb=parse_theory("loop :- loop."))
    solution = solver.solve_once(atom("loop"), solve_options(timeout=100))
    assert solution.is_halt
    exception = solution.getException()
    assert isinstance(exception, TimeOutException)
    assert exception.exceeded_duration == 100


def test_already_loaded_library_exception():
    with pytest.raises(AlreadyLoadedLibraryException) as info:
        libraries(library("dup"), library("dup"))
    assert isinstance(info.value, LibraryException)
    assert info.value.message == "A library aliased as `dup` has already been loaded"


def test_library_exceptions_constructors():
    assert LibraryException("msg", None).message == "msg"
    assert AlreadyLoadedLibraryException("msg", None).message == "msg"
    assert NoSuchALibraryException("msg", None).message == "msg"


def test_no_unify_exception():
    exception = NoUnifyException(atom("a"), atom("b"))
    assert exception.getMessage() == "Cannot match term `a` with term `b`"
    with pytest.raises(NoUnifyException):
        raise exception


def test_occur_check_exception():
    x = var("X")
    fx = struct("f", x)
    exception = OccurCheckException(x, fx, x, fx)
    assert isinstance(exception, NoUnifyException)
    assert str(exception.getMessage()) == (
        f"Cannot match term `{x}` with term `{fx}` because variable `{x}` occurs in term `{fx}`"
    )


def test_no_unify_exception_message_property():
    assert NoUnifyException(atom("a"), atom("b")).message == "Cannot match term `a` with term `b`"
