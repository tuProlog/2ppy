"""Prolog solvers: SLD resolution, as in ISO Prolog.

Prolog solvers prove a goal by *SLD resolution*: they try the clauses whose head unifies with
the goal, in the order they appear in the knowledge base, proving the goals in each clause's
body from left to right, and *backtracking* to the next alternative upon failure; each proof
found is a solution. Negation is *negation as failure* (`\\+ G` holds if `G` cannot be proven).

Prolog solvers come with the standard library of ISO Prolog predicates and functions (e.g.
`member/2`, `findall/3`, `assertz/1`, `is/2`, see `tuprolog.solve.stdlib`), and load further
libraries on request (e.g. `tuprolog.solve.libs.io` and `tuprolog.solve.libs.oop`).

Main functions and constants:

- `prolog_solver`: creates a Prolog solver;
- `PROLOG_SOLVER_FACTORY`: the factory of Prolog solvers (a `tuprolog.solve.SolverFactory`).

Examples:
    >>> from tuprolog.theory.parsing import parse_theory
    >>> kb = parse_theory(
    ...     "parent(abe, homer). parent(homer, bart). "
    ...     "ancestor(X, Y) :- parent(X, Y). "
    ...     "ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z)."
    ... )
    >>> solver = prolog_solver(static_kb=kb)
    >>> [solution["Y"] for solution in solver.solve("ancestor(abe, Y)") if solution]
    [homer, bart]

See Also:
    - `tuprolog.solve`, for querying solvers and handling solutions.
    - `tuprolog.solve.problog`, for probabilistic logic programming.
    - 2P-Kt's [solver API](https://tuprolog.github.io/2p-kt/reference/solver-api/) and
      [state machine](https://tuprolog.github.io/2p-kt/explanation/state-machine/) of its Prolog
      solver.
"""

from ._api import prolog_solver
from ._definitions import PROLOG_SOLVER_FACTORY

__all__ = ["PROLOG_SOLVER_FACTORY", "prolog_solver"]
