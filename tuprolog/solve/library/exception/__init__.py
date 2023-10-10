from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.library.exception as _exception  # type: ignore


AlreadyLoadedLibraryException = _exception.AlreadyLoadedLibraryException

LibraryException = _exception.LibraryException

NoSuchALibraryException = _exception.NoSuchALibraryException


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.library.exception.*")
