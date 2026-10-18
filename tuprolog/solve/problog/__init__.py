"""ProbLog solvers: probabilistic logic programming.

*Probabilistic logic programming* (PLP) attaches probabilities to facts and clauses: with
ProbLog's `::` operator, `0.6::heads(C).` states that each coin `C` lands heads with probability
0.6, independently of the others. The probability of a query is then the probability that it
can be proven, i.e. that the facts used by at least one of its proofs hold: with the clauses
`win :- heads(c1).` and `win :- heads(c2).`, `win` has probability 1 - 0.4 * 0.4 = 0.84.
ProbLog solvers compute it by compiling the proofs into a *binary decision diagram* (BDD).

ProbLog solvers extend Prolog solvers: knowledge bases with probabilistic clauses must be parsed
with `PROBLOG_OPERATORS`, which add `::` to Prolog's operators, and probabilities are computed only
when solving with the probabilistic option (`tuprolog.solve.solve_options(probabilistic=True)`);
otherwise, solvers behave as Prolog ones and ignore probabilities. Probabilities are read with
`tuprolog.solve.plp.probability`. Annotations follow ProbLog's syntax, including `evidence/2` for
facts known to be true or false.

Main functions and constants:

- `problog_solver`: creates a ProbLog solver;
- `PROBLOG_SOLVER_FACTORY`: the factory of ProbLog solvers;
- `PROBLOG_OPERATORS`, `PROBLOG_SPECIFIC_OPERATORS`, `ANNOTATION_OPERATOR`: ProbLog's operators.

Examples:
    >>> from tuprolog.solve import solve_options
    >>> from tuprolog.solve.plp import probability
    >>> from tuprolog.theory.parsing import parse_theory
    >>> kb = parse_theory(
    ...     "0.6::heads(C). win :- heads(c1). win :- heads(c2).", PROBLOG_OPERATORS
    ... )
    >>> solver = problog_solver(static_kb=kb)
    >>> [round(probability(s), 2) for s in solver.solve("win", solve_options(probabilistic=True))]
    [0.84]

See Also:
    - `tuprolog.solve.plp`, for the probabilities of solutions and the probabilistic option.
    - `tuprolog.solve.prolog`, the non-probabilistic solvers.
    - [ProbLog](https://dtai.cs.kuleuven.be/problog/), the language these solvers implement.
"""

from ._api import *
from ._definitions import *

__all__ = [
    "ANNOTATION_OPERATOR",
    "PROBLOG_OPERATORS",
    "PROBLOG_SOLVER_FACTORY",
    "PROBLOG_SPECIFIC_OPERATORS",
    "Operators",
    "problog_solver",
]
