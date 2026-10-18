"""Flag stores given to solvers, and their effect on resolution."""

import pytest

from tests.solve.primitive._support import bindings, error_of, solve_all, solver_with_primitive
from tuprolog.core import atom
from tuprolog.solve.channel import output_channel
from tuprolog.solve.flags import DEFAULT_FLAG_STORE, Unknown, flag_store
from tuprolog.solve.prolog import prolog_solver


def unknown_solver(value, warnings=None):
    return prolog_solver(
        flags=flag_store(DEFAULT_FLAG_STORE, unknown=value),
        warning=output_channel((warnings if warnings is not None else []).append),
    )


def test_solver_exposes_its_flags():
    solver = prolog_solver(flags=flag_store(DEFAULT_FLAG_STORE, custom=atom("v")))
    assert solver.flags["custom"] == atom("v")
    assert bindings(solve_all(solver, "current_prolog_flag(custom, X)"), "X") == ["v"]


def test_unknown_error_raises_existence_errors():
    error = error_of(solve_all(unknown_solver(Unknown.ERROR), "undefined_pred(1)")[0])
    culprit = error.get_arg_at(0)
    assert culprit.functor == "existence_error"
    assert str(culprit.get_arg_at(0)) == "procedure"
    assert "undefined_pred" in str(culprit.get_arg_at(1))


def test_unknown_warning_fails_and_warns():
    warnings: list = []
    assert solve_all(unknown_solver(Unknown.WARNING, warnings), "undefined_pred")[0].is_no
    assert len(warnings) == 1


def test_unknown_fail_fails_silently():
    warnings: list = []
    assert solve_all(unknown_solver(Unknown.FAIL, warnings), "undefined_pred")[0].is_no
    assert warnings == []


@pytest.mark.parametrize("value", ["error", "warning", "fail"])
def test_set_prolog_flag_changes_resolution(value):
    solver = unknown_solver(Unknown.FAIL)
    assert solve_all(solver, f"set_prolog_flag(unknown, {value})")[0].is_yes
    assert str(solver.flags[Unknown]) == value


def test_set_prolog_flag_rejects_inadmissible_values():
    solver = prolog_solver()
    assert solve_all(solver, "set_prolog_flag(unknown, bogus)")[0].is_halt


def test_flags_are_visible_to_primitives():
    def read_flag(request):
        yield request.reply_with(request.context.flags[Unknown] == Unknown.FAIL)

    solver = solver_with_primitive(
        "unknown_is_fail", 0, read_flag, flags=flag_store(DEFAULT_FLAG_STORE, unknown=Unknown.FAIL)
    )
    assert solve_all(solver, "unknown_is_fail")[0].is_yes


def test_solver_flags_given_to_factory_are_not_mutated():
    store = flag_store(DEFAULT_FLAG_STORE)
    solver = prolog_solver(flags=store)
    solve_all(solver, "set_prolog_flag(unknown, fail)")
    assert store[Unknown] == Unknown.WARNING
