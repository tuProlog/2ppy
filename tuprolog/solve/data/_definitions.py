from tuprolog import logger
from tuprolog.jvmutils import Map
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.data as _data  # type: ignore


CustomDataStore = _data.CustomDataStore


CustomData = Map


EMPTY_DATA: CustomData = Map @ {}


EMPTY_DATA_STORE: CustomDataStore = CustomDataStore.empty()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.data.*")
