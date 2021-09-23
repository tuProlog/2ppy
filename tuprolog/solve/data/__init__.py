from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.data import CustomDataStore
# noinspection PyUnresolvedReferences
from java.util import Map as CustomData

from tuprolog.jvmutils import jmap

from typing import Mapping, Any


def custom_data(data: Mapping[str, Any] = {}, **kwargs) -> CustomData:
    all_data = dict(**kwargs)
    for k, v in data:
        all_data[k] = v
    return jmap(all_data)


EMPTY_DATA: CustomData = custom_data()


def custom_data_store(
        persistent: CustomData = EMPTY_DATA,
        durable: CustomData = EMPTY_DATA,
        ephemeral: CustomData = EMPTY_DATA
) -> CustomDataStore:
    return CustomDataStore.empty().copy(persistent, durable, ephemeral)


EMPTY_DATA_STORE: CustomDataStore = CustomDataStore.empty()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.data.*")
