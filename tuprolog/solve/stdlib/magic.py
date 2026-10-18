"""The magic cut, a term used internally by the rules of the standard library."""

import it.unibo.tuprolog.solve.stdlib.magic as _magic  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["MagicCut"]


MagicCut: _magic.MagicCut = _magic.MagicCut.INSTANCE
"""The magic cut, `!MagicCut!`: a special atom acting as a cut (`!`) in standard rules.

Rules like those of `->/2` and `;/2` use it to cut the alternatives of the rule calling them,
rather than those of the goal they appear in. Programs never need it.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.magic.*")
