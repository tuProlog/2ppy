from tuprolog import logger
from tuprolog.solve import Solver, SolverFactory

__all__ = ["PROLOG_SOLVER_FACTORY"]


PROLOG_SOLVER_FACTORY: SolverFactory = Solver.prolog()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.prolog.*")
