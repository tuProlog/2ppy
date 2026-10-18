"""JVM types of unification, re-exported from 2P-Kt's `it.unibo.tuprolog.unify`."""

import it.unibo.tuprolog.unify as _unify  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["DEFAULT_UNIFICATOR", "Unificator"]


Unificator = _unify.Unificator
"""A unification strategy, i.e. an object unifying pairs of terms.

Unificators report failures as values, not exceptions: unifying terms that do not unify gives
the failed substitution (or None, or False). Strategies differ in how they compare non-variable
terms (`tuprolog.unify.strict_unificator` and `tuprolog.unify.naive_unificator`), and may be
decorated with caching (`tuprolog.unify.cached_unificator`). Every operation enables the occurs
check unless its last argument (`occur_check_enabled`) is False.

Members:
    - `mgu(term1, term2[, occur_check_enabled])`: the most general unifier of the terms, or the
      failed substitution.
    - `match(term1, term2[, occur_check_enabled])`: whether the terms unify.
    - `unify(term1, term2[, occur_check_enabled])`: `term1` with the most general unifier applied
      to it, or None.
    - `merge(substitution1, substitution2[, occur_check_enabled])`: the union of two
      substitutions, unifying the terms they bind the same variables to (the failed substitution
      if they disagree).
    - `context`: the bindings assumed to hold before unification starts.
    - `Unificator.DEFAULT_CACHE_CAPACITY`: the default size of cached unificators' caches (32).

Examples:
    >>> from tuprolog.core import atom, substitution, var
    >>> X = var("X")
    >>> u = Unificator.strict()
    >>> u.mgu(X, atom("a"))[X]
    a
    >>> u.merge(substitution({X: atom("a")}), substitution({X: atom("b")})).is_failed
    True

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.unify.Unificator` interface.
"""


DEFAULT_UNIFICATOR = Unificator.getDefault()
"""The default `Unificator`: a strict one, without caching, used by `tuprolog.unify.mgu`,
`tuprolog.unify.unify` and `tuprolog.unify.match`."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.unify.*")
