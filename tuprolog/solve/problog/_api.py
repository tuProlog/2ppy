from io import IOBase

from tuprolog.solve import Solver
from tuprolog.solve.channel import (
    InputChannel,
    OutputChannel,
    ensure_input_channel,
    ensure_output_channel,
    warn,
)
from tuprolog.solve.channel import std_err as _std_err
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
    std_in: InputChannel | IOBase | None = None,
    std_out: OutputChannel | IOBase | None = None,
    std_err: OutputChannel | IOBase | None = None,
    warning: OutputChannel | IOBase | None = None,
    mutable: bool = True,
) -> Solver:
    args = (
        Unificator.getDefault() if unificator is None else unificator,
        _runtime(libraries),
        flags,
        theory() if static_kb is None else static_kb,
        mutable_theory() if dynamic_kb is None else dynamic_kb,
        ensure_input_channel(std_in),
        ensure_output_channel(std_out),
        ensure_output_channel(std_err, _std_err),
        ensure_output_channel(warning, warn),
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
