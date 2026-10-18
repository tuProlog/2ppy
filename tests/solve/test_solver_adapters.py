from collections.abc import Iterable

import pytest

from tuprolog.core import atom, fact, integer, struct, var
from tuprolog.core.parsing import parse_struct
from tuprolog.jvmutils import Sequence
from tuprolog.solve import (
    ALL_SOLUTIONS,
    MAX_TIMEOUT,
    MutableSolver,
    Solution,
    Solver,
    solve_options,
)
from tuprolog.solve.channel import output_channel
from tuprolog.solve.prolog import prolog_solver
from tuprolog.theory import theory
from tuprolog.theory.parsing import parse_theory

X = var("X")
P_X = struct("p", X)


def values(solutions, variable=X):
    return [str(s.substitution[variable]) for s in solutions if s.is_yes]


@pytest.fixture
def solver():
    return prolog_solver(static_kb=parse_theory("p(1). p(2). p(3)."))


@pytest.fixture
def immutable_solver():
    return prolog_solver(static_kb=parse_theory("p(1). p(2). p(3)."), mutable=False)


# --- SolveOptions mapping protocol -------------------------------------------------------------

STATIC_KEYS = {"lazy", "is_lazy", "eager", "is_eager", "timeout", "limit"}


def test_solve_options_properties():
    opts = solve_options(lazy=False, timeout=10, limit=2, custom={"k": "v"})
    assert opts.is_lazy is False
    assert opts.is_eager is True
    assert opts.timeout == 10
    assert opts.limit == 2
    assert opts.options["k"] == "v"


@pytest.mark.parametrize(
    "key, expected",
    [
        ("lazy", False),
        ("is_lazy", False),
        ("eager", True),
        ("is_eager", True),
        ("timeout", 10),
        ("limit", 2),
        ("k", "v"),
    ],
)
def test_solve_options_getitem(key, expected):
    opts = solve_options(lazy=False, timeout=10, limit=2, custom={"k": "v"})
    assert opts[key] == expected


def test_solve_options_getitem_missing_key():
    with pytest.raises(KeyError, match="No such option: missing"):
        solve_options()["missing"]


def test_solve_options_contains():
    opts = solve_options(custom={"k": "v"})
    for key in STATIC_KEYS | {"k"}:
        assert key in opts
    assert "missing" not in opts
    assert 1 not in opts


def test_solve_options_len_matches_iteration():
    assert len(solve_options()) == len(list(solve_options())) == len(STATIC_KEYS)
    opts = solve_options(custom={"a": 1, "b": 2})
    assert len(opts) == len(list(opts)) == len(STATIC_KEYS) + 2


def test_solve_options_iteration_yields_python_strings():
    keys = list(solve_options(custom={"a": 1}))
    assert set(keys) == STATIC_KEYS | {"a"}
    assert all(type(k) is str for k in keys)


def test_solve_options_get():
    opts = solve_options(limit=4, custom={"k": "v"})
    assert opts.get("limit") == 4
    assert opts.get("k") == "v"
    assert opts.get("missing") is None
    assert opts.get("missing", 42) == 42


def test_solve_options_keys_values_items():
    opts = solve_options(lazy=True, timeout=7, limit=1, custom={"k": "v"})
    assert set(opts.keys()) == STATIC_KEYS | {"k"}
    assert dict(opts.items())["timeout"] == 7
    assert len(opts.values()) == len(opts)


def test_solve_options_to_dict():
    opts = dict(solve_options(lazy=False, timeout=7, limit=1, custom={"k": "v"}))
    assert opts == {
        "lazy": False,
        "is_lazy": False,
        "eager": True,
        "is_eager": True,
        "timeout": 7,
        "limit": 1,
        "k": "v",
    }


def test_solve_options_defaults_in_mapping():
    opts = dict(solve_options())
    assert opts["timeout"] == MAX_TIMEOUT
    assert opts["limit"] == ALL_SOLUTIONS


# --- Solver.solve / solve_once -----------------------------------------------------------------


def test_solver_types(solver, immutable_solver):
    assert isinstance(solver, MutableSolver)
    assert isinstance(immutable_solver, Solver)
    assert not isinstance(immutable_solver, MutableSolver)


def test_solve_is_lazy_by_default(solver):
    solutions = solver.solve(P_X)
    assert isinstance(solutions, Sequence)
    assert isinstance(solutions, Iterable)
    assert values(solutions) == ["1", "2", "3"]


def test_solve_lazy_sequence_can_be_consumed_once(solver):
    solutions = solver.solve(P_X)
    assert len(list(solutions)) == 3
    with pytest.raises(Exception, match="only once"):
        list(solutions)


def test_solve_with_lazy_options(solver):
    solutions = solver.solve(P_X, solve_options(lazy=True))
    assert values(solutions) == ["1", "2", "3"]


def test_solve_with_eager_options_returns_a_list(solver):
    solutions = solver.solve(P_X, solve_options(lazy=False))
    assert isinstance(solutions, list)
    assert values(solutions) == ["1", "2", "3"]


def test_solve_with_eager_options_still_yields_all_solutions(solver):
    assert values(solver.solve(P_X, solve_options(lazy=False))) == ["1", "2", "3"]


def test_solve_list(solver):
    solutions = solver.solve_list(P_X)
    assert len(solutions) == 3
    assert values(solutions) == ["1", "2", "3"]


@pytest.mark.parametrize("limit, expected", [(1, ["1"]), (2, ["1", "2"]), (10, ["1", "2", "3"])])
def test_solve_with_limit(solver, limit, expected):
    assert values(solver.solve(P_X, solve_options(limit=limit))) == expected


def test_solve_accepts_options_as_keyword(solver):
    assert values(solver.solve(P_X, options=solve_options(limit=1))) == ["1"]


def test_solve_accepts_python_strings(solver):
    assert [s.to_dict() for s in solver.solve("p(X)")] == [s.to_dict() for s in solver.solve(P_X)]
    assert solver.solve_once("p(X)").is_yes


def test_solve_once(solver):
    sol = solver.solve_once(P_X)
    assert isinstance(sol, Solution)
    assert sol.is_yes
    assert sol.solved_query == struct("p", integer(1))


def test_solve_once_with_options(solver):
    sol = solver.solve_once(P_X, solve_options(timeout=10_000))
    assert sol.solved_query == struct("p", integer(1))


def test_solve_once_no(solver):
    assert solver.solve_once(struct("p", integer(4))).is_no


def test_immutable_solver_solves_too(immutable_solver):
    assert values(immutable_solver.solve(P_X)) == ["1", "2", "3"]
    assert immutable_solver.solve_once(P_X).is_yes


# --- MutableSolver -----------------------------------------------------------------------------

Q_A = fact(struct("q", atom("a")))
Q_B = fact(struct("q", atom("b")))
Q_X = struct("q", X)


@pytest.mark.parametrize(
    "make_args",
    [
        pytest.param(lambda: (Q_A, Q_B), id="varargs"),
        pytest.param(lambda: ([Q_A, Q_B],), id="list"),
        pytest.param(lambda: ((c for c in [Q_A, Q_B]),), id="generator"),
        pytest.param(lambda: (theory(Q_A, Q_B),), id="theory"),
    ],
)
@pytest.mark.parametrize("kind", ["static", "dynamic"])
def test_load_clauses(solver, kind, make_args):
    getattr(solver, f"load_{kind}_clauses")(*make_args())
    assert list(getattr(solver, f"{kind}_kb")) == [Q_A, Q_B]
    assert values(solver.solve(Q_X)) == ["a", "b"]


@pytest.mark.parametrize("kind", ["static", "dynamic"])
def test_load_single_clause(solver, kind):
    getattr(solver, f"load_{kind}_clauses")(Q_A)
    assert list(getattr(solver, f"{kind}_kb")) == [Q_A]


def test_load_static_clauses_replaces_the_static_kb(solver):
    solver.load_static_clauses(Q_A)
    assert solver.solve_once(P_X).is_no
    assert values(solver.solve(Q_X)) == ["a"]


def test_load_dynamic_clauses_are_retractable(solver):
    solver.load_dynamic_clauses(Q_A, Q_B)
    assert solver.solve_once(parse_struct("retract(q(a))")).is_yes
    assert values(solver.solve(Q_X)) == ["b"]


def test_immutable_solver_has_no_loaders(immutable_solver):
    assert not hasattr(immutable_solver, "load_static_clauses")
    assert not hasattr(immutable_solver, "load_dynamic_clauses")


def test_kb_management(solver):
    solver.load_static_kb(parse_theory("k(1)."))
    solver.append_static_kb(parse_theory("k(2)."))
    assert values(solver.solve(struct("k", X))) == ["1", "2"]
    solver.reset_static_kb()
    assert len(solver.static_kb) == 0
    solver.load_dynamic_kb(parse_theory("d(1)."))
    solver.append_dynamic_kb(parse_theory("d(2)."))
    assert values(solver.solve(struct("d", X))) == ["1", "2"]
    solver.reset_dynamic_kb()
    assert len(solver.dynamic_kb) == 0


def test_java_assert_and_retract_methods(solver):
    solver.assertZ(Q_B)
    solver.assertA(Q_A)
    assert list(solver.dynamic_kb) == [Q_A, Q_B]
    assert solver.retract(Q_A).is_success
    assert solver.retract_all(fact(struct("q", var("_")))).is_success
    assert len(solver.dynamic_kb) == 0


def test_snake_case_assert_methods(solver):
    solver.assert_z(Q_B)
    solver.assert_a(Q_A)
    assert list(solver.dynamic_kb) == [Q_A, Q_B]


def test_channel_properties(solver):
    for name in ("standard_output", "standard_input", "standard_error", "warnings"):
        assert getattr(solver, name) is not None


def test_channel_setters_via_java_methods(solver):
    warnings = []
    channel = output_channel(lambda w: warnings.append(w))
    solver.set_warnings(channel)
    assert solver.warnings == channel
    solver.solve_once(struct("undefined", integer(1)))
    assert len(warnings) == 1
    assert "undefined/1" in str(warnings[0])


_IGNORED_SETTER = pytest.mark.xfail(
    strict=True,
    reason="2P-Kt 3.0.1: MutableSolver.setStandardOutput/setStandardError have no effect "
    "(the getters keep returning the old channel)",
)


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("standard_output", marks=_IGNORED_SETTER),
        pytest.param("standard_error", marks=_IGNORED_SETTER),
        "warnings",
    ],
)
def test_channel_property_setters(solver, name):
    channel = output_channel(lambda _: None)
    setattr(solver, name, channel)
    assert getattr(solver, name) == channel


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt 3.0.1: MutableSolver.setStandardOutput replaces the 'stdout' alias only, "
    "while write/1 keeps using the old '$current'/'user_output' channel",
)
def test_set_standard_output_redirects_write(solver):
    out = []
    solver.set_standard_output(output_channel(lambda m: out.append(str(m))))
    solver.solve_once(parse_struct("write(hello)"))
    assert out == ["hello"]


def test_set_flag(solver):
    solver.set_flag("unknown", atom("error"))
    halt = solver.solve_once(struct("undefined", integer(1)))
    assert halt.is_halt
    assert "existence_error" in str(halt.get_exception().error_struct)


def test_clone(solver):
    clone = solver.clone()
    clone.load_static_clauses(Q_A)
    assert values(solver.solve(P_X)) == ["1", "2", "3"]
    assert values(clone.solve(Q_X)) == ["a"]
    assert isinstance(clone, MutableSolver)
