from tuprolog import logger
from tuprolog.solve.flags import DEFAULT_FLAG_STORE, FlagStore
from tuprolog.solve.library import libraries, Library, Runtime
from tuprolog.solve.channel import InputChannel, OutputChannel, std_out, std_in, std_err, warn
from tuprolog.theory import theory, mutable_theory, Theory, Unificator
from tuprolog.solve import Solver, SolverFactory


_PROBLOG_SOLVER_FACTORY = Solver.problog()


def problog_solver(
        unificator: Unificator = Unificator.getDefault(),
        libraries: Library = libraries(),
        flags: FlagStore = DEFAULT_FLAG_STORE,
        static_kb: Theory = theory(),
        dynamic_kb: Theory = mutable_theory(),
        std_in: InputChannel = std_in(),
        std_out: OutputChannel = std_out(),
        std_err: OutputChannel = std_err(),
        warning: OutputChannel = warn(),
        mutable: bool = True
) -> Solver:
    if mutable:
        return _PROBLOG_SOLVER_FACTORY.mutableSolverWithDefaultBuiltins(
            unificator, Runtime.of(libraries), flags, static_kb, dynamic_kb, std_in, std_out, std_err, warning
        )
    else:
        return _PROBLOG_SOLVER_FACTORY.solverWithDefaultBuiltins(
            unificator, Runtime.of(libraries), flags, static_kb, dynamic_kb, std_in, std_out, std_err, warning
        )


def problog_solver_factory() -> SolverFactory:
    return _PROBLOG_SOLVER_FACTORY


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.problog.*")
