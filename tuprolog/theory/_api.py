from typing import Iterable, Union
from tuprolog.core import Clause
from tuprolog.unify import Unificator
from tuprolog.jvmutils import jiterable
from tuprolog.pyutils import iterable_or_varargs
from ._definitions import Theory, MutableTheory


def theory(*clauses: Union[Clause, Iterable[Clause]]) -> Theory:
    return iterable_or_varargs(clauses, lambda ts: Theory.of(jiterable(ts)))


def mutable_theory(*clauses: Union[Clause, Iterable[Clause]]) -> MutableTheory:
    return iterable_or_varargs(clauses, lambda ts: MutableTheory.of(Unificator.getDefault(), jiterable(ts)))
