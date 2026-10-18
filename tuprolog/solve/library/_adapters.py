"""Pythonic adapters for `tuprolog.solve.library.Library` and `Runtime`."""

from collections.abc import Iterable

from jpype import JImplementationFor

from tuprolog.jvmutils import jiterable

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
    """Adds `+` and `-` to `Runtime`."""

    def __jclass_init__(self):
        pass

    def __add__(self, other):
        """Returns the runtime with the libraries of `other` (a library or a runtime) added.

        Raises:
            tuprolog.solve.library.exception.AlreadyLoadedLibraryException: If a library of
                `other` has the alias of a library of this runtime.
        """
        return self.plus(other)

    def __sub__(self, other):
        """Returns the runtime without the libraries in `other`.

        Args:
            other: A library, an alias, or an iterable of aliases.

        Raises:
            KeyError: If no library of this runtime has one of those aliases.
        """
        if isinstance(other, str):
            aliases = {other}
        elif isinstance(other, Iterable):
            aliases = {str(alias) for alias in other}
        else:
            aliases = {str(other.getAlias())}
        missing = aliases - {str(alias) for alias in self.getAliases()}
        if missing:
            raise KeyError(", ".join(sorted(missing)))
        # 2P-Kt's Runtime.minus raises NoSuchALibraryException exactly when the library is loaded
        kept = [
            library for library in self.getLibraries() if str(library.getAlias()) not in aliases
        ]
        return Runtime.of(jiterable(kept))
