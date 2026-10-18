import it.unibo.tuprolog.solve.library.exception as _exception  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

AlreadyLoadedLibraryException = _exception.AlreadyLoadedLibraryException


LibraryException = _exception.LibraryException


NoSuchALibraryException = _exception.NoSuchALibraryException


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.library.exception.*")
