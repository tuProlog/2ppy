"""The factory functions of custom data, re-exported by `tuprolog.solve.data`."""

from collections.abc import Mapping
from typing import Any

from tuprolog.jvmutils import jmap
from tuprolog.pyutils import dict_or_keyword_args

from ._definitions import EMPTY_DATA, CustomData, CustomDataStore

__all__ = ["custom_data", "custom_data_store"]


def custom_data(data: Mapping[str, Any] = {}, **kwargs: Any) -> CustomData:
    """Creates custom data, i.e. a JVM map from keys to values.

    Args:
        data: The values, by key.
        **kwargs: More values, by key.

    Returns:
        The custom data.

    Examples:
        >>> custom_data({"a": 1}, b="x")
        {a=1, b=x}
    """
    return dict_or_keyword_args(data, kwargs, lambda ds: jmap(ds))


def custom_data_store(
    persistent: CustomData = EMPTY_DATA,
    durable: CustomData = EMPTY_DATA,
    ephemeral: CustomData = EMPTY_DATA,
) -> CustomDataStore:
    """Creates a custom data store, from the data of its three tiers.

    Args:
        persistent: The data living as long as the solver.
        durable: The data living during a query.
        ephemeral: The data discarded first.

    Returns:
        The custom data store.

    Examples:
        >>> custom_data_store(persistent=custom_data(a=1))
        CustomDataStore(persistent={a=1}, durable={}, ephemeral={})
    """
    return CustomDataStore.empty().copy(persistent, durable, ephemeral)
