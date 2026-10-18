"""Probabilistic logic programming: probabilities of terms and solutions, probabilistic option.

In *probabilistic logic programming* (PLP), clauses are annotated with probabilities, and the
solutions of queries come with the probability that they hold (see `tuprolog.solve.problog`).
This package holds the vocabulary shared by probabilistic solvers, attached to the plain types of
`tuprolog.solve` as *tags* (see `tuprolog.utils.Taggable`):

- `probability` and `set_probability`: the probability of a term or solution (1.0 if unset);
- `is_probabilistic`, `set_probabilistic` and `probabilistic`: the option asking solvers to
  compute probabilities, also set by `solve_options(probabilistic=True)`;
- `binary_decision_diagram` and siblings: the binary decision diagram (BDD) of a solution, i.e.
  the Boolean formula over probabilistic facts explaining it, from which its probability is
  computed.

Solvers not supporting PLP ignore the probabilistic option, so their solutions have
probability 1.0.

Examples:
    >>> from tuprolog.solve.problog import PROBLOG_OPERATORS, problog_solver
    >>> from tuprolog.theory.parsing import parse_theory
    >>> solver = problog_solver(static_kb=parse_theory("0.2::a.", PROBLOG_OPERATORS))
    >>> solution = solver.solve_once("a", solve_options(probabilistic=True))
    >>> probability(solution), has_binary_decision_diagram(solution)
    (0.2, True)

See Also:
    - `tuprolog.solve.problog`, the probabilistic solvers.
"""

from ._api import *
from ._definitions import *

__all__ = [
    "ProbExtensions",
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
