from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.library as _library  # type: ignore


Library = _library.Library


Pluggable = _library.Pluggable


Runtime = _library.Runtime


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.library.*")
