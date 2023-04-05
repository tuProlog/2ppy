from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve as _solve
from tuprolog.utils import Taggable
from tuprolog.solve import SolveOptions, solve_options as _solve_options, MAX_TIMEOUT, ALL_SOLUTIONS
from typing import TypeVar, Mapping, Any


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


def solve_options(
        lazy: bool = True,
        timeout: int = MAX_TIMEOUT,
        limit: int = ALL_SOLUTIONS,
        probabilistic: bool = False,
        custom: Mapping[str, Any] = dict(),
        **kwargs: Any
) -> SolveOptions:
    non_probabilistic = _solve_options(lazy, timeout, limit, custom, **kwargs)
    if probabilistic:
        return set_probabilistic(non_probabilistic, True)
    return non_probabilistic


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.plp.*")
