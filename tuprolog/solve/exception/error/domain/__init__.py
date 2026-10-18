"""Domain errors: an argument has the right type, but a value outside the admissible ones.

ISO Prolog's `domain_error(Domain, Culprit)` error, thrown as
`error(domain_error(Domain, Culprit), Extra)`, means that `Culprit` has the right type but does
not belong to the set of values `Domain` names: e.g. `atom_length(abc, -1)` throws
`domain_error(not_less_than_zero, -1)` (an integer, but a negative one), and `open/3` with an
unknown mode throws `domain_error(io_mode, Culprit)`. Values of a wrong type raise type errors
instead (see `tuprolog.solve.exception.error.type`).

The error is a `DomainError`, and the domains are the values of the `Domain` enumeration (also
available as the `DOMAIN_*` constants). Build errors with `domain_error_for_argument` (the usual
case, for primitives' arguments), `domain_error_for_flag_values`, `domain_error_for_goal`, or
`domain_error_for_term`.

Examples:
    >>> from tuprolog.solve import signature
    >>> from tuprolog.solve.exception.error import *
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> context = prolog_solver().current_context
    >>> from tuprolog.core import integer
    >>> procedure = signature("foo", 2)
    >>> domain_error_for_argument(context, procedure, DOMAIN_NOT_LESS_THAN_ZERO, integer(-1)).type
    domain_error(not_less_than_zero, -1)
    >>> prolog_solver().solve_once("catch(atom_length(abc, -1), error(E, _), true)")["E"]
    domain_error(not_less_than_zero, -1)

See Also:
    `tuprolog.solve.primitive`, whose `ensuring_*` checks raise these errors;
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from ._api import *
from ._definitions import *

__all__ = [
    "DOMAIN_ATOM_PROPERTY",
    "DOMAIN_BUFFERING_MODE",
    "DOMAIN_CHARACTER_CODE_LIST",
    "DOMAIN_CLAUSE",
    "DOMAIN_CLOSE_OPTION",
    "DOMAIN_DATE_TIME",
    "DOMAIN_DIRECTIVE",
    "DOMAIN_EOF_ACTION",
    "DOMAIN_FACT",
    "DOMAIN_FLAG",
    "DOMAIN_FLAG_VALUE",
    "DOMAIN_FORMAT_CONTROL_SEQUENCE",
    "DOMAIN_IO_MODE",
    "DOMAIN_NON_EMPTY_LIST",
    "DOMAIN_NOT_LESS_THAN_ZERO",
    "DOMAIN_OPERATOR_PRIORITY",
    "DOMAIN_OPERATOR_SPECIFIER",
    "DOMAIN_ORDER",
    "DOMAIN_OS_FILE_PERMISSION",
    "DOMAIN_OS_FILE_PROPERTY",
    "DOMAIN_OS_PATH",
    "DOMAIN_PREDICATE_PROPERTY",
    "DOMAIN_READ_OPTION",
    "DOMAIN_RULE",
    "DOMAIN_SELECTABLE_ITEM",
    "DOMAIN_SOCKET_ADDRESS",
    "DOMAIN_SOCKET_DOMAIN",
    "DOMAIN_SOURCE_SINK",
    "DOMAIN_STREAM",
    "DOMAIN_STREAM_OPTION",
    "DOMAIN_STREAM_OR_ALIAS",
    "DOMAIN_STREAM_POSITION",
    "DOMAIN_STREAM_PROPERTY",
    "DOMAIN_STREAM_SEEK_METHOD",
    "DOMAIN_STREAM_TYPE",
    "DOMAIN_TERM_STREAM_OR_ALIAS",
    "DOMAIN_VAR_BINDING_OPTION",
    "DOMAIN_WELL_FORMED_LIST",
    "DOMAIN_WRITE_OPTION",
    "Domain",
    "DomainError",
    "domain_error_for_argument",
    "domain_error_for_flag_values",
    "domain_error_for_goal",
    "domain_error_for_term",
    "expected_domain",
]
