"""Solving logic queries: solvers, solutions, and the options of a resolution.

A *solver* answers *queries* (or *goals*), i.e. logic terms such as `parent(abe, X)`, against a
*knowledge base* (KB) of clauses, following some resolution strategy: Prolog's SLD resolution
(`tuprolog.solve.prolog`), or probabilistic logic programming (`tuprolog.solve.problog`).
Each answer is a `Solution`, of one of three kinds:

- **yes**: the query holds, for the variable bindings in its `substitution` (e.g. `X = homer`);
- **no**: the query does not hold (or has no more answers);
- **halt**: resolution stopped because of an error (e.g. a logic `type_error`), carried by the
  solution's `exception`.

A query may have zero, one, or many (even infinitely many) solutions, which solvers compute
*lazily*, i.e. one at a time, while the caller iterates over them.

Solvers have two knowledge bases: the *static* one, which queries cannot change, and the
*dynamic* one, which predicates like `assertz/1` and `retract/1` change during resolution.
Solvers also hold *libraries* of predicates and functions (`tuprolog.solve.library`), *flags*
configuring their behaviour (`tuprolog.solve.flags`), *operators* (`tuprolog.core.operators`),
and *channels* for input and output (`tuprolog.solve.channel`).

Main types and functions:

- `Solver`: solves queries, via `query` (Pythonic), `solve` and `solve_once`;
  `MutableSolver` can also be reconfigured (e.g. loading clauses) between queries;
- `Solution`: the answers of a solver;
- `solve_options` (`SolveOptions`): laziness, timeout and maximum number of solutions;
- `signature` (`Signature`): the name and arity identifying a predicate or function.

Solvers are created by the factories of their resolution strategy, e.g.
`tuprolog.solve.prolog.prolog_solver`.

Examples:
    Querying a solver the Pythonic way, with `Solver.query`, which yields the variable bindings of
    each solution as Python values, and raises the error of a halted resolution:

    >>> from tuprolog.solve.prolog import prolog_solver
    >>> from tuprolog.theory.parsing import parse_theory
    >>> solver = prolog_solver(static_kb=parse_theory("parent(abe, homer). parent(homer, bart)."))
    >>> for bindings in solver.query("parent(X, Y)"):
    ...     print(bindings)
    {'X': 'abe', 'Y': 'homer'}
    {'X': 'homer', 'Y': 'bart'}

    Getting the first solution only, with `Solver.solve_once`: solutions are truthy if they are
    *yes*, and map variable names to the terms bound to them.

    >>> solution = solver.solve_once("parent(abe, Who)")
    >>> solution.is_yes, bool(solution)
    (True, True)
    >>> solution["Who"]
    homer
    >>> solution.solved_query
    parent(abe, homer)
    >>> solver.solve_once("parent(bart, _)").is_no
    True

    Iterating over all the `Solution`s, with `Solver.solve`, including the *no* or *halt* that may
    end them:

    >>> for solution in solver.solve("parent(X, Y)", solve_options(limit=1)):
    ...     print(solution.to_dict())
    {'X': 'abe', 'Y': 'homer'}
    >>> halted = solver.solve_once("X is foo + 1")
    >>> halted.is_halt
    True
    >>> halted.exception.type
    type_error(evaluable, foo/0)

See Also:
    - `tuprolog.solve.prolog` and `tuprolog.solve.problog`, the solvers.
    - `tuprolog.solve.library`, `tuprolog.solve.primitive` and `tuprolog.solve.function`, to
      extend solvers with predicates and functions written in Python.
    - `tuprolog.solve.exception`, the errors halting resolutions.
    - 2P-Kt's [solver API](https://tuprolog.github.io/2p-kt/reference/solver-api/) and
      [solver design](https://tuprolog.github.io/2p-kt/explanation/solver-design/).
"""

import tuprolog.solve._adapters as _

from ._api import *
from ._definitions import *

__all__ = [
    "ALL_SOLUTIONS",
    "MAX_TIMEOUT",
    "Durable",
    "ExecutionContext",
    "ExecutionContextAware",
    "MutableSolver",
    "Signature",
    "Solution",
    "SolutionFormatter",
    "SolveOptions",
    "Solver",
    "SolverBuilder",
    "SolverFactory",
    "Time",
    "current_time_instant",
    "halt_solution",
    "no_solution",
    "signature",
    "solution_formatter",
    "solve_options",
    "yes_solution",
]
