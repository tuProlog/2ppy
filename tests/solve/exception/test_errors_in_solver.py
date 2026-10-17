"""Errors raised from Python primitives, or by Prolog built-ins, as seen through the solver."""

from collections.abc import Callable

import pytest

from tuprolog.core import atom, integer, struct, var
from tuprolog.solve import signature
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error import (
    DOMAIN_ORDER,
    ERROR_ZERO_DIVISOR,
    LIMIT_MAX_ARITY,
    OBJECT_PROCEDURE,
    OPERATION_MODIFY,
    PERMISSION_STATIC_PROCEDURE,
    TYPE_CALLABLE,
    DomainError,
    EvaluationError,
    ExistenceError,
    InstantiationError,
    PermissionError,
    RepresentationError,
    SyntaxError,
    TypeError,
    domain_error_for_goal,
    domain_error_for_term,
    evaluation_error,
    existence_error,
    existence_error_for_procedure,
    existence_error_for_resource,
    existence_error_for_source_sink,
    existence_error_for_stream,
    instantiation_error_for_argument,
    instantiation_error_for_goal,
    permission_error,
    representation_error,
    syntax_error,
    syntax_error_while_parsing_clauses,
    syntax_error_while_parsing_term,
    type_error_for_goal,
)
from tuprolog.solve.library import library
from tuprolog.solve.primitive import primitive
from tuprolog.solve.prolog import prolog_solver

from .helpers import solve_once, solver_raising

FOO = signature("foo", 1)

FACTORIES: dict[str, tuple[Callable, type, object]] = {
    "domain_for_term": (
        lambda r: domain_error_for_term(r.context, DOMAIN_ORDER, atom("x")),
        DomainError,
        struct("domain_error", atom("order"), atom("x")),
    ),
    "domain_for_goal": (
        lambda r: domain_error_for_goal(r.context, FOO, DOMAIN_ORDER, atom("x")),
        DomainError,
        struct("domain_error", atom("order"), atom("x")),
    ),
    "evaluation": (
        lambda r: evaluation_error(r.context, ERROR_ZERO_DIVISOR, "zero"),
        EvaluationError,
        struct("evaluation_error", atom("zero_divisor")),
    ),
    "existence": (
        lambda r: existence_error(r.context, OBJECT_PROCEDURE, atom("x"), "msg"),
        ExistenceError,
        struct("existence_error", atom("procedure"), atom("x")),
    ),
    "existence_for_procedure": (
        lambda r: existence_error_for_procedure(r.context, FOO),
        ExistenceError,
        struct("existence_error", atom("procedure"), struct("/", atom("foo"), integer(1))),
    ),
    "existence_for_source_sink": (
        lambda r: existence_error_for_source_sink(r.context, "s"),
        ExistenceError,
        struct("existence_error", atom("source_sink"), atom("s")),
    ),
    "existence_for_stream": (
        lambda r: existence_error_for_stream(r.context, struct("s", integer(1))),
        ExistenceError,
        struct("existence_error", atom("stream"), struct("s", integer(1))),
    ),
    "existence_for_resource": (
        lambda r: existence_error_for_resource(r.context, "r"),
        ExistenceError,
        struct("existence_error", atom("resource"), atom("r")),
    ),
    "instantiation_for_argument": (
        lambda r: instantiation_error_for_argument(r.context, FOO, var("X")),
        InstantiationError,
        atom("instantiation_error"),
    ),
    "instantiation_for_goal": (
        lambda r: instantiation_error_for_goal(r.context, FOO, var("X")),
        InstantiationError,
        atom("instantiation_error"),
    ),
    "permission": (
        lambda r: permission_error(
            r.context, FOO, OPERATION_MODIFY, PERMISSION_STATIC_PROCEDURE, atom("x")
        ),
        PermissionError,
        struct("permission_error", atom("modify"), atom("static_procedure"), atom("x")),
    ),
    "representation": (
        lambda r: representation_error(r.context, FOO, LIMIT_MAX_ARITY),
        RepresentationError,
        struct("representation_error", atom("max_arity")),
    ),
    "syntax": (lambda r: syntax_error(r.context, "bad"), SyntaxError, atom("syntax_error")),
    "syntax_while_parsing_term": (
        lambda r: syntax_error_while_parsing_term(r.context, "f(", 1, 2, "bad"),
        SyntaxError,
        atom("syntax_error"),
    ),
    "syntax_while_parsing_clauses": (
        lambda r: syntax_error_while_parsing_clauses(r.context, "f(", 0, 1, 2, "bad"),
        SyntaxError,
        atom("syntax_error"),
    ),
    "type_for_goal": (
        lambda r: type_error_for_goal(r.context, FOO, TYPE_CALLABLE, integer(1)),
        TypeError,
        struct("type_error", atom("callable"), integer(1)),
    ),
}


@pytest.fixture(scope="module")
def solver():
    return solver_raising(**{name: factory for name, (factory, _, _) in FACTORIES.items()})


@pytest.mark.parametrize("name", FACTORIES)
def test_error_raised_from_primitive_halts(solver, name):
    _, error_class, error_type = FACTORIES[name]
    solution = solve_once(solver, name)
    assert solution.is_halt
    exception = solution.getException()
    assert isinstance(exception, error_class)
    assert exception.getType() == error_type
    assert exception.error_struct[0] == error_type
    assert struct(name) in list(exception.logic_stack_trace)


@pytest.mark.parametrize("name", FACTORIES)
def test_error_raised_from_primitive_is_catchable(solver, name):
    _, _, error_type = FACTORIES[name]
    solution = solve_once(solver, f"catch({name}, error(Type, Extra), true)")
    assert solution.is_yes
    assert solution.substitution.getByName("Type") == error_type
    expected_extra = solve_once(solver, name).getException().extra_data
    assert solution.substitution.getByName("Extra") == expected_extra


@pytest.mark.parametrize("name", FACTORIES)
def test_error_raised_from_primitive_is_not_caught_by_mismatching_catch(solver, name):
    solution = solve_once(solver, f"catch({name}, not_an_error, true)")
    assert solution.is_halt
    assert isinstance(solution.getException(), FACTORIES[name][1])


def test_error_replied_from_primitive():
    def replying(request):
        error = type_error_for_goal(request.context, request.signature, TYPE_CALLABLE, integer(1))
        yield request.replyException(error, None)

    solver = prolog_solver(
        libraries=library("replying", primitives={signature("rep", 0): primitive(replying)})
    )
    solution = solve_once(solver, "rep")
    assert isinstance(solution.getException(), TypeError)
    caught = solve_once(solver, "catch(rep, error(type_error(T, C), _), true)")
    assert caught.substitution.getByName("T") == atom("callable")
    assert caught.substitution.getByName("C") == integer(1)


def test_python_exceptions_from_primitives_propagate():
    # like 2P-Kt, which only turns ResolutionExceptions into Halt solutions
    def failing(request):
        raise ValueError("python error")

    solver = prolog_solver(
        libraries=library("failing", primitives={signature("failing", 0): primitive(failing)})
    )
    with pytest.raises(ValueError, match="python error"):
        solve_once(solver, "failing")


@pytest.mark.parametrize(
    "query, error_class, error_type",
    [
        ("X is 1 / 0", EvaluationError, struct("evaluation_error", atom("zero_divisor"))),
        ("atom_length(X, Y)", InstantiationError, atom("instantiation_error")),
        ("atom_length(1, X)", TypeError, struct("type_error", atom("atom"), integer(1))),
        (
            "assertz(foo :- 1)",
            DomainError,
            struct("domain_error", atom("clause"), struct(":-", atom("foo"), integer(1))),
        ),
        (
            "assertz(atom_length(a, 1))",
            PermissionError,
            struct(
                "permission_error",
                atom("modify"),
                atom("private_procedure"),  # 2P-Kt's choice for library predicates
                struct("/", atom("atom_length"), integer(2)),
            ),
        ),
    ],
)
def test_builtin_errors(query, error_class, error_type):
    solution = solve_once(prolog_solver(), query)
    assert solution.is_halt
    exception = solution.getException()
    assert isinstance(exception, error_class)
    assert isinstance(exception, LogicError)
    assert exception.getType() == error_type


def test_thrown_error_terms_become_logic_errors():
    solution = solve_once(prolog_solver(), "throw(error(type_error(atom, 1), extra))")
    assert solution.is_halt
    exception = solution.getException()
    assert isinstance(exception, TypeError)
    assert exception.error_struct == struct(
        "error", struct("type_error", atom("atom"), integer(1)), atom("extra")
    )


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt ExistenceError.ObjectType.of() lacks uppercase(): throwing a standard "
    "existence_error(procedure, _) term makes solve_once raise IllegalArgumentException",
)
def test_thrown_existence_error_terms_become_logic_errors():
    solution = solve_once(prolog_solver(), "throw(error(existence_error(procedure, foo/1), x))")
    assert solution.is_halt
    assert isinstance(solution.getException(), ExistenceError)


def test_halt_solution_exception_property(solver):
    solution = solve_once(solver, "syntax")
    assert solution.exception == solution.getException()
