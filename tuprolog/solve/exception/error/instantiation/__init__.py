"""Instantiation errors: an argument is an unbound variable, where a value is needed.

ISO Prolog's `instantiation_error` error, thrown as `error(instantiation_error, Extra)`, means
that a predicate received an unbound variable where it needs a (more) instantiated term: e.g.
`X is Y + 1` cannot compute `Y + 1`, and `atom_length(X, L)` cannot measure `X`.

The error is an `InstantiationError`. Build errors with `instantiation_error_for_argument` (for
primitives' arguments) or `instantiation_error_for_goal`.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> prolog_solver().solve_once("catch(X is Y + 1, error(E, _), true)")["E"]
    instantiation_error

See Also:
    `tuprolog.solve.primitive`, whose `ensuring_*` checks raise these errors;
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._api import *
from ._definitions import *

__all__ = ["InstantiationError", "instantiation_error_for_argument", "instantiation_error_for_goal"]
