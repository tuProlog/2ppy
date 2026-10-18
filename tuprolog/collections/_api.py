"""Factories of clause collections."""

from collections.abc import Iterable

from tuprolog.core import Clause
from tuprolog.jvmutils import jiterable
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.unify import DEFAULT_UNIFICATOR, Unificator

from ._definitions import ClauseMultiSet, ClauseQueue, MutableClauseMultiSet, MutableClauseQueue

__all__ = ["clause_multi_set", "clause_queue"]


def clause_multi_set(
    *clauses: Clause | Iterable[Clause],
    unificator: Unificator = DEFAULT_UNIFICATOR,
    mutable: bool = False,
) -> ClauseMultiSet:
    """Creates an unordered collection of clauses, possibly with duplicates, indexed for retrieval.

    Args:
        *clauses: The clauses, either as arguments or as one iterable.
        unificator: The `tuprolog.unify.Unificator` matching clauses (the default one, unless
            given).
        mutable: Whether the multiset changes in place (False by default).

    Returns:
        A `ClauseMultiSet`, or a `MutableClauseMultiSet` if `mutable`.

    Examples:
        >>> from tuprolog.core import fact, struct, var
        >>> multiset = clause_multi_set([fact(struct("f", "a")), fact(struct("f", "a"))])
        >>> multiset[fact(struct("f", var("X")))]
        [f(a) :- true, f(a) :- true]
    """
    factory = MutableClauseMultiSet if mutable else ClauseMultiSet
    return iterable_or_varargs(clauses, lambda cs: factory.of(unificator, jiterable(cs)))


def clause_queue(
    *clauses: Clause | Iterable[Clause],
    unificator: Unificator = DEFAULT_UNIFICATOR,
    mutable: bool = False,
) -> ClauseQueue:
    """Creates an ordered collection of clauses, indexed for retrieval (in FIFO or LIFO order).

    Args:
        *clauses: The clauses, in order, either as arguments or as one iterable.
        unificator: The `tuprolog.unify.Unificator` matching clauses (the default one, unless
            given).
        mutable: Whether the queue changes in place (False by default).

    Returns:
        A `ClauseQueue`, or a `MutableClauseQueue` if `mutable`.

    Examples:
        >>> from tuprolog.core import atom, fact
        >>> queue = clause_queue(mutable=True)
        >>> _ = queue.add_all(fact(atom("a")), fact(atom("b")))
        >>> queue
        MutableReteClauseQueue(a :- true, b :- true)
    """
    factory = MutableClauseQueue if mutable else ClauseQueue
    return iterable_or_varargs(clauses, lambda cs: factory.of(unificator, jiterable(cs)))
