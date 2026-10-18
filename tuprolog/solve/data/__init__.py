"""Custom data: values that libraries and programs attach to the state of a solver.

Primitives and Prolog programs can store arbitrary values, by key, in the state of a solver
(its `tuprolog.solve.ExecutionContext`), in three tiers, by how long values survive:

- *persistent* data lives as long as the solver, i.e. across queries;
- *durable* data lives during a query, longer than ephemeral data;
- *ephemeral* data is the first to be discarded, e.g. at each resolution step.

Prolog programs read and write them with `get_persistent/2` and `set_persistent/2` (and the
`durable` and `ephemeral` variants); primitives with the side effects of
`tuprolog.solve.sideffects` (e.g. `set_persistent_data`).

Main types and functions:

- `CustomData`: a JVM map from keys (strings) to values, created by `custom_data`;
- `CustomDataStore`: the three tiers of a solver, created by `custom_data_store`;
- `EMPTY_DATA` and `EMPTY_DATA_STORE`.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> solver = prolog_solver()
    >>> solver.solve_once("set_persistent(counter, 1)").is_yes
    True
    >>> solver.solve_once("get_persistent(counter, Value)")["Value"]
    1
"""

from ._api import *
from ._definitions import *

__all__ = [
    "EMPTY_DATA",
    "EMPTY_DATA_STORE",
    "CustomData",
    "CustomDataStore",
    "custom_data",
    "custom_data_store",
]
