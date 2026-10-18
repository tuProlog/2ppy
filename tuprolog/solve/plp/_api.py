from typing import TypeVar

from tuprolog.solve import (
    SolveOptions,
    solve_options,  # re-exported, see its probabilistic argument
)
from tuprolog.utils import Taggable

from ._definitions import ProbExtensions

__all__ = [
    "is_probabilistic",
    "probabilistic",
    "probability",
    "set_probabilistic",
    "set_probability",
    "solve_options",
]


def probability(taggable: Taggable) -> float:
    return ProbExtensions.getProbability(taggable)


_T = TypeVar("_T", bound=Taggable)


def set_probability(taggable: _T, value: float) -> _T:
    return ProbExtensions.setProbability(taggable, value)


def is_probabilistic(solve_opts: SolveOptions) -> bool:
    return ProbExtensions.isProbabilistic(solve_opts)


def set_probabilistic(solve_opts: SolveOptions, value: bool) -> SolveOptions:
    return ProbExtensions.setProbabilistic(solve_opts, value)


def probabilistic(solve_opts: SolveOptions) -> SolveOptions:
    return ProbExtensions.probabilistic(solve_opts)
