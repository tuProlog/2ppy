"""Exceptions signalling unification failures.

`tuprolog.unify`'s functions and unificators report failures as values (the failed substitution,
None, or False): these exceptions are raised by the code needing two terms to unify, and are
`tuprolog.errors.UnificationError`s (hence `ValueError`s).
"""

import it.unibo.tuprolog.unify.exception as _exceptions  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["NoUnifyException", "OccurCheckException"]


NoUnifyException = _exceptions.NoUnifyException
"""Two terms could not be unified.

Constructed as `NoUnifyException(term1, term2)`; its `message` names the two terms. It is a
`tuprolog.errors.UnificationError`, hence a `ValueError`.

Examples:
    >>> from tuprolog.core import atom
    >>> NoUnifyException(atom("a"), atom("b")).message
    'Cannot match term `a` with term `b`'
"""

OccurCheckException = _exceptions.OccurCheckException
"""Two terms could not be unified because of the occurs check.

A `NoUnifyException` whose cause is a variable occurring in the term it should be bound to (e.g.
`X` and `f(X)`). Constructed as `OccurCheckException(term1, term2, variable, term)`.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.unify.exception.*")
