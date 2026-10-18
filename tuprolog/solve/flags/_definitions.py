"""The JVM types and constants of Prolog flags, re-exported by `tuprolog.solve.flags`."""

import it.unibo.tuprolog.solve.flags as _flags  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger
from tuprolog.jvmutils import Pair

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
]


FlagStore = _flags.FlagStore
"""An immutable set of flags: a JVM map from flag names (strings) to values (terms).

Changes return new stores: `set(name, value)`, `plus(...)` (a flag, a notable flag set to its
default value, or another store), `minus(...)` (names). Python additions:

- `len(store)`, `name in store` (also for notable flags), and the JVM map's `keys()`, `values()`
  and `items()`;
- `store[name]` (also for notable flags) returns the value of a flag, or `None` if there is none;
- `store + other` merges a `Flag`, a `NotableFlag`, another store, or a dict from names to terms
  (later values override earlier ones); `store - name` removes a flag (also a notable one).

Create stores with `flag_store`, or start from `DEFAULT_FLAG_STORE` or `EMPTY_FLAG_STORE`.

Examples:
    >>> from tuprolog.core import atom
    >>> store = EMPTY_FLAG_STORE + Unknown + {"my_flag": atom("on")}
    >>> len(store), "unknown" in store, store[Unknown]
    (2, True, warning)
    >>> print(store["missing"])
    None
    >>> store - "my_flag"
    FlagStore(flags={unknown=warning})
"""


NotableFlag = _flags.NotableFlag
"""A flag known to solvers, whose admissible values and default value are known in advance.

Members: `name`, `default_value`, `admissible_values` (a set of terms), `is_admissible_value(term)`,
`is_editable` (whether programs can change it), `help` (a description), `to_pair()` (the `Flag`
setting it to its default value), and `to(value)` (the `Flag` setting it to `value`).

Examples:
    >>> Unknown.name, Unknown.default_value
    ('unknown', warning)
    >>> MaxArity.is_editable
    False
"""


Flag = Pair
"""A flag: a `(name, value)` pair, i.e. 2P-Kt's `kotlin.Pair` of a string and a term.

Its members are `first` (the name) and `second` (the value); create flags with `flag`.
"""


EMPTY_FLAG_STORE: FlagStore = FlagStore.EMPTY
"""The flag store with no flags."""


DEFAULT_FLAG_STORE: FlagStore = FlagStore.DEFAULT
"""The flag store with all the notable flags, set to their default values, which solvers use by default.

Examples:
    >>> sorted(DEFAULT_FLAG_STORE.keys())  # doctest: +NORMALIZE_WHITESPACE
    ['double_quotes', 'ground_queries_have_boolean_solution', 'last_call_optimization',
     'max_arity', 'show_wildcard_variables_in_solutions', 'track_variables', 'unique_solutions',
     'unknown']
"""


DoubleQuotes: NotableFlag = _flags.DoubleQuotes.INSTANCE
"""ISO Prolog's `double_quotes` flag: how double-quoted text is parsed.

2P-Kt only supports `atom` (its default): `"some text"` is read as an atom.
"""


GroundQueriesHaveBooleanSolution: NotableFlag = _flags.GroundQueriesHaveBooleanSolution.INSTANCE
"""The `ground_queries_have_boolean_solution` flag: how *yes* solutions of ground queries are shown.

A query is *ground* if it has no variables. If `on`, solution formatters show its *yes* solutions
as `yes.`; if `off` (the default), they also show the solved query. The solutions do not change.
"""


LastCallOptimization: NotableFlag = _flags.LastCallOptimization.INSTANCE
"""The `last_call_optimization` flag: whether solvers optimize tail calls (`on`, the default).

With the optimization, a goal calling a predicate as the last goal of a clause body does not
grow the solver's stack, so deep recursions need constant memory.
"""


MaxArity: NotableFlag = _flags.MaxArity.INSTANCE
"""ISO Prolog's `max_arity` flag: the maximum arity of predicates and functions (read-only).

2P-Kt sets no practical limit: its value is the largest JVM integer, 2147483647.
"""


ShowWildCardVariablesInSolutions: NotableFlag = _flags.ShowWildCardVariablesInSolutions.INSTANCE
"""The `show_wildcard_variables_in_solutions` flag: whether solutions bind wildcard variables.

Wildcard variables are those whose name starts with `_` (e.g. `_X`); if `off`, their bindings are
left out of the substitutions of solutions; if `on` (the default), they are kept.
"""


TrackVariables: NotableFlag = _flags.TrackVariables.INSTANCE
"""The `track_variables` flag: whether solvers keep additional information about variables.

`off` by default; ProbLog solvers turn it `on`, as they need it to compute probabilities.
"""


UniqueSolutions: NotableFlag = _flags.UniqueSolutions.INSTANCE
"""The `unique_solutions` flag: whether solvers drop duplicate *yes* solutions.

If `on`, only the first *yes* solution with a given solved query is kept (e.g. `member(X, [1, 1])`
has one solution); if `off` (the default), duplicates are kept, as in standard Prolog.
"""


Unknown: NotableFlag = _flags.Unknown.INSTANCE
"""ISO Prolog's `unknown` flag: what happens when calling a predicate that does not exist.

Its values are `error` (resolution halts with an existence error), `warning` (the default: a
warning is reported on the solver's warnings channel, and the call fails), and `fail` (the call
silently fails).

Examples:
    >>> from tuprolog.solve.flags import flag_store
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> solution = prolog_solver(flags=flag_store(unknown="error")).solve_once("undefined")
    >>> solution.is_halt
    True
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.flags.*")
