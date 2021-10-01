from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.library.exception as _exception


AlreadyLoadedLibraryException = _exception.AlreadyLoadedLibraryException

LibraryException = _exception.LibraryException

NoSuchALibraryException = _exception.NoSuchALibraryException


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.library.exception.*")
