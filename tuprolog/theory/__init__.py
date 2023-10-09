from typing import Iterable, Union
from tuprolog import logger
from tuprolog.core import Clause
from tuprolog.unify import Unificator
from ._ktadapt import *
import jpype.imports
import it.unibo.tuprolog.theory as _theory # type: ignore

Theory = _theory.Theory

MutableTheory = _theory.MutableTheory

RetractResult = _theory.RetractResult


def theory(*clauses: Union[Clause, Iterable[Clause]]) -> Theory:
    return iterable_or_varargs(clauses, lambda ts: Theory.of(jiterable(ts)))


def mutable_theory(*clauses: Union[Clause, Iterable[Clause]]) -> MutableTheory:
    return iterable_or_varargs(clauses, lambda ts: MutableTheory.of(Unificator.getDefault(), jiterable(ts)))


logger.debug("Loaded JVM classes from it.unibo.tuprolog.theory.*")
