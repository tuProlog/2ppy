

import pytest

from tuprolog.core import atom, fact, struct, var
from tuprolog.solve import ALL_SOLUTIONS, MAX_TIMEOUT, solve_options
from tuprolog.solve.prolog import prolog_solver
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


Q_A = fact(struct("q", atom("a")))


Q_B = fact(struct("q", atom("b")))


Q_X = struct("q", X)


