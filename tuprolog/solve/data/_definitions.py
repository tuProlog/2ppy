import it.unibo.tuprolog.solve.data as _data  # type: ignore
import java.util as _jutils  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger
from tuprolog.jvmutils import Map

CustomDataStore = _data.CustomDataStore


CustomData = Map


EMPTY_DATA: CustomData = _jutils.Collections.emptyMap()


EMPTY_DATA_STORE: CustomDataStore = CustomDataStore.empty()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.data.*")
