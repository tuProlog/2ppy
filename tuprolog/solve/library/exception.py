"""The errors of loading and unloading libraries.

Examples:
    >>> from tuprolog.solve.library import libraries, library
    >>> try:
    ...     libraries(library("my.lib"), library("my.lib"))
    ... except AlreadyLoadedLibraryException as error:
    ...     print(error.message)
    A library aliased as `my.lib` has already been loaded
"""

import it.unibo.tuprolog.solve.library.exception as _exception  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["AlreadyLoadedLibraryException", "LibraryException", "NoSuchALibraryException"]


AlreadyLoadedLibraryException = _exception.AlreadyLoadedLibraryException
"""Raised when adding, to a runtime, a library whose alias is already loaded.

A `LibraryException`.
"""


LibraryException = _exception.LibraryException
"""The base of the errors of loading and unloading libraries into runtimes.

Unlike `tuprolog.solve.exception.ResolutionException`, these are raised as Python exceptions by
the operations on runtimes, rather than ending resolutions with a *halt* solution.
"""


NoSuchALibraryException = _exception.NoSuchALibraryException
"""Raised when removing, from a runtime, a library that is not loaded.

A `LibraryException`.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.library.exception.*")
