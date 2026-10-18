import it.unibo.tuprolog.solve.libs.io as _io  # type: ignore
import it.unibo.tuprolog.solve.libs.oop as _oop  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["IOLib", "OOPLib"]


IOLib: _io.IOLib = _io.IOLib.INSTANCE


OOPLib: _oop.OOPLib = _oop.OOPLib.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.libs.*")
