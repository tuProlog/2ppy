"""The `flag_store()` helper."""

import pytest

from tuprolog.core import atom, integer
from tuprolog.solve.flags import (
    DEFAULT_FLAG_STORE,
    EMPTY_FLAG_STORE,
    FlagStore,
    MaxArity,
    Unknown,
    flag,
    flag_store,
)


def test_flag_store_empty():
    store = flag_store()
    assert isinstance(store, FlagStore)
    assert store == EMPTY_FLAG_STORE


def test_flag_store_from_notable_flags():
    store = flag_store(Unknown, MaxArity)
    assert store == FlagStore.of(Unknown, MaxArity)
    assert store[Unknown] == Unknown.WARNING


def test_flag_store_from_flags_and_pairs():
    store = flag_store(flag("a", atom("x")), ("b", atom("y")), ["c", atom("z")])
    assert {k: str(v) for k, v in [(str(k), store[k]) for k in store]} == {
        "a": "x",
        "b": "y",
        "c": "z",
    }


def test_flag_store_from_keyword_arguments():
    store = flag_store(a=atom("x"), unknown=Unknown.FAIL)
    assert store["a"] == atom("x")
    assert store[Unknown] == Unknown.FAIL


def test_flag_store_from_other_stores():
    store = flag_store(DEFAULT_FLAG_STORE, flag_store(a=atom("x")))
    assert len(store) == len(DEFAULT_FLAG_STORE) + 1


def test_flag_store_from_dict():
    store = flag_store({"a": atom("x"), "b": atom("y")})
    assert len(store) == 2
    assert store["a"] == atom("x")


def test_flag_store_rejects_malformed_arguments():
    with pytest.raises(ValueError):
        flag_store([Unknown, atom("x"), atom("y")])


def test_flag_store_mixed():
    store = flag_store(Unknown, ("a", atom("x")), DEFAULT_FLAG_STORE, b=atom("y"))
    assert len(store) == len(DEFAULT_FLAG_STORE) + 2


def test_flag_store_keyword_arguments_override_positional_ones():
    assert flag_store(DEFAULT_FLAG_STORE, unknown=Unknown.FAIL)[Unknown] == Unknown.FAIL
    assert flag_store({"unknown": Unknown.ERROR}, unknown=Unknown.FAIL)[Unknown] == Unknown.FAIL


def test_flag_store_later_positional_arguments_override_earlier_ones():
    assert flag_store(("unknown", Unknown.FAIL), Unknown)[Unknown] == Unknown.WARNING
    assert flag_store(Unknown, ("unknown", Unknown.FAIL))[Unknown] == Unknown.FAIL
    assert flag_store(DEFAULT_FLAG_STORE, ("unknown", Unknown.FAIL))[Unknown] == Unknown.FAIL


def test_flag_store_accepts_a_single_iterable_of_flags():
    assert flag_store([Unknown, MaxArity]) == flag_store(Unknown, MaxArity)


def test_flag_store_converts_python_values():
    assert flag_store({"a": "x"}, b=1) == flag_store({"a": atom("x"), "b": integer(1)})


def test_flag_store_accepts_one_shot_iterators():
    assert flag_store(iter([("a", 1), ("b", 2)])) == flag_store(a=1, b=2)
    assert flag_store(iter(["a", 1])) == flag_store(a=1)
