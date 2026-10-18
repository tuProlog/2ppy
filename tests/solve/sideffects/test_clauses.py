"""Side effects altering the knowledge bases: factories and their effect on solvers."""

import pytest

from tests.solve.primitive._support import bindings, solve_all
from tuprolog.core import Clause, fact, integer, struct
from tuprolog.solve.sideffects import (
    AddDynamicClauses,
    AddStaticClauses,
    RemoveDynamicClauses,
    RemoveStaticClauses,
    ResetDynamicKb,
    ResetStaticKb,
    SideEffect,
    add_dynamic_clauses,
    add_static_clauses,
    remove_dynamic_clauses,
    remove_static_clauses,
    reset_dynamic_kb,
    reset_static_kb,
)
from tuprolog.theory import mutable_theory, theory


def f(n: int) -> Clause:
    return fact(struct("f", integer(n)))


F1, F2, F3 = f(1), f(2), f(3)

FACTORIES = [
    (reset_static_kb, ResetStaticKb),
    (add_static_clauses, AddStaticClauses),
    (remove_static_clauses, RemoveStaticClauses),
    (reset_dynamic_kb, ResetDynamicKb),
    (add_dynamic_clauses, AddDynamicClauses),
    (remove_dynamic_clauses, RemoveDynamicClauses),
]


@pytest.mark.parametrize("factory, kind", FACTORIES)
@pytest.mark.parametrize(
    "arguments, expected",
    [
        (lambda: (), []),
        (lambda: (F1,), [F1]),
        (lambda: (F1, F2), [F1, F2]),
        (lambda: ([F1, F2],), [F1, F2]),
        (lambda: ((F1, F2),), [F1, F2]),
        (lambda: (iter([F1, F2]),), [F1, F2]),
        (lambda: (theory(F1, F2),), [F1, F2]),
    ],
    ids=["none", "one", "many", "list", "tuple", "iterator", "theory"],
)
def test_clause_side_effect_factories(factory, kind, arguments, expected):
    effect = factory(*arguments())
    assert isinstance(effect, kind)
    assert isinstance(effect, SideEffect)
    assert list(effect.clauses) == expected


@pytest.mark.parametrize("factory", [add_static_clauses, add_dynamic_clauses])
def test_add_clauses_defaults_to_appending(factory):
    assert factory(F1).on_top is False


@pytest.mark.parametrize("factory", [add_static_clauses, add_dynamic_clauses])
@pytest.mark.parametrize("on_top", [True, False])
def test_add_clauses_on_top(factory, on_top):
    assert factory(F1, F2, on_top=on_top).on_top is on_top
    assert factory([F1, F2], on_top=on_top).on_top is on_top


def _values(solver, goal="emit, f(X)"):
    return bindings(solve_all(solver, goal), "X")


def test_add_static_clauses_appends(emitting):
    solver = emitting(add_static_clauses(F2, F3), static_kb=theory(F1))
    assert _values(solver) == ["1", "2", "3"]
    assert list(solver.static_kb) == [F1, F2, F3]


def test_add_static_clauses_on_top(emitting):
    solver = emitting(add_static_clauses(F2, F3, on_top=True), static_kb=theory(F1))
    assert _values(solver) == ["2", "3", "1"]


def test_add_dynamic_clauses_appends(emitting):
    solver = emitting(add_dynamic_clauses([F2, F3]), dynamic_kb=mutable_theory(F1))
    assert _values(solver) == ["1", "2", "3"]
    assert list(solver.dynamic_kb) == [F1, F2, F3]


def test_add_dynamic_clauses_on_top(emitting):
    solver = emitting(add_dynamic_clauses([F2, F3], on_top=True), dynamic_kb=mutable_theory(F1))
    assert _values(solver) == ["2", "3", "1"]


def test_added_dynamic_clauses_can_be_retracted(emitting):
    solver = emitting(add_dynamic_clauses(F1, F2))
    assert solve_all(solver, "emit")[0].is_yes
    assert solve_all(solver, "retract(f(1))")[0].is_yes
    assert _values(solver, "f(X)") == ["2"]


def test_reset_static_kb(emitting):
    solver = emitting(reset_static_kb(F3), static_kb=theory(F1, F2))
    assert _values(solver) == ["3"]
    assert list(solver.static_kb) == [F3]


def test_reset_static_kb_to_empty(emitting):
    solver = emitting(reset_static_kb(), static_kb=theory(F1, F2))
    assert solve_all(solver, "emit")[0].is_yes
    assert list(solver.static_kb) == []


def test_reset_dynamic_kb(emitting):
    solver = emitting(reset_dynamic_kb([F3]), dynamic_kb=mutable_theory(F1, F2))
    assert _values(solver) == ["3"]
    assert list(solver.dynamic_kb) == [F3]


def test_remove_static_clauses(emitting):
    solver = emitting(remove_static_clauses(F1, F3), static_kb=theory(F1, F2, F3))
    assert _values(solver) == ["2"]


def test_remove_dynamic_clauses(emitting):
    solver = emitting(remove_dynamic_clauses([F2]), dynamic_kb=mutable_theory(F1, F2))
    assert _values(solver) == ["1"]


def test_removing_missing_clauses_is_harmless(emitting):
    solver = emitting(remove_static_clauses(F3), static_kb=theory(F1))
    assert _values(solver) == ["1"]


def test_side_effects_of_later_solutions_accumulate(emitting):
    solver = emitting(add_dynamic_clauses(F1))
    for _ in range(3):
        assert solve_all(solver, "emit")[0].is_yes
    assert _values(solver, "f(X)") == ["1", "1", "1"]


def test_side_effects_are_applied_in_order(emitting):
    solver = emitting(reset_dynamic_kb(F1), add_dynamic_clauses(F2), remove_dynamic_clauses(F1))
    assert _values(solver) == ["2"]


def test_static_kb_given_to_solver_is_not_modified(emitting):
    original = theory(F1)
    solver = emitting(add_static_clauses(F2), static_kb=original)
    assert _values(solver) == ["1", "2"]
    assert list(original) == [F1]
