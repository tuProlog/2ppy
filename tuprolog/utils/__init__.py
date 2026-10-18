"""General-purpose JVM interfaces shared by 2P-Kt's types.

- `Castable`: types whose objects can be cast to sub-types by explicit methods (e.g.
  `term.cast_to_atom()`, `term.as_atom()`).
- `Taggable`: immutable objects carrying named metadata, their *tags* (e.g. terms and
  substitutions).

Examples:
    >>> from tuprolog.core import atom
    >>> from tuprolog.utils import Castable, Taggable
    >>> isinstance(atom("a"), Castable), isinstance(atom("a"), Taggable)
    (True, True)
"""

from ._definitions import Castable, Taggable

__all__ = ["Castable", "Taggable"]
