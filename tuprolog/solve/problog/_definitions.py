from tuprolog import logger
from tuprolog.solve import Solver, SolverFactory
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.problog as _problog  # type: ignore


PROBLOG_SOLVER_FACTORY : SolverFactory = Solver.problog()


Operators = _problog.Operators


ANNOTATION_OPERATOR = Operators.ANNOTATION_OPERATOR


PROBLOG_SPECIFIC_OPERATORS = Operators.PROBLOG_SPECIFIC_OPERATORS


PROBLOG_OPERATORS = Operators.PROBLOG_OPERATORS


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.problog.*")
