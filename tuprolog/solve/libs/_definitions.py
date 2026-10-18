import it.unibo.tuprolog.solve.libs.io as _io  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["IOLib"]


IOLib: _io.IOLib = _io.IOLib.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.libs.*")
