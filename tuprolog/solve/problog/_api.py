from tuprolog.solve import Solver, channel
from tuprolog.solve.channel import InputChannel, OutputChannel
from tuprolog.solve.flags import DEFAULT_FLAG_STORE, FlagStore
from tuprolog.solve.library import Library, Runtime, libraries
from tuprolog.theory import Theory, mutable_theory, theory
from tuprolog.unify import Unificator

from ._definitions import PROBLOG_SOLVER_FACTORY

__all__ = ["problog_solver"]


def problog_solver(
    unificator: Unificator | None = None,
    libraries: Runtime | Library | None = None,
    flags: FlagStore = DEFAULT_FLAG_STORE,
    static_kb: Theory | None = None,
    dynamic_kb: Theory | None = None,
    std_in: InputChannel | None = None,
    std_out: OutputChannel | None = None,
    std_err: OutputChannel | None = None,
    warning: OutputChannel | None = None,
    mutable: bool = True,
) -> Solver:
    args = (
        Unificator.getDefault() if unificator is None else unificator,
        _runtime(libraries),
        flags,
        theory() if static_kb is None else static_kb,
        mutable_theory() if dynamic_kb is None else dynamic_kb,
        channel.std_in() if std_in is None else std_in,
        channel.std_out() if std_out is None else std_out,
        channel.std_err() if std_err is None else std_err,
        channel.warn() if warning is None else warning,
    )
    if mutable:
        return PROBLOG_SOLVER_FACTORY.mutableSolverWithDefaultBuiltins(*args)
    else:
        return PROBLOG_SOLVER_FACTORY.solverWithDefaultBuiltins(*args)


def _runtime(libs: Runtime | Library | None) -> Runtime:
    if libs is None:
        return libraries()
    if isinstance(libs, Library):
        return Runtime.of(libs)
    return libs
