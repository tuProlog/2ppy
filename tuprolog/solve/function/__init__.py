"""Logic functions: functions evaluated in arithmetic expressions, e.g. by `is/2`.

Prolog evaluates arithmetic expressions only in some predicates, e.g. `X is 1 + 2` or `X > 2`:
elsewhere, `1 + 2` is just a term. Each operation in an expression (e.g. `+/2`, `sqrt/1`) is a
*logic function*, receiving the (evaluated) arguments, and returning a term. The standard ones
are in `tuprolog.solve.stdlib.function`; libraries add others (see `tuprolog.solve.library`).

Functions receive a *compute request* (`ComputeRequest`: the function's `signature`, its
`arguments`, and the solver's `context`), and return a *compute response* (`ComputeResponse`,
holding the `result`).

Main types and functions:

- `function`: creates a logic function from a Python function on Python values;
- `logic_function`: creates a logic function from a Python function on requests;
- `LogicFunction`, `ComputeRequest`, `ComputeResponse`, `AbstractLogicFunction`;
- `eval_as_expression` and `eval_as_arithmetic_expression`: evaluate expressions in primitives.

Examples:
    >>> from tuprolog.solve.library import library
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> hypot = function(lambda x, y: (x**2 + y**2) ** 0.5)
    >>> solver = prolog_solver(libraries=library("my.math", functions={"hypot/2": hypot}))
    >>> solver.solve_once("X is hypot(3, 4) + 1")["X"]
    6.0

See Also:
    - 2P-Kt's [primitives and functions](
      https://tuprolog.github.io/2p-kt/reference/primitives-and-functions/).
"""

from ._api import *
from ._definitions import *

__all__ = [
    "AbstractLogicFunction",
    "ArithmeticUtilsKt",
    "Compute",
    "ComputeRequest",
    "ComputeResponse",
    "LogicFunction",
    "compute_request",
    "compute_response",
    "eval_as_arithmetic_expression",
    "eval_as_expression",
    "function",
    "logic_function",
]
