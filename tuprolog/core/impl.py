"""Concrete implementations of term-related types, for advanced uses.

Prefer the factories of `tuprolog.core` (e.g. `tuprolog.core.default_formatter`) to these classes.
"""

import it.unibo.tuprolog.core.impl as _impl  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger
from tuprolog.core import TermFormatter

__all__ = ["DefaultTermFormatter"]


DefaultTermFormatter = _impl.SimpleTermFormatter
"""The simplest term formatter: canonical rendering, with variables by their complete name.

Its constructor takes (all optional): `quoted` (whether to quote atoms when needed, default
true), `numberVars` (whether to render `'$VAR'(N)` terms as variable names, default false),
`ignoreOps` (whether to ignore operators, default false), `tagsOptions` (a
`tuprolog.core.TagsFormattingOptions`).

Examples:
    >>> from tuprolog.core import struct, var
    >>> DefaultTermFormatter().format(struct("f", var("X")))
    'f(X_...)'

Note:
    2P-Kt's `it.unibo.tuprolog.core.impl.SimpleTermFormatter`, an internal class of 2P-Kt.
"""

logger.debug(
    "Loaded compatibility layer for JVM subtypes of " + str(TermFormatter.class_.getName())
)
