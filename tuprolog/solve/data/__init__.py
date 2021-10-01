from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.data as _data
from tuprolog.jvmutils import Map
from tuprolog.pyutils import dict_or_keyword_args
from tuprolog.jvmutils import jmap
from typing import Mapping, Any


CustomDataStore = _data.CustomDataStore

CustomData = Map


def custom_data(data: Mapping[str, Any] = {}, **kwargs) -> CustomData:
    return dict_or_keyword_args(data, kwargs, lambda ds: jmap(ds))


EMPTY_DATA: CustomData = custom_data()


def custom_data_store(
        persistent: CustomData = EMPTY_DATA,
        durable: CustomData = EMPTY_DATA,
        ephemeral: CustomData = EMPTY_DATA
) -> CustomDataStore:
    return CustomDataStore.empty().copy(persistent, durable, ephemeral)


EMPTY_DATA_STORE: CustomDataStore = CustomDataStore.empty()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.data.*")
