"""The functions of probabilistic logic programming, re-exported by `tuprolog.solve.plp`."""

from typing import Any, TypeVar

from tuprolog.solve import (
    Solution,
    SolveOptions,
    solve_options,  # re-exported, see its probabilistic argument
)
from tuprolog.utils import Taggable

from ._definitions import ProbExtensions

__all__ = [
    "binary_decision_diagram",
    "has_binary_decision_diagram",
    "is_probabilistic",
    "probabilistic",
    "probability",
    "set_binary_decision_diagram",
    "set_probabilistic",
    "set_probability",
    "solve_options",
]


def probability(taggable: Taggable) -> float:
    """Returns the probability of a term or solution.

    Args:
        taggable: A taggable object, e.g. a `tuprolog.core.Term`, or a `Solution` of a
            probabilistic solver solving with the probabilistic option.

    Returns:
        The probability set with `set_probability` (or computed by a solver), or 1.0 if none was.

    Examples:
        >>> from tuprolog.core import atom
        >>> probability(atom("a"))
        1.0
    """
    return ProbExtensions.getProbability(taggable)


_T = TypeVar("_T", bound=Taggable)


def set_probability(taggable: _T, value: float) -> _T:
    """Returns a copy of a term or solution with the given probability.

    Args:
        taggable: A taggable object, e.g. a `tuprolog.core.Term`, left unchanged.
        value: The probability, clamped between 0.0 and 1.0.

    Returns:
        A copy of `taggable` whose `probability` is `value`.

    Examples:
        >>> from tuprolog.core import atom
        >>> probability(set_probability(atom("a"), 0.3))
        0.3
        >>> probability(set_probability(atom("a"), 1.5))
        1.0
    """
    return ProbExtensions.setProbability(taggable, value)


def is_probabilistic(solve_opts: SolveOptions) -> bool:
    """Returns whether solve options ask for probabilities to be computed (`False` by default).

    Args:
        solve_opts: The solve options.

    Returns:
        Whether the probabilistic option is on.

    Examples:
        >>> is_probabilistic(solve_options()), is_probabilistic(solve_options(probabilistic=True))
        (False, True)
    """
    return ProbExtensions.isProbabilistic(solve_opts)


def set_probabilistic(solve_opts: SolveOptions, value: bool) -> SolveOptions:
    """Returns a copy of solve options with the probabilistic option set to `value`.

    Args:
        solve_opts: The solve options, left unchanged.
        value: Whether solvers should compute the probabilities of solutions.

    Returns:
        The new solve options.
    """
    return ProbExtensions.setProbabilistic(solve_opts, value)


def probabilistic(solve_opts: SolveOptions) -> SolveOptions:
    """Returns a copy of solve options with the probabilistic option on.

    Args:
        solve_opts: The solve options, left unchanged.

    Returns:
        The new solve options, like `set_probabilistic(solve_opts, True)`.

    Examples:
        >>> is_probabilistic(probabilistic(solve_options(limit=1)))
        True
    """
    return ProbExtensions.probabilistic(solve_opts)


def has_binary_decision_diagram(solution: Solution) -> bool:
    """Returns whether a solution has a binary decision diagram explaining its probability.

    Only probabilistic solvers, solving with the probabilistic option, attach one.

    Args:
        solution: The solution.

    Returns:
        Whether `binary_decision_diagram(solution)` is not `None`.
    """
    return ProbExtensions.getHasBinaryDecisionDiagram(solution)


def binary_decision_diagram(solution: Solution) -> Any:
    """Returns the binary decision diagram (BDD) explaining the probability of a solution.

    A BDD is a compact representation of a Boolean formula: here, the formula over the
    probabilistic facts that holds exactly when the solution can be proven.

    Args:
        solution: The solution.

    Returns:
        The JVM `it.unibo.tuprolog.bdd.BinaryDecisionDiagram`, or `None` if the solution has none
        (see `has_binary_decision_diagram`).
    """
    return ProbExtensions.getBinaryDecisionDiagram(solution)


def set_binary_decision_diagram(solution: Solution, bdd: Any) -> Solution:
    """Returns a copy of a solution with the given binary decision diagram.

    Args:
        solution: The solution, left unchanged.
        bdd: The JVM `it.unibo.tuprolog.bdd.BinaryDecisionDiagram`.

    Returns:
        The new solution.
    """
    return ProbExtensions.setBinaryDecisionDiagram(solution, bdd)
