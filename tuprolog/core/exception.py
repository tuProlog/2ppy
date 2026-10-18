"""The exceptions raised by 2P-Kt's term model (e.g. when applying a substitution fails).

They are JVM exceptions: catch them by these classes (or by `tuprolog.errors`' Python
classifications).
"""

import it.unibo.tuprolog.core.exception as _exceptions  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["SubstitutionApplicationException", "SubstitutionException", "TuPrologException"]


TuPrologException = _exceptions.TuPrologException
"""The base class of 2P-Kt's exceptions (a JVM `RuntimeException`).

Note:
    2P-Kt's `it.unibo.tuprolog.core.exception.TuPrologException`.
"""

SubstitutionException = _exceptions.SubstitutionException
"""Raised when a substitution was expected to be a unifier, but turned out to be the failed one.

Members: `substitution` (the substitution at hand).
"""

SubstitutionApplicationException = _exceptions.SubstitutionApplicationException
"""Raised when applying a substitution to a term fails, as the substitution is the failed one.

Members: `term` (the term), `substitution` (the substitution).
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.exception.*")
