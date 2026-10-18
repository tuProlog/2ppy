"""Warnings: non-fatal problems a solver reports while solving, without stopping.

Some problems do not deserve to end a query with an error: e.g., by default, calling an
undefined predicate just fails (as the `unknown` flag is `warning`), and a failing initialization
directive does not prevent loading the rest of a theory. Solvers report such problems as
**warnings** (`tuprolog.solve.exception.Warning`s) on their warnings output channel, which prints
their messages on `sys.stderr` by default (pass `warning=...` to the solver factories, e.g.
`tuprolog.solve.prolog.prolog_solver`, to handle them otherwise).

Types: `MissingPredicate` and `InitializationIssue`, built by `missing_predicate` and
`initialization_issue`.

Examples:
    >>> from tuprolog.solve.channel import output_channel
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> warnings = []
    >>> solver = prolog_solver(warning=output_channel(warnings.append))
    >>> solver.solve_once("undefined").is_no
    True
    >>> [warning.message for warning in warnings]
    ['No such a predicate: undefined/0']

See Also:
    `tuprolog.solve.exception`, for the other exceptions;
    `tuprolog.solve.flags`, for the `unknown` flag;
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._api import *
from ._definitions import *

__all__ = ["InitializationIssue", "MissingPredicate", "initialization_issue", "missing_predicate"]
