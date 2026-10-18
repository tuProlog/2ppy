"""Message errors: the errors carrying an arbitrary thrown term, fitting no ISO error family.

When Prolog code throws a term that is not an ISO `error(Type, Extra)` one (e.g.
`throw(my_problem)`), or a primitive needs to throw a custom term, 2P-Kt represents it as a
`MessageError`, whose `content` is the thrown term. Catching it in Prolog unifies the catcher
with that very term.

Build them with `message_error`.

Examples:
    >>> from tuprolog.core import atom
    >>> from tuprolog.solve.library import library
    >>> from tuprolog.solve.primitive import primitive
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> def complain(request):
    ...     raise message_error(atom("my_problem"), request.context)
    >>> lib = library("demo", primitives={"complain/0": primitive(complain)})
    >>> solver = prolog_solver(libraries=lib)
    >>> solver.solve_once("catch(complain, E, true)")["E"]
    my_problem

See Also:
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._api import *
from ._definitions import *

__all__ = ["MessageError", "message_error"]
