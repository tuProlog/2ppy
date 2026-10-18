"""Unification of logic terms.

*Unification* is the basic operation of logic programming: given two terms, it looks for a way of
binding their variables so that the two terms become syntactically equal. For instance, `f(X, b)`
and `f(a, Y)` unify by binding `X` to `a` and `Y` to `b`, while `f(X)` and `g(X)` do not unify,
as their functors differ. Prolog uses unification to pass arguments (a goal is unified with the
heads of the clauses defining it), to return results, and to deconstruct data.

The bindings unification finds are represented by a `tuprolog.core.Substitution`: a *unifier*
(`Substitution.Unifier`) when unification succeeds, or the *failed* substitution
(`Substitution.Fail`) when it does not. Among all the substitutions making two terms equal,
unification computes the *most general unifier* (MGU), i.e. the one binding variables only as much
as needed: any other unifier is an instance of it.

The *occurs check* forbids binding a variable to a term containing it (e.g. `X` to `f(X)`), which
would otherwise denote an infinite term. It is enabled by default here: disabling it (as most
Prolog systems do in `=/2`) is faster, but unsound whenever such cyclic bindings may arise.

This package offers:

- `mgu`, `unify` and `match`: unification through the default strategy, returning respectively
  the MGU, the unified term, or whether the terms unify;
- `Unificator`: the type of unification strategies, created by `strict_unificator`,
  `naive_unificator` (comparing numbers by value) and `unificator` / `cached_unificator`
  (memoizing recent results);
- `tuprolog.unify.exception`: the exceptions signalling unification failures.

Examples:
    >>> from tuprolog.core import atom, struct, var
    >>> X, Y = var("X"), var("Y")
    >>> unifier = mgu(struct("f", X, "b"), struct("f", "a", Y))
    >>> unifier[X], unifier[Y]
    (a, b)
    >>> unify(struct("f", X, "b"), struct("f", "a", Y))
    f(a, b)
    >>> match(struct("f", X), struct("g", X))
    False

See Also:
    `tuprolog.core.Substitution`, the type of unifiers; 2P-Kt's
    [unification API](https://tuprolog.github.io/2p-kt/reference/unification-api/).
"""

from ._api import *
from ._definitions import *

__all__ = [
    "DEFAULT_UNIFICATOR",
    "Unificator",
    "cached_unificator",
    "match",
    "mgu",
    "naive_unificator",
    "strict_unificator",
    "unificator",
    "unify",
]
