import it.unibo.tuprolog.utils as _utils  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["Castable", "Taggable"]


Castable = _utils.Castable
"""Objects of a type hierarchy that can be cast to its sub-types by explicit methods, e.g. terms.

For terms, `term.cast_to_struct()` returns the term as a `tuprolog.core.Struct`, raising a Java
`ClassCastException` when it is not one, while `term.as_struct()` returns `None` in that case (and
so on for the other term types).

Note:
    2P-Kt's `it.unibo.tuprolog.utils.Castable`.
"""

Taggable = _utils.Taggable
"""Immutable objects carrying *tags*, i.e. named metadata, e.g. terms and substitutions.

Members: `tags` (a map from tag names to values), `get_tag(name)` (a tag's value, or `None`),
`contains_tag(name)`, `replace_tags(tags)` (a copy whose tags are `tags`).

Examples:
    >>> from tuprolog.core import atom
    >>> tagged = atom("a").replace_tags({"source": "user"})
    >>> tagged.get_tag("source"), tagged.contains_tag("other"), atom("a").contains_tag("source")
    ('user', False, False)

Note:
    2P-Kt's `it.unibo.tuprolog.utils.Taggable`.
"""

logger.debug("Loaded JVM classes from it.unibo.tuprolog.utils.*")
