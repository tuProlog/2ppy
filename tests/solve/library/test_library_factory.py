"""The `library()` factory, Library/Runtime customizers, and libraries loaded into solvers."""

import pytest

from tests.solve.primitive._support import bindings, python_int, solve_all
from tuprolog.core import integer
from tuprolog.core.operators import XFX, operator, operator_set
from tuprolog.solve import signature
from tuprolog.solve.function import compute_response, logic_function
from tuprolog.solve.library import Library, Runtime, libraries, library
from tuprolog.solve.library.exception import AlreadyLoadedLibraryException
from tuprolog.solve.primitive import primitive
from tuprolog.solve.prolog import prolog_solver
from tuprolog.theory import theory
from tuprolog.theory.parsing import parse_theory

ALWAYS = primitive(lambda r: [r.reply_success()])
DOUBLE = logic_function(lambda r: compute_response(integer(python_int(r.arguments[0]) * 2)))
ARROW = operator("===>", XFX, 700)


def test_library_defaults():
    lib = library("empty")
    assert isinstance(lib, Library)
    assert lib.alias == "empty"
    assert len(lib.primitives) == 0
    assert len(lib.functions) == 0
    assert len(list(lib.clauses)) == 0
    assert len(list(lib.operators)) == 0


def test_library_without_alias():
    lib = library(primitives={signature("always", 0): ALWAYS})
    assert lib.has_primitive(signature("always", 0))
    assert (
        prolog_solver(libraries=lib)
        .solve_once(__import__("tuprolog.core", fromlist=["atom"]).atom("always"))
        .is_yes
    )


def test_library_contents():
    clauses = parse_theory("twice(X, Y) :- Y is double(X).")
    lib = library(
        "lib.full",
        primitives={signature("always", 0): ALWAYS},
        clauses=clauses,
        operators=operator_set(ARROW),
        functions={signature("double", 1): DOUBLE},
    )
    assert lib.has_primitive(signature("always", 0))
    assert lib.has_function(signature("double", 1))
    assert lib.has_rule(signature("twice", 2))
    assert list(lib.clauses) == list(clauses)
    assert list(lib.operators) == [ARROW]


@pytest.fixture(scope="module")
def full_solver():
    lib = library(
        "lib.full",
        primitives={signature("always", 0): ALWAYS},
        clauses=parse_theory("twice(X, Y) :- Y is double(X)."),
        operators=operator_set(ARROW),
        functions={signature("double", 1): DOUBLE},
    )
    return prolog_solver(libraries=lib)


def test_library_primitives_in_solver(full_solver):
    assert solve_all(full_solver, "always")[0].is_yes
    assert solve_all(full_solver, "'lib.full.always'")[0].is_yes


def test_library_functions_in_solver(full_solver):
    assert bindings(solve_all(full_solver, "X is double(21)"), "X") == ["42"]
    assert bindings(solve_all(full_solver, "X is 'lib.full.double'(2) + 1"), "X") == ["5"]


def test_library_clauses_in_solver(full_solver):
    assert bindings(solve_all(full_solver, "twice(4, Y)"), "Y") == ["8"]


def test_library_clauses_are_protected(full_solver):
    assert solve_all(full_solver, "assertz(twice(a, b))")[0].is_halt


def test_library_operators_in_solver(full_solver):
    assert bindings(solve_all(full_solver, "current_op(P, xfx, '===>')"), "P") == ["700"]


def test_library_clauses_from_python_list():
    lib = library("lib.list", clauses=list(theory(*parse_theory("p(1). p(2)."))))
    assert bindings(solve_all(prolog_solver(libraries=lib), "p(X)"), "X") == ["1", "2"]


def test_library_to_runtime():
    lib = library("a")
    runtime = lib.to_runtime()
    assert isinstance(runtime, Runtime)
    assert [str(a) for a in runtime.keySet()] == ["a"]


def test_runtime_addition():
    runtime = libraries(library("a")) + library("b")
    assert isinstance(runtime, Runtime)
    assert [str(a) for a in runtime.keySet()] == ["a", "b"]
    runtime = libraries(library("a")) + libraries(library("b"), library("c"))
    assert [str(a) for a in runtime.keySet()] == ["a", "b", "c"]


def test_runtime_addition_rejects_duplicates():
    with pytest.raises(AlreadyLoadedLibraryException):
        libraries(library("a")) + library("a")


def test_runtime_lookup():
    lib = library("a", primitives={signature("always", 0): ALWAYS})
    runtime = libraries(lib)
    assert runtime["a"] == lib
    assert "a" in runtime
    assert runtime.has_primitive(signature("always", 0))
    assert runtime.has_primitive(signature("a.always", 0))


def test_solver_loads_prolog_lang_besides_given_libraries():
    solver = prolog_solver(libraries=libraries(library("a"), library("b")))
    assert {"a", "b"} <= {str(a) for a in solver.libraries.keySet()}


def test_solver_load_library_at_runtime():
    solver = prolog_solver()
    assert solve_all(solver, "always")[0].is_no
    solver.load_library(library("late", primitives={signature("always", 0): ALWAYS}))
    assert solve_all(solver, "always")[0].is_yes


@pytest.mark.parametrize("operators", [lambda: [ARROW], lambda: (ARROW,), lambda: iter([ARROW])])
def test_library_operators_from_python_iterables(operators):
    lib = library("lib.ops", operators=operators())
    assert list(lib.operators) == [ARROW]
