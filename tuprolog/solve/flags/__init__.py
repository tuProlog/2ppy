"""Prolog flags: named settings configuring the behaviour of solvers.

A *flag* is a name bound to a term, e.g. `unknown` to `warning`, read and changed by Prolog
programs via `current_prolog_flag/2` and `set_prolog_flag/2`. *Notable* flags are the flags
solvers know: their admissible values and defaults are known in advance (see `NotableFlag`).
ISO Prolog defines some (`unknown`, `double_quotes`, `max_arity`), 2P-Kt others.

Main types, constants and functions:

- `FlagStore`: an immutable set of flags, by name; solvers have one (`Solver.flags`);
- `Flag`: a `(name, value)` pair;
- `NotableFlag`, and the notable flags `Unknown`, `DoubleQuotes`, `MaxArity`,
  `LastCallOptimization`, `TrackVariables`, `UniqueSolutions`,
  `ShowWildCardVariablesInSolutions`, `GroundQueriesHaveBooleanSolution`;
- `DEFAULT_FLAG_STORE`: the notable flags, with their default values; `EMPTY_FLAG_STORE`;
- `flag` and `flag_store`: create flags and flag stores.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> solver = prolog_solver(flags=flag_store(DEFAULT_FLAG_STORE, unknown="fail"))
    >>> solver.flags["unknown"]
    fail
    >>> solver.solve_once("undefined_predicate").is_no
    True
    >>> solver.solve_once("current_prolog_flag(max_arity, X)")["X"]
    2147483647

See Also:
    - `tuprolog.solve.sideffects.set_flags`, for primitives changing flags.
    - 2P-Kt's [solver design](https://tuprolog.github.io/2p-kt/explanation/solver-design/).
"""

import tuprolog.solve.flags._adapters as _

from ._api import *
from ._definitions import *

__all__ = [
    "DEFAULT_FLAG_STORE",
    "EMPTY_FLAG_STORE",
    "DoubleQuotes",
    "Flag",
    "FlagStore",
    "GroundQueriesHaveBooleanSolution",
    "LastCallOptimization",
    "MaxArity",
    "NotableFlag",
    "ShowWildCardVariablesInSolutions",
    "TrackVariables",
    "UniqueSolutions",
    "Unknown",
    "flag",
    "flag_store",
]
