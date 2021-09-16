from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.theory import MutableTheory, Theory, RetractResult

# noinspection PyUnresolvedReferences
from typing import Iterable, Union

# noinspection PyUnresolvedReferences
from tuprolog.core import Clause
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jiterable


def theory(*clauses: Union[Clause, Iterable[Clause]]) -> Theory:
    return iterable_or_varargs(clauses, lambda ts: Theory.of(jiterable(ts)))


def mutable_theory(*clauses: Union[Clause, Iterable[Clause]]) -> MutableTheory:
    return iterable_or_varargs(clauses, lambda ts: MutableTheory.of(jiterable(ts)))


logger.debug("Loaded JVM classes from it.unibo.tuprolog.theory.*")
