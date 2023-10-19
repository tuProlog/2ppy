from typing import Mapping, Any
from tuprolog.pyutils import dict_or_keyword_args
from tuprolog.jvmutils import jmap
from ._definitions import CustomData, CustomDataStore, EMPTY_DATA


def custom_data(data: Mapping[str, Any] = {}, **kwargs) -> CustomData:
    return dict_or_keyword_args(data, kwargs, lambda ds: jmap(ds))


def custom_data_store(
        persistent: CustomData = EMPTY_DATA,
        durable: CustomData = EMPTY_DATA,
        ephemeral: CustomData = EMPTY_DATA
) -> CustomDataStore:
    return CustomDataStore.empty().copy(persistent, durable, ephemeral)
