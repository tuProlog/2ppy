"""JVM types of clause collections, re-exported from 2P-Kt's `it.unibo.tuprolog.collections`."""

import it.unibo.tuprolog.collections as _collections  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "ClauseCollection",
    "ClauseMultiSet",
    "ClauseQueue",
    "MutableClauseCollection",
    "MutableClauseMultiSet",
    "MutableClauseQueue",
    "RetrieveResult",
]


ClauseCollection = _collections.ClauseCollection
"""An immutable collection of clauses, matched by unification.

The operations "changing" it return new collections, leaving it untouched. It is the common
interface of `ClauseQueue` and `ClauseMultiSet`.

Python protocols (see `tuprolog.collections._adapters`):
    - `len(collection)`, `bool(collection)`: the amount of clauses, and whether there is any.
    - `clause in collection`: whether some clause unifies with `clause`.
    - `collection + clause`, `collection + clauses`: the collection with clauses added (for
      mutable collections, the collection itself, changed).
    - iteration, over all clauses; `==` and, for immutable collections, hashing.

Members:
    - `add(clause)`, `add_all(clause, ...)`: the collection with clauses added.
    - `contains_all(clause, ...)`: whether every clause unifies with some stored clause.
    - `retrieve(clause)`, `retrieve_all(clause)`: the `RetrieveResult` of removing the first, or
      every, clause unifying with `clause`.
    - `rules`, `directives`, `size`, `is_empty()`, `is_non_empty()`, `unificator`.

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.collections.ClauseCollection` interface.
"""

MutableClauseCollection = _collections.MutableClauseCollection
"""A `ClauseCollection` changing in place.

`add`, `add_all`, `retrieve` and `retrieve_all` change the collection itself, and return it (or
a `RetrieveResult` wrapping it), which is cheaper than copying collections changing often.
Mutable collections are not hashable.

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.collections.MutableClauseCollection` interface.
"""

ClauseMultiSet = _collections.ClauseMultiSet
"""An immutable, unordered `ClauseCollection`, possibly containing duplicates.

Python protocols:
    - `multiset[clause]`: the list of the stored clauses unifying with `clause`, in no
      particular order.

Members:
    - `count(clause)`: how many stored clauses unify with `clause`.
    - `get(clause)`: the stored clauses unifying with `clause`, as a lazy iterable.

Examples:
    >>> from tuprolog.core import fact, struct, var
    >>> from tuprolog.collections import clause_multi_set
    >>> multiset = clause_multi_set(fact(struct("f", "a")), fact(struct("f", "a")))
    >>> multiset.count(fact(struct("f", var("X"))))
    2

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.collections.ClauseMultiSet` interface; create multisets with
    `tuprolog.collections.clause_multi_set`.
"""

MutableClauseMultiSet = _collections.MutableClauseMultiSet
"""A `ClauseMultiSet` changing in place (see `MutableClauseCollection`).

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.collections.MutableClauseMultiSet` interface.
"""

ClauseQueue = _collections.ClauseQueue
"""An immutable `ClauseCollection` keeping the insertion order of clauses.

Clauses are added at the end (`add`, `add_last`) or at the beginning (`add_first`), and retrieved
in FIFO order (from the first to the last) or in LIFO order (from the last to the first).

Python protocols:
    - `queue[clause]`: the list of the stored clauses unifying with `clause`, in FIFO order.

Members:
    - `add_first(clause)`, `add_last(clause)`: the queue with a clause added at an end.
    - `fifo_ordered(clause)`, `lifo_ordered(clause)`: the lists of the stored clauses unifying
      with `clause`, in FIFO or LIFO order.
    - `retrieve_first(clause)`: the `RetrieveResult` of removing the first clause unifying with
      `clause` (as `retrieve` does).

Examples:
    >>> from tuprolog.core import fact, struct
    >>> from tuprolog.collections import clause_queue
    >>> queue = clause_queue(fact(struct("f", "a")))
    >>> queue.add_first(fact(struct("f", "b")))
    ReteClauseQueue(f(b) :- true, f(a) :- true)

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.collections.ClauseQueue` interface; create queues with
    `tuprolog.collections.clause_queue`.
"""

MutableClauseQueue = _collections.MutableClauseQueue
"""A `ClauseQueue` changing in place (see `MutableClauseCollection`).

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.collections.MutableClauseQueue` interface.
"""

RetrieveResult = _collections.RetrieveResult
"""The outcome of removing clauses from a `ClauseCollection` (see `ClauseCollection.retrieve`).

It is either a `RetrieveResult.Success`, if some clauses were removed, or a
`RetrieveResult.Failure`, if no clause matched; it is truthy if successful.

Members:
    - `is_success`, `is_failure`: which outcome it is.
    - `collection`: the collection resulting from the operation (unchanged on failure).
    - `clauses`: the list of removed clauses (None on failure).
    - `first_clause`: the first removed clause (None on failure).

Examples:
    >>> from tuprolog.core import fact, struct, var
    >>> from tuprolog.collections import clause_queue
    >>> result = clause_queue(fact(struct("f", "a"))).retrieve(fact(struct("f", var("X"))))
    >>> bool(result), result.first_clause
    (True, f(a) :- true)

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.collections.RetrieveResult` sealed class.
"""

logger.debug("Loaded JVM classes from it.unibo.tuprolog.collections.*")
