"""The JVM types and constants of ProbLog solvers, re-exported by `tuprolog.solve.problog`."""

import it.unibo.tuprolog.solve.problog as _problog  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger
from tuprolog.solve import Solver, SolverFactory

__all__ = [
    "ANNOTATION_OPERATOR",
    "PROBLOG_OPERATORS",
    "PROBLOG_SOLVER_FACTORY",
    "PROBLOG_SPECIFIC_OPERATORS",
    "Operators",
]


PROBLOG_SOLVER_FACTORY: SolverFactory = Solver.problog()
"""The factory of ProbLog solvers (2P-Kt's `Solver.problog`), see `tuprolog.solve.SolverFactory`.

Its solvers always load ProbLog's library, and turn the `track_variables` flag on, as computing
probabilities requires it. `tuprolog.solve.problog.problog_solver` is a simpler way to create
solvers.
"""


Operators = _problog.Operators
"""The JVM class holding ProbLog's operators, also re-exported as module constants.

Its static fields are `ANNOTATION_FUNCTOR` (`::`), `ANNOTATION_OPERATOR`,
`PROBLOG_SPECIFIC_OPERATORS` and `PROBLOG_OPERATORS`.
"""


ANNOTATION_OPERATOR = Operators.ANNOTATION_OPERATOR
"""ProbLog's probability annotation, `::`: an infix, right-associative (`xfy`) operator, priority 900.

Its priority is lower than the one of `:-`, so that `0.3::a :- b.` reads as `(0.3::a) :- b.`

Examples:
    >>> ANNOTATION_OPERATOR
    Operator(900, XFY, '::')
"""


PROBLOG_SPECIFIC_OPERATORS = Operators.PROBLOG_SPECIFIC_OPERATORS
"""The operators ProbLog adds to Prolog's, i.e. only `ANNOTATION_OPERATOR` (an `OperatorSet`)."""


PROBLOG_OPERATORS = Operators.PROBLOG_OPERATORS
"""ProbLog's operators: Prolog's standard ones, plus `ANNOTATION_OPERATOR` (an `OperatorSet`).

Parse probabilistic knowledge bases and queries with them, e.g.
`tuprolog.theory.parsing.parse_theory(text, PROBLOG_OPERATORS)`.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.problog.*")
