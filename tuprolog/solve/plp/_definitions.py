"""The JVM class of 2P-Kt's PLP extensions, re-exported by `tuprolog.solve.plp`."""

import it.unibo.tuprolog.solve as _solve  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["ProbExtensions"]


ProbExtensions = _solve.ProbExtensions
"""The JVM class of 2P-Kt's PLP extension functions, wrapped by `tuprolog.solve.plp`'s functions.

Its static methods (e.g. `getProbability(taggable)`, `setProbabilistic(options, value)`) are those
the functions of `tuprolog.solve.plp` call; it also has the constants `DEFAULT_PROBABILITY` (1.0)
and `DEFAULT_PROBABILISTIC_OPTION` (`False`).
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.plp.*")
