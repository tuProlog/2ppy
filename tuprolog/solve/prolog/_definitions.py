"""The JVM factory of Prolog solvers, re-exported by `tuprolog.solve.prolog`."""

from tuprolog import logger
from tuprolog.solve import Solver, SolverFactory

__all__ = ["PROLOG_SOLVER_FACTORY"]


PROLOG_SOLVER_FACTORY: SolverFactory = Solver.prolog()
"""The factory of Prolog solvers (2P-Kt's `Solver.prolog`), see `tuprolog.solve.SolverFactory`.

Its `default_builtins` is the library of ISO Prolog predicates and functions, `prolog.lang`.
`tuprolog.solve.prolog.prolog_solver` is a simpler way to create solvers.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.prolog.*")
