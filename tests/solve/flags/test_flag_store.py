"""Python protocols of FlagStore, and the notable flags re-exported by tuprolog.solve.flags."""

import pytest
from jpype import JException

from tuprolog.core import atom, integer
from tuprolog.jvmutils import jmap
from tuprolog.solve.flags import (
    DEFAULT_FLAG_STORE,
    EMPTY_FLAG_STORE,
    DoubleQuotes,
    FlagStore,
    GroundQueriesHaveBooleanSolution,
    LastCallOptimization,
    MaxArity,
    NotableFlag,
    ShowWildCardVariablesInSolutions,
    TrackVariables,
    UniqueSolutions,
    Unknown,
    flag,
)

NOTABLE_FLAGS = [
    DoubleQuotes,
    GroundQueriesHaveBooleanSolution,
    LastCallOptimization,
    MaxArity,
    ShowWildCardVariablesInSolutions,
    TrackVariables,
    UniqueSolutions,
    Unknown,
]


def test_empty_flag_store():
    assert len(EMPTY_FLAG_STORE) == 0
    assert EMPTY_FLAG_STORE == FlagStore.empty()
    assert list(EMPTY_FLAG_STORE) == []


def test_default_flag_store_holds_every_notable_flag_with_its_default():
    assert len(DEFAULT_FLAG_STORE) == len(NOTABLE_FLAGS)
    for notable in NOTABLE_FLAGS:
        assert DEFAULT_FLAG_STORE[notable] == notable.default_value
        assert DEFAULT_FLAG_STORE[notable.name] == notable.default_value


@pytest.mark.parametrize("notable", NOTABLE_FLAGS, ids=lambda f: str(f.name))
def test_notable_flags(notable):
    assert isinstance(notable, NotableFlag)
    assert notable.is_admissible_value(notable.default_value)
    assert notable.default_value in list(notable.admissible_values) or notable is MaxArity


@pytest.mark.parametrize(
    "notable, names",
    [
        (Unknown, ["ERROR", "WARNING", "FAIL"]),
        (TrackVariables, ["ON", "OFF"]),
        (LastCallOptimization, ["ON", "OFF"]),
        (DoubleQuotes, ["ATOM"]),
        (GroundQueriesHaveBooleanSolution, ["ON", "OFF"]),
        (ShowWildCardVariablesInSolutions, ["ON", "OFF"]),
        (UniqueSolutions, ["ON", "OFF"]),
    ],
    ids=[
        "unknown",
        "track_variables",
        "last_call_optimization",
        "double_quotes",
        "ground_queries_have_boolean_solution",
        "show_wildcard_variables_in_solutions",
        "unique_solutions",
    ],
)
def test_notable_flag_admissible_values(notable, names):
    values = [getattr(notable, name) for name in names]
    assert {str(v) for v in notable.admissible_values} == {str(v) for v in values}
    for value in values:
        assert notable.is_admissible_value(value)
    assert not notable.is_admissible_value(atom("definitely_not_admissible"))


def test_notable_flag_editability():
    assert Unknown.is_editable
    assert not MaxArity.is_editable


@pytest.mark.parametrize("notable", NOTABLE_FLAGS, ids=lambda f: str(f.name))
def test_notable_flag_from_name(notable):
    assert NotableFlag.fromName(notable.name) == notable


def test_from_name_of_unknown_flag_is_none():
    assert NotableFlag.fromName("no_such_flag") is None


def test_len():
    assert len(DEFAULT_FLAG_STORE + flag("a", atom("b"))) == len(NOTABLE_FLAGS) + 1


def test_getitem_by_notable_flag_or_name():
    store = DEFAULT_FLAG_STORE.set(Unknown, Unknown.FAIL)
    assert store[Unknown] == Unknown.FAIL
    assert store["unknown"] == Unknown.FAIL


def test_getitem_of_missing_flag_raises_key_error():
    with pytest.raises(KeyError, match="missing"):
        EMPTY_FLAG_STORE["missing"]
    with pytest.raises(KeyError, match="unknown"):
        EMPTY_FLAG_STORE[Unknown]


def test_iteration_yields_flag_names():
    assert {str(name) for name in DEFAULT_FLAG_STORE} == {f.name for f in NOTABLE_FLAGS}


def test_contains_flag_names():
    assert "unknown" in DEFAULT_FLAG_STORE
    assert "missing" not in DEFAULT_FLAG_STORE


def test_contains_notable_flags():
    for notable in NOTABLE_FLAGS:
        assert notable in DEFAULT_FLAG_STORE
        assert notable not in EMPTY_FLAG_STORE
    assert Unknown not in DEFAULT_FLAG_STORE - Unknown


def test_add_notable_flag_sets_its_default():
    assert (EMPTY_FLAG_STORE + Unknown)[Unknown] == Unknown.WARNING


@pytest.mark.parametrize(
    "pair",
    [flag("a", atom("b")), ("a", atom("b")), ["a", atom("b")]],
    ids=["pair", "tuple", "list"],
)
def test_add_pair(pair):
    assert (EMPTY_FLAG_STORE + pair)["a"] == atom("b")


def test_add_dict():
    store = EMPTY_FLAG_STORE + {"a": atom("b"), "c": integer(1)}
    assert len(store) == 2
    assert store["a"] == atom("b")
    assert store["c"] == integer(1)


def test_add_store():
    store = flag_store_of(a=atom("x")) + flag_store_of(a=atom("y"), b=atom("z"))
    assert store["a"] == atom("y")
    assert store["b"] == atom("z")


def test_add_does_not_mutate():
    store = EMPTY_FLAG_STORE + {"a": atom("b")}
    assert len(store) == 1
    assert len(EMPTY_FLAG_STORE) == 0


@pytest.mark.parametrize("removed", [Unknown, "unknown", ["unknown"], ("unknown",)])
def test_sub(removed):
    store = DEFAULT_FLAG_STORE - removed
    assert "unknown" not in store
    assert len(store) == len(NOTABLE_FLAGS) - 1
    assert len(DEFAULT_FLAG_STORE) == len(NOTABLE_FLAGS)


def test_sub_many():
    assert len(DEFAULT_FLAG_STORE - ["unknown", "max_arity"]) == len(NOTABLE_FLAGS) - 2


def test_sub_missing_is_harmless():
    assert DEFAULT_FLAG_STORE - "missing" == DEFAULT_FLAG_STORE


def test_set_notable_flag():
    store = DEFAULT_FLAG_STORE.set(Unknown, Unknown.ERROR)
    assert store[Unknown] == Unknown.ERROR
    assert DEFAULT_FLAG_STORE[Unknown] == Unknown.WARNING


def test_set_notable_flag_rejects_inadmissible_values():
    with pytest.raises(JException):
        DEFAULT_FLAG_STORE.set(Unknown, atom("bad"))


def test_set_custom_flag():
    assert EMPTY_FLAG_STORE.set("custom", atom("v"))["custom"] == atom("v")


def test_equality():
    assert FlagStore.of(Unknown) == EMPTY_FLAG_STORE + Unknown
    assert DEFAULT_FLAG_STORE != EMPTY_FLAG_STORE


def flag_store_of(**flags):
    return FlagStore.of(jmap(flags))
