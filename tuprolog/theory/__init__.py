from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.theory as _theory
import it.unibo.tuprolog.unify as _unify
from typing import Iterable, Union
from tuprolog.core import Clause
from ._ktadapt import *

Theory = _theory.Theory

MutableTheory = _theory.MutableTheory

RetractResult = _theory.RetractResult

Unificator = _unify.Unificator


def theory(*clauses: Union[Clause, Iterable[Clause]]) -> Theory:
    return iterable_or_varargs(clauses, lambda ts: Theory.of(jiterable(ts)))


def mutable_theory(*clauses: Union[Clause, Iterable[Clause]]) -> MutableTheory:
    return iterable_or_varargs(clauses, lambda ts: MutableTheory.of(Unificator.getDefault(), jiterable(ts)))


logger.debug("Loaded JVM classes from it.unibo.tuprolog.theory.*")
