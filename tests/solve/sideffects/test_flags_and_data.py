"""Side effects altering flags and custom data: factories and their effect on solvers."""

import pytest

from tests.solve.primitive._support import bindings, error_of, solve_all
from tuprolog.core import atom, integer
from tuprolog.solve.flags import DEFAULT_FLAG_STORE, MaxArity, Unknown
from tuprolog.solve.sideffects import (
    ClearFlags,
    ResetFlags,
    SetDurableData,
    SetEphemeralData,
    SetFlags,
    SetPersistentData,
    clear_flags,
    reset_durable_data,
    reset_ephemeral_data,
    reset_flags,
    reset_persistent_data,
    set_durable_data,
    set_ephemeral_data,
    set_flags,
    set_persistent_data,
)


def as_dict(mapping) -> dict[str, str]:
    return {str(k): str(mapping[k]) for k in mapping}


@pytest.mark.parametrize("factory, kind", [(set_flags, SetFlags), (reset_flags, ResetFlags)])
def test_flag_factories(factory, kind):
    assert isinstance(factory(), kind)
    assert as_dict(factory().flags) == {}
    assert as_dict(factory({"a": atom("x")}).flags) == {"a": "x"}
    assert as_dict(factory(a=atom("x")).flags) == {"a": "x"}
    assert as_dict(factory({"a": atom("x"), "b": atom("y")}, b=atom("z")).flags) == {
        "a": "x",
        "b": "z",
    }


@pytest.mark.parametrize(
    "arguments, expected",
    [
        (lambda: (), []),
        (lambda: ("unknown", "max_arity"), ["unknown", "max_arity"]),
        (lambda: (["unknown", "max_arity"],), ["unknown", "max_arity"]),
        (lambda: (iter(["unknown"]),), ["unknown"]),
    ],
    ids=["none", "many", "list", "iterator"],
)
def test_clear_flags_factory(arguments, expected):
    effect = clear_flags(*arguments())
    assert isinstance(effect, ClearFlags)
    assert [str(n) for n in effect.names] == expected


@pytest.mark.xfail(
    strict=True,
    reason="iterable_or_varargs (tuprolog/pyutils.py) unpacks a single string into characters",
)
def test_clear_flags_with_single_name():
    assert [str(n) for n in clear_flags("unknown").names] == ["unknown"]


def test_set_flags_end_to_end(emitting):
    solver = emitting(set_flags(unknown=Unknown.ERROR, custom=atom("v")))
    solutions = solve_all(
        solver, "emit, current_prolog_flag(unknown, U), current_prolog_flag(custom, C)"
    )
    assert bindings(solutions, "U") == ["error"]
    assert bindings(solutions, "C") == ["v"]
    assert solver.flags[Unknown] == Unknown.ERROR
    assert str(error_of(solve_all(solver, "undefined")[0]).get_arg_at(0)).startswith(
        "existence_error"
    )


def test_set_flags_keeps_other_flags(emitting):
    solver = emitting(set_flags(custom=atom("v")))
    solve_all(solver, "emit")
    assert solver.flags[MaxArity] == DEFAULT_FLAG_STORE[MaxArity]


def test_reset_flags_end_to_end(emitting):
    solver = emitting(reset_flags(custom=atom("v")))
    solve_all(solver, "emit")
    assert as_dict(solver.flags) == {"custom": "v"}


def test_clear_flags_end_to_end(emitting):
    solver = emitting(clear_flags("unknown", "max_arity"))
    solve_all(solver, "emit")
    assert "unknown" not in solver.flags
    assert "max_arity" not in solver.flags
    assert "double_quotes" in solver.flags


DATA_FACTORIES = [
    (set_persistent_data, SetPersistentData, False),
    (reset_persistent_data, SetPersistentData, True),
    (set_durable_data, SetDurableData, False),
    (reset_durable_data, SetDurableData, True),
    (set_ephemeral_data, SetEphemeralData, False),
    (reset_ephemeral_data, SetEphemeralData, True),
]


@pytest.mark.parametrize("factory, kind, reset", DATA_FACTORIES)
def test_data_factories(factory, kind, reset):
    for effect in [factory(), factory({"k": atom("v")}), factory(k=atom("v"))]:
        assert isinstance(effect, kind)
        assert effect.reset is reset
    assert as_dict(factory({"k": atom("v")}, j=integer(1)).data) == {"k": "v", "j": "1"}
    assert as_dict(factory({"k": atom("v")}, k=atom("w")).data) == {"k": "w"}


@pytest.mark.parametrize(
    "factory, getter, survives",
    [
        (set_persistent_data, "get_persistent", True),
        (set_durable_data, "get_durable", False),
        (set_ephemeral_data, "get_ephemeral", False),
    ],
)
def test_data_end_to_end(emitting, factory, getter, survives):
    solver = emitting(factory(key=atom("value")))
    assert bindings(solve_all(solver, f"emit, {getter}(key, X)"), "X") == ["value"]
    later = solve_all(solver, f"{getter}(key, X)")[0]
    assert later.is_yes is survives


def test_reset_persistent_data_drops_other_keys(emitting):
    def solver_emitting(*effects):
        return emitting(*effects)

    solver = solver_emitting(set_persistent_data(a=atom("x")), reset_persistent_data(b=atom("y")))
    solve_all(solver, "emit")
    assert solve_all(solver, "get_persistent(a, X)")[0].is_no
    assert bindings(solve_all(solver, "get_persistent(b, X)"), "X") == ["y"]


def test_set_persistent_data_merges_keys(emitting):
    solver = emitting(set_persistent_data(a=atom("x")), set_persistent_data(b=atom("y")))
    solve_all(solver, "emit")
    assert bindings(solve_all(solver, "get_persistent(a, X)"), "X") == ["x"]
    assert bindings(solve_all(solver, "get_persistent(b, X)"), "X") == ["y"]
