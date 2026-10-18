"""The JVM types of custom data, re-exported by `tuprolog.solve.data`."""

import it.unibo.tuprolog.solve.data as _data  # type: ignore
import java.util as _jutils  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger
from tuprolog.jvmutils import Map

__all__ = ["EMPTY_DATA", "EMPTY_DATA_STORE", "CustomData", "CustomDataStore"]


CustomDataStore = _data.CustomDataStore
"""The custom data of a solver, in three tiers: `persistent`, `durable` and `ephemeral`.

Each tier is a `CustomData` map. Members: `persistent`, `durable`, `ephemeral`,
`copy(persistent, durable, ephemeral)`, `discard_ephemeral()` (a copy without ephemeral data),
`preserve_persistent()` (a copy with persistent data only). Create stores with
`custom_data_store`.
"""


CustomData = Map
"""Custom data: a JVM map from keys (strings) to arbitrary values, created by `custom_data`."""


EMPTY_DATA: CustomData = _jutils.Collections.emptyMap()
"""The empty custom data."""


EMPTY_DATA_STORE: CustomDataStore = CustomDataStore.empty()
"""The custom data store with no data in any tier."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.data.*")
