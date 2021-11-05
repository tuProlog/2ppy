from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve as _solve
from tuprolog.utils import Taggable
from tuprolog.solve import SolveOptions
from typing import TypeVar


ProbExtensions = _solve.ProbExtensions


def probability(taggable: Taggable) -> float:
    return ProbExtensions.getProbability(taggable)


T = TypeVar("T", bound=Taggable, covariant=True)


def set_probability(taggable: T) -> T:
    return ProbExtensions.setProbability(taggable)


def is_probabilistic(solve_opts: SolveOptions) -> bool:
    return ProbExtensions.isProbabilistic(solve_opts)


def set_probabilistic(solve_opts: SolveOptions, value: bool) -> SolveOptions:
    return ProbExtensions.setProbabilistic(solve_opts, value)


def probabilistic(solve_opts: SolveOptions) -> SolveOptions:
    return ProbExtensions.probabilistic(solve_opts)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.plp.*")
