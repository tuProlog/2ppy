"""Tests for `tuprolog.errors`: Python exception classes injected as bases of 2P-Kt's exceptions."""

import warnings as python_warnings

import pytest
from jpype import JClass

from tuprolog import errors
from tuprolog.core import atom, integer, struct
from tuprolog.core.parsing import ParseException, parse_term
from tuprolog.errors import (
    HaltError,
    LibraryError,
    ParsingError,
    PrologDomainError,
    PrologError,
    PrologEvaluationError,
    PrologExistenceError,
    PrologInstantiationError,
    PrologMessageError,
    PrologPermissionError,
    PrologRepresentationError,
    PrologSyntaxError,
    PrologSystemError,
    PrologTypeError,
    PrologWarning,
    ResolutionError,
    SubstitutionError,
    TimeOutError,
    TuPrologError,
    UnificationError,
)
from tuprolog.solve import solve_options
from tuprolog.solve.prolog import prolog_solver

PACKAGES = {
    "core": "it.unibo.tuprolog.core.",
    "solve": "it.unibo.tuprolog.solve.exception.",
    "error": "it.unibo.tuprolog.solve.exception.error.",
}

INJECTED = [
    (TuPrologError, "core", "exception.TuPrologException", (Exception,)),
    (SubstitutionError, "core", "exception.SubstitutionApplicationException", (ValueError,)),
    (ParsingError, "core", "parsing.ParseException", (ValueError,)),
    (ParsingError, "core", "parsing.InvalidTermTypeException", (ValueError,)),
    (UnificationError, "core", "../unify.exception.OccurCheckException", (ValueError,)),
    (LibraryError, "solve", "../library.exception.NoSuchALibraryException", ()),
    (ResolutionError, "solve", "ResolutionException", ()),
    (HaltError, "solve", "HaltException", ()),
    (TimeOutError, "solve", "TimeOutException", ()),
    (PrologWarning, "solve", "warning.MissingPredicate", (Warning,)),
    (PrologError, "solve", "LogicError", ()),
    (PrologTypeError, "error", "TypeError", (TypeError,)),
    (PrologDomainError, "error", "DomainError", (ValueError,)),
    (PrologRepresentationError, "error", "RepresentationError", (ValueError,)),
    (PrologInstantiationError, "error", "InstantiationError", (ValueError,)),
    (PrologEvaluationError, "error", "EvaluationError", (ArithmeticError,)),
    (PrologExistenceError, "error", "ExistenceError", (LookupError,)),
    (PrologPermissionError, "error", "PermissionError", ()),
    (PrologSyntaxError, "error", "SyntaxError", (ValueError,)),
    (PrologSystemError, "error", "SystemError", (RuntimeError,)),
    (PrologMessageError, "error", "MessageError", ()),
]


def jvm_class(package: str, name: str):
    prefix = PACKAGES[package]
    while name.startswith("../"):
        prefix, name = prefix.rsplit(".", 2)[0] + ".", name[3:]
    return JClass(prefix + name)


@pytest.mark.parametrize(
    "python, package, name, builtins", INJECTED, ids=[f"{p}.{n}" for _, p, n, _ in INJECTED]
)
def test_python_classes_are_bases_of_jvm_ones(python, package, name, builtins):
    jvm = jvm_class(package, name)
    assert issubclass(jvm, python)
    assert issubclass(jvm, TuPrologError)
    for builtin in builtins:
        assert issubclass(jvm, builtin)


def test_hierarchy():
    assert issubclass(PrologError, ResolutionError)
    assert issubclass(HaltError, ResolutionError)
    assert issubclass(PrologWarning, ResolutionError)
    for cls in vars(errors).values():
        if isinstance(cls, type) and cls.__module__ == errors.__name__:
            assert issubclass(cls, TuPrologError)
    assert not issubclass(PrologPermissionError, PermissionError)


def solve_error(goal: str, **kwargs):
    solution = prolog_solver(**kwargs).solve_once(parse_term(goal))
    assert solution.is_halt, solution
    return solution.exception


@pytest.mark.parametrize(
    "goal, expected, builtin",
    [
        ("atom_length(1, _)", PrologTypeError, TypeError),
        ("atom_length(_, _)", PrologInstantiationError, ValueError),
        ("_ is 1 / 0", PrologEvaluationError, ArithmeticError),
        ("atom_length(abc, -1)", PrologDomainError, ValueError),
        ("throw(error(system_error, x))", PrologSystemError, RuntimeError),
    ],
)
def test_solver_errors_are_catchable_as_python_ones(goal, expected, builtin):
    error = solve_error(goal)
    assert isinstance(error, expected)
    with pytest.raises(builtin):
        raise error
    with pytest.raises(PrologError):
        raise error


def test_existence_errors_are_lookup_errors():
    from tuprolog.solve.flags import DEFAULT_FLAG_STORE, Unknown

    error = solve_error("missing", flags=DEFAULT_FLAG_STORE.set(Unknown, Unknown.ERROR))
    assert isinstance(error, PrologExistenceError)
    assert isinstance(error, LookupError)


def test_logic_error_accessors():
    error = solve_error("atom_length(1, _)")
    assert error.type == struct("type_error", atom("atom"), integer(1))
    assert error.error_struct.functor == "error"
    assert error.error_struct[0] == error.type
    assert error.extra_data is not None
    assert error.message.startswith("The 0-th argument of `atom_length/2`")
    assert error.context is not None
    assert isinstance(error.logic_stack_trace, list)


def test_halt_error():
    error = solve_error("halt(3)")
    assert isinstance(error, HaltError)
    assert error.exit_status == 3


def test_timeout_error():
    solver = prolog_solver()
    solution = solver.solve_once(parse_term("repeat, fail"), solve_options(timeout=50))
    assert isinstance(solution.exception, TimeOutError)


def test_parse_errors_are_value_errors():
    with pytest.raises(ValueError, match="Unexpected end of input"):
        parse_term("f(")
    with pytest.raises(ParsingError):
        parse_term("f(")
    with pytest.raises(ParseException):
        parse_term("f(")


def test_warnings_are_python_warnings():
    from tuprolog.solve.channel import output_channel
    from tuprolog.solve.flags import DEFAULT_FLAG_STORE, Unknown

    warnings: list = []
    solver = prolog_solver(
        flags=DEFAULT_FLAG_STORE.set(Unknown, Unknown.WARNING),
        warning=output_channel(warnings.append),
    )
    solver.solve_once(parse_term("missing"))
    assert isinstance(warnings[0], PrologWarning)
    with pytest.warns(PrologWarning, match="missing/0"):
        python_warnings.warn(warnings[0], stacklevel=1)


def test_jvm_exceptions_built_from_python_keep_working():
    from tuprolog.core import Substitution
    from tuprolog.core.exception import SubstitutionException, TuPrologException

    with pytest.raises(TuPrologError, match="boom"):
        raise TuPrologException("boom")
    with pytest.raises(ValueError) as caught:
        raise SubstitutionException(Substitution.empty(), "bad")
    assert caught.value.message == "bad"
    assert isinstance(caught.value, SubstitutionError)


def test_python_exceptions_raised_by_python_code_are_not_classified():
    assert not isinstance(ValueError("x"), TuPrologError)
    assert not issubclass(ValueError, ParsingError)


def test_classifications_are_not_instantiable():
    with pytest.raises(TypeError):
        PrologTypeError("not a JVM exception")


def test_jpype_subclass_checks_are_preserved():
    throwable = JClass("java.lang.Throwable")
    runtime = JClass("java.lang.RuntimeException")
    assert issubclass(runtime, throwable)
    assert not issubclass(throwable, runtime)


def test_repr_shows_class_and_message():
    error = solve_error("atom_length(1, _)")
    assert repr(error) == f"{type(error).__name__}({error.message!r})"
    assert repr(error).startswith("it.unibo.tuprolog.solve.exception.error.TypeError('The 0-th")


def test_repr_of_errors_without_message_shows_their_term():
    error = solve_error("X is 1 / 0")
    assert error.message is None
    assert "evaluation_error(zero_divisor)" in repr(error)
