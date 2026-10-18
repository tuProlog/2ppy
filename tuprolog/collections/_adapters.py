from collections.abc import Iterable, Sized

from jpype import JClass, JImplementationFor

from tuprolog import logger
from tuprolog.core import Term
from tuprolog.jvmutils import jiterable

_MutableClauseCollection = JClass("it.unibo.tuprolog.collections.MutableClauseCollection")


def _clauses(clause, clauses) -> list:
    if len(clauses) == 0 and isinstance(clause, Iterable) and not isinstance(clause, Term):
        return list(clause)
    return [clause, *clauses]


@JImplementationFor("it.unibo.tuprolog.collections.ClauseCollection")
class _KtClauseCollection:
    def __jclass_init__(cls):
        Sized.register(cls)

    def __len__(self):
        return self.getSize()

    def __bool__(self):
        return not self.isEmpty()

    def __contains__(self, clause):
        return self.contains(clause)

    def __add__(self, other):
        """collection + clause, or collection + iterable of clauses (for mutable collections,
        this changes the collection in place, as `add`/`addAll` do)."""
        if isinstance(other, Iterable) and not isinstance(other, Term):
            return self.addAll(jiterable(other))
        return self.add(other)

    def __hash__(self):
        # value-based equality: a mutable collection's hash would change with its clauses
        if isinstance(self, _MutableClauseCollection):
            raise TypeError(f"unhashable type: '{type(self).__name__}'")
        return self.hashCode()

    def add_all(self, clause, *clauses):
        """add_all(c1, c2, ...) or add_all(iterable_of_clauses)."""
        return self.addAll(jiterable(_clauses(clause, clauses)))

    def contains_all(self, clause, *clauses):
        return self.containsAll(jiterable(_clauses(clause, clauses)))


@JImplementationFor("it.unibo.tuprolog.collections.ClauseMultiSet")
class _KtClauseMultiSet:
    def __getitem__(self, clause):
        """The clauses unifying with `clause`."""
        return list(self.get(clause))


@JImplementationFor("it.unibo.tuprolog.collections.ClauseQueue")
class _KtClauseQueue:
    def __getitem__(self, clause):
        """The clauses unifying with `clause`, in FIFO order."""
        return list(self.getFifoOrdered(clause))

    def fifo_ordered(self, clause):
        return list(self.getFifoOrdered(clause))

    def lifo_ordered(self, clause):
        return list(self.getLifoOrdered(clause))


@JImplementationFor("it.unibo.tuprolog.collections.RetrieveResult")
class _KtRetrieveResult:
    def __bool__(self):
        return self.isSuccess()


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.collections.*")
