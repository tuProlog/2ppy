from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve as _solve  # type: ignore


Durable = _solve.Durable


ExecutionContext = _solve.ExecutionContext


ExecutionContextAware = _solve.ExecutionContextAware


MutableSolver = _solve.MutableSolver


Signature = _solve.Signature


Solution = _solve.Solution


SolutionFormatter = _solve.SolutionFormatter


SolveOptions = _solve.SolveOptions


Solver = _solve.Solver


SolverBuilder = _solve.SolverBuilder


SolverFactory = _solve.SolverFactory


Time = _solve.Time


MAX_TIMEOUT: int = SolveOptions.MAX_TIMEOUT


ALL_SOLUTIONS: int = SolveOptions.ALL_SOLUTIONS


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.*")
