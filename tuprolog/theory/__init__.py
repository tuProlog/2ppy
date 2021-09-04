import logging
import jpype
import jpype.imports

from it.unibo.tuprolog.theory import MutableTheory
from it.unibo.tuprolog.theory import Theory
from it.unibo.tuprolog.theory import RetractResult

from typing import Iterable, Union
from tuprolog.core import Clause
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jiterable, jmap


logging.debug("Loaded JVM classes from it.unibo.tuprolog.theory.*")


def theory(*clauses: Union[Clause, Iterable[Clause]]) -> Theory:
    return iterable_or_varargs(terms, lambda ts: Theory.of(jiterable(ts)))


def mutable_theory(*clauses: Union[Clause, Iterable[Clause]]) -> MutableTheory:
    return iterable_or_varargs(terms, lambda ts: MutableTheory.of(jiterable(ts)))