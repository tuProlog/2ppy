"""System errors: internal problems, e.g. exceptions raised by the code implementing predicates.

ISO Prolog's `system_error` error, thrown as `error(system_error, Extra)`, reports problems of the
implementation rather than of the program: in this library, notably, exceptions raised by Python
primitives that are not logic errors (see `tuprolog.solve.primitive.python_error`), and terms
thrown by `throw/1` that no `catch/3` caught. Prolog code can still catch them.

The error is a `SystemError` (the JVM class: import it explicitly, as it shadows Python's built-in
name). Build errors with `system_error`.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> error = prolog_solver().solve_once("throw(oops)").get_exception()
    >>> error.type, error.message
    (system_error, 'Uncaught exception `oops`')

See Also:
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._api import *
from ._definitions import *
from ._definitions import SystemError  # not in __all__, as star-imports would shadow the builtin

__all__ = ["system_error"]
