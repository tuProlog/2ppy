from collections.abc import Iterable

from tuprolog.core import Clause
from tuprolog.jvmutils import jiterable
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.unify import Unificator

from ._definitions import MutableTheory, Theory

__all__ = ["mutable_theory", "theory"]


def theory(*clauses: Clause | Iterable[Clause]) -> Theory:
    return iterable_or_varargs(clauses, lambda ts: Theory.of(jiterable(ts)))


def mutable_theory(*clauses: Clause | Iterable[Clause]) -> MutableTheory:
    return iterable_or_varargs(
        clauses, lambda ts: MutableTheory.of(Unificator.getDefault(), jiterable(ts))
    )
