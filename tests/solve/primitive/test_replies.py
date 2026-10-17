"""Replies of primitives implemented in Python, checked end to end through a solver."""

import pytest

from tests.solve.primitive._support import (
    RequestCapturer,
    bindings,
    error_of,
    solve_all,
    solver_with_primitive,
)
from tuprolog.core import atom, failed, integer, struct, unifier, var
from tuprolog.solve import halt_solution, no_solution, yes_solution
from tuprolog.solve.exception.error import TypeError
from tuprolog.solve.flags import Unknown
from tuprolog.solve.primitive import SolveResponse, ensuring_argument_is_integer
from tuprolog.solve.sideffects import set_flags
from tuprolog.unify import mgu


@pytest.fixture(scope="module")
def capturer() -> RequestCapturer:
    return RequestCapturer()


def _type_error(request) -> TypeError:
    try:
        ensuring_argument_is_integer(request, 0)
    except TypeError as error:
        return error
    raise AssertionError("expected a type error")


def _bind_first_to(value):
    def implementation(request):
        yield request.reply_success(unifier({request.arguments[0]: value}))

    return implementation


def test_reply_success_without_arguments():
    solver = solver_with_primitive("p", 0, lambda r: [r.reply_success()])
    solutions = solve_all(solver, "p")
    assert len(solutions) == 1 and solutions[0].is_yes
    assert solutions[0].substitution.is_empty


def test_reply_success_with_unifier():
    solver = solver_with_primitive("p", 1, _bind_first_to(atom("a")))
    assert bindings(solve_all(solver, "p(X)"), "X") == ["a"]


def test_reply_success_with_none_substitution_and_side_effects():
    solver = solver_with_primitive(
        "p", 0, lambda r: [r.reply_success(None, set_flags(unknown=Unknown.ERROR))]
    )
    assert solve_all(solver, "p")[0].is_yes
    assert solver.flags[Unknown] == Unknown.ERROR


def test_reply_with_substitution():
    def implementation(request):
        yield request.reply_with(mgu(request.arguments[0], integer(1)))

    solver = solver_with_primitive("p", 1, implementation)
    assert bindings(solve_all(solver, "p(X)"), "X") == ["1"]
    assert solve_all(solver, "p(2)")[0].is_no


def test_reply_with_failed_substitution_fails():
    solver = solver_with_primitive("p", 0, lambda r: [r.reply_with(failed())])
    assert solve_all(solver, "p")[0].is_no


@pytest.mark.parametrize("condition, outcome", [(True, "is_yes"), (False, "is_no")])
def test_reply_with_condition(condition, outcome):
    solver = solver_with_primitive("p", 0, lambda r: [r.reply_with(condition)])
    assert getattr(solve_all(solver, "p")[0], outcome)


def test_reply_with_solutions():
    def implementation(request):
        query = request.query
        x = request.arguments[0]
        yield request.reply_with(yes_solution(query, unifier({x: integer(1)})))
        yield request.reply_with(no_solution(query))

    solver = solver_with_primitive("p", 1, implementation)
    solutions = solve_all(solver, "p(X)")
    assert bindings(solutions[:1], "X") == ["1"]
    assert solutions[1].is_no


def test_reply_with_halt_solution():
    def implementation(request):
        error = _type_error(request)
        yield request.reply_with(halt_solution(request.query, error))

    solver = solver_with_primitive("p", 1, implementation)
    error = error_of(solve_all(solver, "p(a)")[0])
    assert str(error.get_arg_at(0)) == "type_error(integer, a)"


def test_reply_with_side_effects():
    solver = solver_with_primitive(
        "p", 0, lambda r: [r.reply_with(True, set_flags(unknown=Unknown.FAIL))]
    )
    assert solve_all(solver, "p")[0].is_yes
    assert solver.flags[Unknown] == Unknown.FAIL


def test_reply_fail_without_arguments():
    solver = solver_with_primitive("p", 0, lambda r: [r.reply_fail()])
    assert solve_all(solver, "p")[0].is_no


def test_reply_fail_with_side_effects():
    solver = solver_with_primitive(
        "p", 0, lambda r: [r.reply_fail(set_flags(unknown=Unknown.ERROR))]
    )
    assert solve_all(solver, "p")[0].is_no


def test_reply_exception_is_catchable():
    def implementation(request):
        error = _type_error(request)
        yield request.reply_exception(error)

    solver = solver_with_primitive("p", 1, implementation)
    assert error_of(solve_all(solver, "p(a)")[0]) is not None
    caught = solve_all(solver, "catch(p(a), error(type_error(T, C), _), true)")
    assert bindings(caught, "T") == ["integer"]
    assert bindings(caught, "C") == ["a"]


def test_reply_exception_with_side_effects():
    def implementation(request):
        error = _type_error(request)
        yield request.reply_exception(error, set_flags(unknown=Unknown.FAIL))

    solver = solver_with_primitive("p", 1, implementation)
    assert solve_all(solver, "p(a)")[0].is_halt


@pytest.mark.parametrize(
    "reply",
    [
        lambda r: r.reply_success(),
        lambda r: r.reply_fail(),
        lambda r: r.reply_with(True),
        lambda r: r.reply_success(None, set_flags(a=atom("b"))),
    ],
)
def test_replies_are_responses_to_the_request(capturer, reply):
    request = capturer.request(struct("f", var("X")))
    response = reply(request)
    assert isinstance(response, SolveResponse)
    assert response.solution.query == request.query
    assert response.side_effect_manager is None


def test_reply_side_effects_are_recorded(capturer):
    request = capturer.request()
    effect = set_flags(a=atom("b"))
    for response in [
        request.reply_success(None, effect),
        request.reply_fail(effect),
        request.reply_with(False, effect),
    ]:
        assert list(response.side_effects) == [effect]
