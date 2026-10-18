"""Indexed collections of clauses, retrieved by unification.

Clause collections store clauses (see `tuprolog.core.Clause`) and look them up by *unification*
(see `tuprolog.unify`) rather than by equality: asking for `f(X)` gives back the stored clauses
`f(a)`, `f(b)`, ... that unify with it. They are the storage on which theories
(`tuprolog.theory.Theory`) are built, and are indexed (by functor, arity and first argument) so
that lookups only check the clauses which may unify.

Two kinds of collections exist:

- *queues* (`ClauseQueue`, built by `clause_queue`) keep the insertion order, and retrieve clauses
  in FIFO (first-in, first-out) or LIFO (last-in, first-out) order: Prolog needs clauses to be
  tried in order, so theories use queues;
- *multisets* (`ClauseMultiSet`, built by `clause_multi_set`) give no ordering guarantee, and
  may contain duplicates.

Both come in an immutable flavour, whose "changing" operations return new collections, and in a
mutable one (`MutableClauseQueue`, `MutableClauseMultiSet`), changing in place.

Examples:
    >>> from tuprolog.core import fact, struct, var
    >>> queue = clause_queue(fact(struct("f", "a")), fact(struct("f", "b")), fact(struct("g", "c")))
    >>> len(queue)
    3
    >>> queue[fact(struct("f", var("X")))]
    [f(a) :- true, f(b) :- true]
    >>> queue.lifo_ordered(fact(struct("f", var("X"))))
    [f(b) :- true, f(a) :- true]
    >>> queue.retrieve(fact(struct("f", var("X")))).collection
    ReteClauseQueue(f(b) :- true, g(c) :- true)

See Also:
    `tuprolog.theory`, for the Prolog-flavoured API of knowledge bases.
"""

import tuprolog.collections._adapters as _

from ._api import *
from ._definitions import *

__all__ = [
    "ClauseCollection",
    "ClauseMultiSet",
    "ClauseQueue",
    "MutableClauseCollection",
    "MutableClauseMultiSet",
    "MutableClauseQueue",
    "RetrieveResult",
    "clause_multi_set",
    "clause_queue",
]
