"""Pythonic adapters for `tuprolog.solve.flags.FlagStore`."""

from collections.abc import Mapping

from jpype import JImplementationFor

from tuprolog import logger
from tuprolog.jvmutils import jmap

from ._definitions import NotableFlag


@JImplementationFor("it.unibo.tuprolog.solve.flags.FlagStore")
class _KtFlagStore:
    """Adds `len`, `in`, indexing, `+` and `-` to `FlagStore`s."""

    def __jclass_init__(cls):
        pass

    def __len__(self):
        """Returns the number of flags."""
        return self.getSize()

    def __getitem__(self, notableFlag):
        """Returns the value of the flag with the given name (or notable flag).

        Raises:
            KeyError: If there is no such flag.
        """
        value = self.get(notableFlag)
        if value is None:
            raise KeyError(
                notableFlag.name if isinstance(notableFlag, NotableFlag) else notableFlag
            )
        return value

    def __contains__(self, flag):
        """Returns whether there is a flag with the given name (or notable flag)."""
        if isinstance(flag, NotableFlag):
            flag = flag.name
        return self.containsKey(flag)

    def __add__(self, other):
        """Returns a store with the flags of `other` added, overriding homonymous ones.

        Args:
            other: A `Flag`, a `NotableFlag` (set to its default value), a `FlagStore`, or a
                mapping from names to terms (or Python values, see `tuprolog.core.to_term`).
        """
        if isinstance(other, Mapping):
            from tuprolog.core import to_term

            return self.plus(jmap({k: to_term(v) for k, v in other.items()}))
        return self.plus(other)

    def __sub__(self, other):
        """Returns a store without the flag named `other` (a name, or a `NotableFlag`)."""
        if isinstance(other, NotableFlag):
            return self.minus(other.name)
        return self.minus(other)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.solve.flags.*")
