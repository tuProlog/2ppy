"""Pythonic adapters for `tuprolog.solve.library.Library` and `Runtime`."""

from jpype import JImplementationFor

from ._definitions import Runtime


@JImplementationFor("it.unibo.tuprolog.solve.library.Library")
class _KtLibrary:
    """Adds `to_runtime` to `Library`."""

    def __jclass_init__(self):
        pass

    def to_runtime(self):
        """Returns the runtime made of this library only."""
        return Runtime.of(self)


@JImplementationFor("it.unibo.tuprolog.solve.library.Runtime")
class _KtRuntime:
    """Adds `+` to `Runtime`."""

    def __jclass_init__(self):
        pass

    def __add__(self, other):
        """Returns the runtime with the libraries of `other` (a library or a runtime) added.

        Raises:
            tuprolog.solve.library.exception.AlreadyLoadedLibraryException: If a library of
                `other` has the alias of a library of this runtime.
        """
        return self.plus(other)
