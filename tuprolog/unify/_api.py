"""Factories of unification strategies, and unification through the default one."""

from tuprolog.core import Substitution, Term

from ._definitions import DEFAULT_UNIFICATOR, Unificator

__all__ = [
    "cached_unificator",
    "match",
    "mgu",
    "naive_unificator",
    "strict_unificator",
    "unificator",
    "unify",
]


def strict_unificator(context: Substitution | None = None) -> Unificator:
    """Creates a strict unification strategy.

    A strict unificator deems two non-variable terms equal when they are identical, numbers
    included: the integer `1` and the real `1.0` do not unify.

    Args:
        context: The bindings assumed to hold before any unification starts: every result is
            computed as if they were merged into it. None (the default) means no bindings.

    Returns:
        The strict unificator, without caching.

    Examples:
        >>> from tuprolog.core import integer, real
        >>> strict_unificator().match(integer(1), real(1.0))
        False

    Note:
        Wraps 2P-Kt's `Unificator.strict`.
    """
    if context is None:
        return Unificator.strict()
    else:
        return Unificator.strict(context)


def naive_unificator(context: Substitution | None = None) -> Unificator:
    """Creates a naive unification strategy, which compares numbers by value.

    Unlike `strict_unificator`'s strategy, a naive unificator deems two numbers equal when their
    values are, regardless of their representation: the integer `1` and the real `1.0` unify.

    Args:
        context: The bindings assumed to hold before any unification starts. None (the default)
            means no bindings.

    Returns:
        The naive unificator, without caching.

    Examples:
        >>> from tuprolog.core import integer, real
        >>> naive_unificator().match(integer(1), real(1.0))
        True

    Note:
        Wraps 2P-Kt's `Unificator.naive`.
    """
    if context is None:
        return Unificator.naive()
    else:
        return Unificator.naive(context)


def cached_unificator(
    unificator: Unificator, cache_size: int = Unificator.DEFAULT_CACHE_CAPACITY
) -> Unificator:
    """Decorates a unificator so that it memoizes its most recent results.

    The results of `mgu` and `merge` (hence of `match` and `unify` too) are stored in a
    least-recently-used cache, sparing their computation when the same terms are unified again.
    Caching an already cached unificator re-wraps the underlying one, with the new capacity.

    Args:
        unificator: The unificator to decorate.
        cache_size: The maximum amount of results the cache stores (32 by default).

    Returns:
        The cached unificator, behaving as `unificator` does.

    Examples:
        >>> from tuprolog.core import atom, var
        >>> cached = cached_unificator(strict_unificator(), cache_size=8)
        >>> cached.match(var("X"), atom("a"))
        True

    Note:
        Wraps 2P-Kt's `Unificator.cached`.
    """
    return Unificator.cached(unificator, cache_size)


def unificator(context: Substitution | None = None) -> Unificator:
    """Creates the recommended unification strategy: a cached, strict unificator.

    Args:
        context: The bindings assumed to hold before any unification starts: unifications
            conflicting with them fail. None (the default) means no bindings.

    Returns:
        A `cached_unificator` decorating a `strict_unificator`.

    Examples:
        >>> from tuprolog.core import atom, substitution, var
        >>> X = var("X")
        >>> u = unificator(substitution({X: atom("a")}))
        >>> u.match(X, atom("a")), u.match(X, atom("b"))
        (True, False)
    """
    return cached_unificator(strict_unificator(context))


def mgu(x: Term, y: Term, occur_check: bool = True) -> Substitution:
    """Computes the most general unifier of two terms, through the default unificator.

    Args:
        x: The first term. When the two terms have distinct roles, it is the subject (e.g. a goal,
            or a value), and `y` the reference (e.g. a clause head, or a pattern).
        y: The second term.
        occur_check: Whether variables may not be bound to terms containing them (True by
            default): disabling it is faster, but lets unification build cyclic bindings.

    Returns:
        The most general unifier (a `tuprolog.core.Substitution.Unifier`, empty if the terms are
        already equal), or the failed substitution (`Substitution.Fail`, whose `is_failed` is
        True) if the terms do not unify.

    Examples:
        >>> from tuprolog.core import struct, var
        >>> X, Y = var("X"), var("Y")
        >>> unifier = mgu(struct("f", X, "b"), struct("f", "a", Y))
        >>> unifier[X], unifier[Y]
        (a, b)
        >>> mgu(X, struct("f", X)).is_failed
        True
        >>> mgu(X, struct("f", X), occur_check=False).is_failed
        False

    See Also:
        `unify`, `match`, and `Unificator.mgu`.
    """
    return DEFAULT_UNIFICATOR.mgu(x, y, occur_check)


def unify(x: Term, y: Term, occur_check: bool = True) -> Term:
    """Unifies two terms through the default unificator, returning the unified term.

    Args:
        x: The first term, to which the unifier is applied.
        y: The second term.
        occur_check: Whether variables may not be bound to terms containing them (True by
            default).

    Returns:
        `x`, with the most general unifier of `x` and `y` applied to it, or None if the terms do
        not unify.

    Examples:
        >>> from tuprolog.core import atom, struct, var
        >>> unify(struct("f", var("X"), "b"), struct("f", "a", var("Y")))
        f(a, b)
        >>> print(unify(atom("a"), atom("b")))
        None

    See Also:
        `mgu`, `match`, and `Unificator.unify`.
    """
    return DEFAULT_UNIFICATOR.unify(x, y, occur_check)


def match(x: Term, y: Term, occur_check: bool = True) -> bool:
    """Tells whether two terms unify, through the default unificator.

    Args:
        x: The first term.
        y: The second term.
        occur_check: Whether variables may not be bound to terms containing them (True by
            default).

    Returns:
        True if the terms unify, i.e. if `mgu` would not fail, False otherwise.

    Examples:
        >>> from tuprolog.core import atom, struct, var
        >>> match(struct("f", var("X")), struct("f", "a"))
        True
        >>> match(atom("a"), atom("b"))
        False

    See Also:
        `mgu`, `unify`, and `Unificator.match`.
    """
    return DEFAULT_UNIFICATOR.match(x, y, occur_check)
