"""The factory function of Prolog solvers, re-exported by `tuprolog.solve.prolog`."""

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

from ._definitions import PROLOG_SOLVER_FACTORY

__all__ = ["prolog_solver"]


def prolog_solver(
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
    """Creates a Prolog solver, with the standard library of ISO Prolog predicates and functions.

    Args:
        unificator: The unification algorithm; by default, the standard one (see
            `tuprolog.unify`).
        libraries: Further libraries of predicates and functions (a `Library`, or a `Runtime` of
            several ones, see `tuprolog.solve.library`), loaded on top of the standard ones.
        flags: The flags (see `tuprolog.solve.flags`); by default, `DEFAULT_FLAG_STORE`.
        static_kb: The static knowledge base, i.e. the clauses queries cannot change; empty by
            default.
        dynamic_kb: The dynamic knowledge base, i.e. the clauses that predicates like
            `assertz/1` and `retract/1` change; empty by default.
        std_in: The standard input: an `InputChannel`, a Python stream, or a callable returning a
            string per call (`None` at the end); by default, Python's `sys.stdin`.
        std_out: The standard output, where `write/1` writes: an `OutputChannel`, a Python
            stream, or a callable taking each string; by default, Python's `sys.stdout`.
        std_err: The standard error, like `std_out`; by default, Python's `sys.stderr`.
        warning: Where warnings go (e.g. about calls to unknown predicates): an `OutputChannel`,
            a Python stream (receiving their messages), or a callable taking each
            `tuprolog.solve.exception.Warning`; by default, Python's `sys.stderr`.
        mutable: Whether to create a `tuprolog.solve.MutableSolver`, whose state Python code can
            change between queries (the default), or a plain `tuprolog.solve.Solver`.

    Returns:
        The Prolog solver.

    Examples:
        >>> import io
        >>> from tuprolog.solve.flags import flag_store
        >>> from tuprolog.theory.parsing import parse_theory
        >>> output = io.StringIO()
        >>> solver = prolog_solver(
        ...     static_kb=parse_theory("greet(Name) :- write(hello), write(' '), write(Name)."),
        ...     flags=flag_store(unknown="fail"),
        ...     std_out=output,
        ... )
        >>> solver.solve_once("greet(world)").is_yes
        True
        >>> output.getvalue()
        'hello world'
        >>> solver.solve_once("undefined_predicate").is_no
        True

    Note:
        Wraps 2P-Kt's `SolverFactory.mutableSolverWithDefaultBuiltins` and
        `solverWithDefaultBuiltins`, of `Solver.prolog`.
    """
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
        return PROLOG_SOLVER_FACTORY.mutableSolverWithDefaultBuiltins(*args)
    else:
        return PROLOG_SOLVER_FACTORY.solverWithDefaultBuiltins(*args)


def _runtime(libs: Runtime | Library | None) -> Runtime:
    if libs is None:
        return libraries()
    if isinstance(libs, Library):
        return Runtime.of(libs)
    return libs
