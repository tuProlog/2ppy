from collections.abc import Mapping
from typing import Any

from tuprolog.jvmutils import jmap
from tuprolog.pyutils import dict_or_keyword_args

from ._definitions import EMPTY_DATA, CustomData, CustomDataStore

__all__ = ["custom_data", "custom_data_store"]


def custom_data(data: Mapping[str, Any] = {}, **kwargs: Any) -> CustomData:
    return dict_or_keyword_args(data, kwargs, lambda ds: jmap(ds))


def custom_data_store(
    persistent: CustomData = EMPTY_DATA,
    durable: CustomData = EMPTY_DATA,
    ephemeral: CustomData = EMPTY_DATA,
) -> CustomDataStore:
    return CustomDataStore.empty().copy(persistent, durable, ephemeral)
