import it.unibo.tuprolog.solve.library as _library  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

Library = _library.Library


Pluggable = _library.Pluggable


Runtime = _library.Runtime


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.library.*")
