"""Operators: functors written in prefix, infix or postfix notation, e.g. `+` in `1 + 2`.

In Prolog syntax, `1 + 2 * 3` is the term `+(1, *(2, 3))`: `+` and `*` are *operators*, each with a
*priority* (the lower, the tighter it binds) and a *specifier* (its position, i.e. prefix, infix or
postfix, and associativity). Parsers (see `tuprolog.core.parsing`) and formatters (see
`tuprolog.core.TermFormatter`) consult an *operator set* to read and write such expressions;
programs can declare new operators, with the `op/3` directive.

This package offers the types `Operator`, `OperatorSet` and `Specifier`, the factories `operator`,
`operator_set` and `specifier`, the standard operator sets (`DEFAULT_OPERATORS`,
`STANDARD_OPERATORS`, `EMPTY_OPERATORS`), and the specifiers (`XFX`, `YFX`, `FY`, ...).

Examples:
    >>> from tuprolog.core.operators import DEFAULT_OPERATORS, XFX, operator, operator_set
    >>> from tuprolog.core.parsing import parse_term
    >>> operators = DEFAULT_OPERATORS + operator_set(operator("++", XFX, 700))
    >>> parse_term("a ++ b", operators)
    '++'(a, b)

See Also:
    `tuprolog.core.parsing`, for parsing terms with operators.
"""

import tuprolog.core.operators._adapters as _

from ._api import *
from ._definitions import *

__all__ = [
    "DEFAULT_OPERATORS",
    "EMPTY_OPERATORS",
    "FX",
    "FY",
    "STANDARD_OPERATORS",
    "XF",
    "XFX",
    "XFY",
    "YF",
    "YFX",
    "Operator",
    "OperatorSet",
    "Specifier",
    "operator",
    "operator_set",
    "specifier",
]
