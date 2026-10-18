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
    """An unordered collection of clauses, possibly with duplicates, indexed for retrieval."""
    factory = MutableClauseMultiSet if mutable else ClauseMultiSet
    return iterable_or_varargs(clauses, lambda cs: factory.of(unificator, jiterable(cs)))


def clause_queue(
    *clauses: Clause | Iterable[Clause],
    unificator: Unificator = DEFAULT_UNIFICATOR,
    mutable: bool = False,
) -> ClauseQueue:
    """An ordered collection of clauses, indexed for retrieval (in FIFO or LIFO order)."""
    factory = MutableClauseQueue if mutable else ClauseQueue
    return iterable_or_varargs(clauses, lambda cs: factory.of(unificator, jiterable(cs)))
