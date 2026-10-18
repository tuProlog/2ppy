"""The factory function of ProbLog solvers, re-exported by `tuprolog.solve.problog`."""

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
    """Creates a ProbLog solver, i.e. a Prolog solver also computing probabilities.

    Probabilities are computed only when solving with the probabilistic option (see
    `tuprolog.solve.solve_options` and `tuprolog.solve.plp`); otherwise, the solver behaves as a
    Prolog one, finding one solution per proof, and ignoring probabilities.

    Args:
        unificator: The unification algorithm; by default, the standard one (see
            `tuprolog.unify`).
        libraries: Further libraries of predicates and functions (a `Library`, or a `Runtime` of
            several ones, see `tuprolog.solve.library`), loaded on top of the standard ones.
        flags: The flags (see `tuprolog.solve.flags`); by default, `DEFAULT_FLAG_STORE`.
        static_kb: The static knowledge base, i.e. the clauses queries cannot change, parsed
            with `PROBLOG_OPERATORS` if probabilistic; empty by default.
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
        The ProbLog solver.

    Examples:
        >>> from tuprolog.solve import solve_options
        >>> from tuprolog.solve.plp import probability
        >>> from tuprolog.solve.problog import PROBLOG_OPERATORS
        >>> from tuprolog.theory.parsing import parse_theory
        >>> kb = parse_theory(
        ...     "0.3::rain. 0.5::sprinkler. wet :- rain. wet :- sprinkler.", PROBLOG_OPERATORS
        ... )
        >>> solver = problog_solver(static_kb=kb)
        >>> solution = next(iter(solver.solve("wet", solve_options(probabilistic=True))))
        >>> round(probability(solution), 2)
        0.65
        >>> list(solver.query("wet"))  # not probabilistic: one solution per proof
        [{}, {}]

    Note:
        `solve_once` stops at the first proof, so the probability of its solution only accounts
        for that proof: use `solve` to get the probability of a query.
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
        return PROBLOG_SOLVER_FACTORY.mutableSolverWithDefaultBuiltins(*args)
    else:
        return PROBLOG_SOLVER_FACTORY.solverWithDefaultBuiltins(*args)


def _runtime(libs: Runtime | Library | None) -> Runtime:
    if libs is None:
        return libraries()
    if isinstance(libs, Library):
        return Runtime.of(libs)
    return libs
