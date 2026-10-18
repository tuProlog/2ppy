"""The Pythonic layer on solvers: string goals, dict-like solutions, `query`, and primitives or
functions written as plain Python functions."""

import pytest

from tuprolog.core import Var, atom, integer, struct
from tuprolog.errors import HaltError, PrologSystemError, PrologTypeError
from tuprolog.solve import signature
from tuprolog.solve.function import function
from tuprolog.solve.library import library
from tuprolog.solve.primitive import predicate, primitive, python_error
from tuprolog.solve.prolog import prolog_solver
from tuprolog.theory.parsing import parse_theory

THEORY = "p(1, a). p(2.5, [x, y]). p(3, f(Z))."


@pytest.fixture
def solver():
    return prolog_solver(static_kb=parse_theory(THEORY))


# --- string goals ----------------------------------------------------------------------------------


def test_string_goals_use_the_solver_operators():
    solver = prolog_solver()
    assert solver.solve_once("op(700, xfx, ===>)").is_yes
    assert solver.solve_once("X = (a ===> b)")["X"] == struct("===>", atom("a"), atom("b"))


def test_string_goals_must_be_structs(solver):
    with pytest.raises(ValueError):
        solver.solve_once("X")


# --- solutions -------------------------------------------------------------------------------------


def test_solutions_are_truthy_when_positive(solver):
    assert solver.solve_once("p(1, _)")
    assert not solver.solve_once("p(9, _)")
    assert not solver.solve_once("atom_length(1, _)")


def test_solution_bindings(solver):
    solution = solver.solve_once("p(X, Y)")
    assert solution.bindings == {"X": integer(1), "Y": atom("a")}
    assert solution["X"] == integer(1)
    assert "Y" in solution
    assert "Z" not in solution
    with pytest.raises(KeyError):
        solution["Z"]


def test_bindings_skip_anonymous_variables(solver):
    assert solver.solve_once("p(X, _)").bindings.keys() == {"X"}


def test_negative_and_halted_solutions_have_no_bindings(solver):
    assert solver.solve_once("p(9, X)").bindings == {}
    assert solver.solve_once("atom_length(1, X)").to_dict() == {}


def test_solution_to_dict(solver):
    first, second, third = (s.to_dict() for s in solver.solve("p(X, Y)") if s)
    assert first == {"X": 1, "Y": "a"}
    assert second == {"X": 2.5, "Y": ["x", "y"]}
    assert third["X"] == 3
    assert third["Y"].functor == "f"


def test_raise_error(solver):
    solution = solver.solve_once("p(1, X)")
    assert solution.raise_error() is solution
    assert not solver.solve_once("p(9, X)").raise_error()
    with pytest.raises(TypeError):
        solver.solve_once("atom_length(1, X)").raise_error()


# --- query -----------------------------------------------------------------------------------------


def test_query_yields_python_bindings(solver):
    results = list(solver.query("p(X, Y)"))
    assert results[:2] == [{"X": 1, "Y": "a"}, {"X": 2.5, "Y": ["x", "y"]}]
    assert results[2]["X"] == 3
    assert results[2]["Y"].functor == "f"


def test_query_of_ground_goals(solver):
    assert list(solver.query("p(1, a)")) == [{}]
    assert list(solver.query("p(1, b)")) == []


def test_query_is_lazy_and_limited():
    solver = prolog_solver()
    assert list(solver.query("repeat", limit=3)) == [{}, {}, {}]
    assert [r["X"] for r in solver.query("member(X, [a, b, c])", limit=2)] == ["a", "b"]
    results = solver.query("repeat")
    assert [next(results) for _ in range(5)] == [{}] * 5


def test_query_raises_errors(solver):
    with pytest.raises(PrologTypeError):
        list(solver.query("atom_length(1, X)"))
    with pytest.raises(HaltError):
        list(solver.query("halt"))


def test_query_timeout():
    with pytest.raises(Exception, match="(?i)time"):
        list(prolog_solver().query("repeat, fail", timeout=50))


# --- predicates and functions ----------------------------------------------------------------------


def between(low, high, x):
    if isinstance(x, Var):
        for i in range(low, high + 1):
            yield low, high, i
    elif low <= x <= high:
        yield low, high, x


@pytest.fixture
def python_solver():
    lib = library(
        "py",
        primitives={
            "py_between/3": predicate(between),
            "even/1": predicate(lambda x: x % 2 == 0),
            "always/0": predicate(lambda: None),
            "upper/2": predicate(lambda s, _: [(s, s.upper())]),
            "digit/1": predicate(lambda _: range(3)),
            "wrong_arity/1": predicate(lambda _: [(1, 2)]),
            "divide/0": predicate(lambda: 1 / 0),
        },
        functions={"hypot/2": function(lambda a, b: (a * a + b * b) ** 0.5)},
    )
    return prolog_solver(libraries=lib)


def test_predicates_yielding_solutions(python_solver):
    assert [r["X"] for r in python_solver.query("py_between(1, 3, X)")] == [1, 2, 3]
    assert list(python_solver.query("py_between(1, 3, 2)")) == [{}]
    assert list(python_solver.query("py_between(1, 3, 7)")) == []


def test_predicates_returning_booleans(python_solver):
    assert list(python_solver.query("even(4)")) == [{}]
    assert list(python_solver.query("even(3)")) == []
    assert list(python_solver.query("always")) == [{}]


def test_predicates_bind_variables(python_solver):
    assert list(python_solver.query("upper(hello, U)")) == [{"U": "HELLO"}]
    assert list(python_solver.query("upper(hello, 'HELLO')")) == [{}]
    assert list(python_solver.query("upper(hello, bye)")) == []


def test_unary_predicates_yield_bare_values(python_solver):
    assert [r["D"] for r in python_solver.query("digit(D)")] == [0, 1, 2]


def test_predicates_with_wrong_outcomes_raise_system_errors(python_solver):
    with pytest.raises(PrologSystemError, match="ValueError"):
        list(python_solver.query("wrong_arity(_)"))
    with pytest.raises(PrologSystemError, match="ZeroDivisionError"):
        list(python_solver.query("divide"))
    assert list(python_solver.query("catch(divide, error(system_error, _), true)")) == [{}]


def test_functions(python_solver):
    assert list(python_solver.query("X is hypot(3, 4)")) == [{"X": 5.0}]
    assert list(python_solver.query("hypot(3, 4) > 4")) == [{}]


# --- errors from Python ----------------------------------------------------------------------------


def test_python_error_keeps_logic_errors():
    solver = prolog_solver()
    error = solver.solve_once("atom_length(1, _)").exception
    assert python_error(None, error) is error


def test_primitives_raising_logic_errors_halt_with_them():
    def raising(request):
        raise solver.solve_once("atom_length(1, _)").exception

    solver = prolog_solver()
    raising_solver = prolog_solver(
        libraries=library("r", primitives={"raising/0": primitive(raising)})
    )
    with pytest.raises(PrologTypeError):
        list(raising_solver.query("raising"))


# --- signatures ------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text, name, arity",
    [("succ/2", "succ", 2), ("a/b/1", "a/b", 1), ("//2", "/", 2), ("nil/0", "nil", 0)],
)
def test_signatures_from_strings(text, name, arity):
    assert signature(text) == signature(name, arity)


@pytest.mark.parametrize("text", ["succ", "succ/", "/2", "succ/x"])
def test_malformed_signature_strings(text):
    with pytest.raises(TypeError, match="name/arity"):
        signature(text)


def test_libraries_accept_signature_strings():
    lib = library("s", primitives={"yes/0": predicate(lambda: True)})
    assert signature("yes", 0) in lib.primitives
