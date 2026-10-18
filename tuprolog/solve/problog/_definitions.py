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


Operators = _problog.Operators


ANNOTATION_OPERATOR = Operators.ANNOTATION_OPERATOR


PROBLOG_SPECIFIC_OPERATORS = Operators.PROBLOG_SPECIFIC_OPERATORS


PROBLOG_OPERATORS = Operators.PROBLOG_OPERATORS


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.problog.*")
