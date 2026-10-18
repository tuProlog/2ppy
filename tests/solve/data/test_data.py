"""Custom data and custom data stores."""

import pytest
from jpype import JException

from tuprolog.core import atom
from tuprolog.solve.data import (
    EMPTY_DATA,
    EMPTY_DATA_STORE,
    CustomData,
    CustomDataStore,
    custom_data,
    custom_data_store,
)


def as_dict(data) -> dict:
    return {str(k): data[k] for k in data}


def test_empty_data():
    assert len(EMPTY_DATA) == 0
    assert isinstance(EMPTY_DATA, CustomData)


def test_empty_data_is_immutable():
    with pytest.raises(JException):
        EMPTY_DATA.put("polluted", 1)
    assert len(EMPTY_DATA) == 0


def test_custom_data_empty():
    data = custom_data()
    assert isinstance(data, CustomData)
    assert len(data) == 0


def test_custom_data_from_dict_and_keywords():
    data = custom_data({"a": atom("x")}, b=atom("y"))
    assert as_dict(data) == {"a": atom("x"), "b": atom("y")}


def test_custom_data_keywords_override_dict():
    assert as_dict(custom_data({"a": atom("x")}, a=atom("y"))) == {"a": atom("y")}


def test_custom_data_accepts_python_values():
    data = custom_data(n=1, s="text")
    assert data["n"] == 1
    assert data["s"] == "text"


def test_custom_data_store_empty():
    store = custom_data_store()
    assert isinstance(store, CustomDataStore)
    assert store == EMPTY_DATA_STORE == CustomDataStore.empty()
    assert len(store.persistent) == len(store.durable) == len(store.ephemeral) == 0


def test_custom_data_store_tiers():
    store = custom_data_store(custom_data(p=1), custom_data(d=2), custom_data(e=3))
    assert as_dict(store.persistent) == {"p": 1}
    assert as_dict(store.durable) == {"d": 2}
    assert as_dict(store.ephemeral) == {"e": 3}


def test_custom_data_store_keyword_tiers_and_dicts():
    store = custom_data_store(ephemeral={"e": 3})
    assert as_dict(store.ephemeral) == {"e": 3}
    assert len(store.persistent) == 0


def test_custom_data_store_pruning():
    store = custom_data_store(custom_data(p=1), custom_data(d=2), custom_data(e=3))
    discarded = store.discardEphemeral()
    assert len(discarded.ephemeral) == 0 and len(discarded.durable) == 1
    preserved = store.preservePersistent()
    assert len(preserved.durable) == 0 and len(preserved.persistent) == 1
