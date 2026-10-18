"""Primitives implemented in Python, bundled in libraries and invoked by solvers."""

from collections.abc import Iterable

import pytest

from tests.solve.primitive._support import (
    bindings,
    python_int,
    solve_all,
    solve_once,
    solver_with_primitive,
)
from tuprolog.core import atom, integer, logic_list, unifier
from tuprolog.solve import signature
from tuprolog.solve.flags import Unknown
from tuprolog.solve.primitive import (
    AbstractPrimitive,
    Primitive,
    SolveRequest,
    SolveResponse,
    primitive,
    solve_response,
)
from tuprolog.solve.sideffects import add_dynamic_clauses, set_flags
from tuprolog.theory.parsing import parse_theory
from tuprolog.unify import mgu


def between(request: SolveRequest) -> Iterable[SolveResponse]:
    low, high = (python_int(t) for t in request.arguments[:2])
    for i in range(low, high + 1):
        substitution = mgu(request.arguments[2], integer(i))
        if substitution.is_success:
            yield request.reply_with(substitution)


@pytest.fixture(scope="module")
def between_solver():
    return solver_with_primitive("py_between", 3, between)


def test_primitive_is_a_primitive():
    p = primitive(between)
    assert isinstance(p, Primitive)


def test_abstract_primitive_cannot_solve():
    with pytest.raises(NotImplementedError):
        AbstractPrimitive().solve(None)


def test_subclassing_abstract_primitive():
    class Answer(AbstractPrimitive):
        def solve(self, request):
            yield request.reply_with(mgu(request.arguments[0], integer(42)))

    solver = solver_with_primitive("answer", 1, Answer().solve)
    assert bindings(solve_all(solver, "answer(X)"), "X") == ["42"]
    from tests.solve.primitive._support import single_primitive_library  # noqa: F401
    from tuprolog.solve.library import library
    from tuprolog.solve.prolog import prolog_solver

    lib = library("lib.answer", primitives={signature("answer", 1): Answer()})
    assert bindings(solve_all(prolog_solver(libraries=lib), "answer(X)"), "X") == ["42"]


def test_generator_primitive_yields_many_solutions(between_solver):
    assert bindings(solve_all(between_solver, "py_between(1, 4, X)"), "X") == ["1", "2", "3", "4"]


def test_primitive_with_no_solutions_fails(between_solver):
    assert solve_all(between_solver, "py_between(3, 1, X)")[0].is_no


def test_primitive_solutions_are_lazy(between_solver):
    calls: list[int] = []

    def counting(request):
        for i in range(1000):
            calls.append(i)
            yield request.reply_with(mgu(request.arguments[0], integer(i)))

    solver = solver_with_primitive("counting", 1, counting)
    assert solve_once(solver, "counting(X)").is_yes
    assert len(calls) < 1000


def test_cut_prunes_primitive_solutions(between_solver):
    assert bindings(solve_all(between_solver, "py_between(1, 9, X), !"), "X") == ["1"]


def test_primitive_in_conjunctions_and_findall(between_solver):
    goal = "findall(X-Y, (py_between(1, 2, X), py_between(X, 2, Y)), L)"
    assert bindings(solve_all(between_solver, goal), "L") == ["['-'(1, 1), '-'(1, 2), '-'(2, 2)]"]


def test_primitive_with_ground_output(between_solver):
    assert [s.is_yes for s in solve_all(between_solver, "py_between(1, 3, 2)")] == [True]
    assert not any(s.is_yes for s in solve_all(between_solver, "py_between(1, 3, 5)"))


def test_failed_reply_ends_the_solutions_of_a_primitive():
    solver = solver_with_primitive("p", 0, lambda r: [r.reply_fail(), r.reply_success()])
    assert [s.is_yes for s in solve_all(solver, "p")] == [False]


def test_primitive_returning_a_list():
    solver = solver_with_primitive("p", 0, lambda r: [r.reply_success(), r.reply_success()])
    assert len(solve_all(solver, "p")) == 2


def test_primitive_returning_an_empty_list_fails():
    solver = solver_with_primitive("p", 0, lambda r: [])
    assert solve_all(solver, "p")[0].is_no


def test_primitive_called_from_rules(between_solver):
    solver = solver_with_primitive(
        "py_between", 3, between, static_kb=parse_theory("small(X) :- py_between(1, 3, X).")
    )
    assert bindings(solve_all(solver, "small(X)"), "X") == ["1", "2", "3"]


def test_primitive_can_bind_complex_terms():
    def listing(request):
        yield request.reply_success(
            unifier({request.arguments[0]: logic_list(integer(1), integer(2))})
        )

    solver = solver_with_primitive("listing", 1, listing)
    assert bindings(solve_all(solver, "listing(L)"), "L") == ["[1, 2]"]


def test_primitive_closures_keep_python_state():
    counter = {"n": 0}

    def tick(request):
        counter["n"] += 1
        yield request.reply_with(mgu(request.arguments[0], integer(counter["n"])))

    solver = solver_with_primitive("tick", 1, tick)
    assert [bindings(solve_all(solver, "tick(X)"), "X") for _ in range(3)] == [["1"], ["2"], ["3"]]


def test_python_exceptions_become_logic_errors():
    def broken(request):
        raise ValueError("boom")

    solver = solver_with_primitive("broken", 0, broken)
    [solution] = solve_all(solver, "broken")
    assert solution.is_halt
    with pytest.raises(RuntimeError, match="boom"):  # a system_error
        solution.raise_error()


def test_python_exceptions_raised_lazily_become_logic_errors():
    def broken(request):
        yield request.reply_success()
        raise ValueError("late")

    solver = solver_with_primitive("broken", 0, broken)
    solutions = solve_all(solver, "broken")
    assert [s.is_yes for s in solutions] == [True, False]
    assert solutions[1].is_halt


def test_primitive_can_use_sub_solvers():
    def count_solutions(request):
        goal = request.arguments[0]
        n = sum(1 for s in request.solve(goal) if s.is_yes)
        yield request.reply_with(mgu(request.arguments[1], integer(n)))

    solver = solver_with_primitive(
        "count", 2, count_solutions, static_kb=parse_theory("p(1). p(2). p(3).")
    )
    assert bindings(solve_all(solver, "count(p(_), N)"), "N") == ["3"]


@pytest.mark.parametrize("effects", [lambda: (), lambda: (set_flags(unknown=atom("fail")),)])
def test_solve_response(effects):
    def respond(request):
        from tuprolog.solve import yes_solution

        yield solve_response(yes_solution(request.query), *effects())

    solver = solver_with_primitive("respond", 0, respond)
    assert solve_all(solver, "respond")[0].is_yes


def test_solve_response_side_effects_are_applied():
    def respond(request):
        from tuprolog.solve import yes_solution

        effects = [set_flags(unknown=Unknown.ERROR), add_dynamic_clauses(*parse_theory("q(1)."))]
        yield solve_response(yes_solution(request.query), effects)

    solver = solver_with_primitive("respond", 0, respond)
    assert bindings(solve_all(solver, "respond, q(X)"), "X") == ["1"]
    assert solver.flags[Unknown] == Unknown.ERROR


def test_solve_response_fields():
    from tuprolog.core import atom
    from tuprolog.solve import no_solution

    effect = set_flags(a=atom("b"))
    response = solve_response(no_solution(atom("q")), effect)
    assert isinstance(response, SolveResponse)
    assert response.solution.is_no
    assert list(response.side_effects) == [effect]
    assert list(solve_response(no_solution(atom("q"))).side_effects) == []
