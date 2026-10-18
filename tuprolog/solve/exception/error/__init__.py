"""ISO Prolog errors: the `error(Type, Extra)` terms predicates throw, one family per kind.

When a built-in predicate cannot do its job because of its arguments or of the system, ISO Prolog
has it throw a term `error(Type, Extra)`: `Type` classifies the problem, and `Extra` carries
implementation-defined details (2P-Kt puts a human-readable message there). Prolog code handles
them with `catch(Goal, error(Type, _), Recovery)`. In this library each error is a
`tuprolog.solve.exception.LogicError`, of the subclass matching its family:

| Family (sub-package) | `Type` | Meaning |
|---|---|---|
| `instantiation` | `instantiation_error` | an argument is unbound, but a value is needed |
| `type` | `type_error(Type, Culprit)` | `Culprit` is not of type `Type` (e.g. `integer`) |
| `domain` | `domain_error(Domain, Culprit)` | `Culprit` is of the right type, not in `Domain` |
| `existence` | `existence_error(Kind, Culprit)` | there is no `Kind` object `Culprit` |
| `permission` | `permission_error(Op, Kind, Culprit)` | `Op` is not allowed on `Culprit` |
| `representation` | `representation_error(Limit)` | an implementation limit is exceeded |
| `evaluation` | `evaluation_error(Error)` | an arithmetic expression cannot be evaluated |
| `syntax` | `syntax_error` | some text being read is not valid Prolog |
| `system` | `system_error` | an internal problem, e.g. an exception raised by Python code |
| `message` | any thrown term | a term fitting no ISO family (e.g. `throw(my_problem)`) |

This package re-exports every family: error classes, the enumerations of their parameters (e.g.
`Type`, `Domain`) with their values as constants (e.g. `TYPE_INTEGER`, `DOMAIN_IO_MODE`), and the
factories building errors (e.g. `type_error_for_argument`), which take the execution context the
error occurs in (in a primitive, the request's `context`). `TypeError`, `PermissionError`,
`SyntaxError`, and `SystemError` must be imported explicitly, as they shadow Python's built-ins.

Primitives raise these errors (or reply with them) to signal problems; the argument checks of
`tuprolog.solve.primitive` (`ensuring_*`) raise the standard ones.

Examples:
    >>> from tuprolog.core import atom
    >>> from tuprolog.solve.library import library
    >>> from tuprolog.solve.primitive import primitive
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> def colour(request):
    ...     [argument] = request.arguments
    ...     if str(argument) not in ("red", "green"):
    ...         domain = expected_domain("flag_value")
    ...         raise domain_error_for_argument(
    ...             request.context, request.signature, domain, argument, 0
    ...         )
    ...     yield request.reply_success()
    >>> lib = library("demo", primitives={"colour/1": primitive(colour)})
    >>> solver = prolog_solver(libraries=lib)
    >>> solver.solve_once("catch(colour(blue), error(E, _), true)")["E"]
    domain_error(flag_value, blue)

See Also:
    `tuprolog.solve.exception`, for the other exceptions;
    `tuprolog.errors`, for the Python exception classes of each family;
    2P-Kt's documentation on
    [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
"""

from .domain import *
from .evaluation import *
from .existence import *
from .instantiation import *
from .message import *
from .permission import *
from .permission import PermissionError  # not in __all__, as star-imports would shadow the builtin
from .representation import *
from .syntax import *
from .syntax import SyntaxError  # not in __all__, as star-imports would shadow the builtin
from .system import *
from .system import SystemError  # not in __all__, as star-imports would shadow the builtin
from .type import *
from .type import TypeError  # not in __all__, as star-imports would shadow the builtin

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
    "ERROR_FLOAT_OVERFLOW",
    "ERROR_INT_OVERFLOW",
    "ERROR_UNDEFINED",
    "ERROR_UNDERFLOW",
    "ERROR_ZERO_DIVISOR",
    "LIMIT_CHARACTER",
    "LIMIT_CHARACTER_CODE",
    "LIMIT_IN_CHARACTER_CODE",
    "LIMIT_MAX_ARITY",
    "LIMIT_MAX_INTEGER",
    "LIMIT_MIN_INTEGER",
    "LIMIT_OOP_OBJECT",
    "LIMIT_TOO_MANY_VARIABLES",
    "OBJECT_OOP_ALIAS",
    "OBJECT_OOP_CONSTRUCTOR",
    "OBJECT_OOP_METHOD",
    "OBJECT_OOP_PROPERTY",
    "OBJECT_PROCEDURE",
    "OBJECT_RESOURCE",
    "OBJECT_SOURCE_SINK",
    "OBJECT_STREAM",
    "OPERATION_ACCESS",
    "OPERATION_ADD_ALIAS",
    "OPERATION_CLOSE",
    "OPERATION_CREATE",
    "OPERATION_INPUT",
    "OPERATION_INVOKE",
    "OPERATION_MODIFY",
    "OPERATION_OPEN",
    "OPERATION_OUTPUT",
    "OPERATION_REPOSITION",
    "PERMISSION_BINARY_STREAM",
    "PERMISSION_FLAG",
    "PERMISSION_OOP_METHOD",
    "PERMISSION_OPERATOR",
    "PERMISSION_PAST_END_OF_STREAM",
    "PERMISSION_PRIVATE_PROCEDURE",
    "PERMISSION_SOURCE_SINK",
    "PERMISSION_STATIC_PROCEDURE",
    "PERMISSION_STREAM",
    "PERMISSION_TEXT_STREAM",
    "TYPE_ATOM",
    "TYPE_ATOMIC",
    "TYPE_BOOLEAN",
    "TYPE_BYTE",
    "TYPE_CALLABLE",
    "TYPE_CHARACTER",
    "TYPE_COMPOUND",
    "TYPE_DEALIASING_EXPRESSION",
    "TYPE_EVALUABLE",
    "TYPE_FLOAT",
    "TYPE_INTEGER",
    "TYPE_IN_CHARACTER",
    "TYPE_LIST",
    "TYPE_NUMBER",
    "TYPE_OBJECT_REFERENCE",
    "TYPE_PAIR",
    "TYPE_PREDICATE_INDICATOR",
    "TYPE_REFERENCE",
    "TYPE_TYPE_REFERENCE",
    "TYPE_URL",
    "TYPE_VARIABLE",
    "Domain",
    "DomainError",
    "ErrorType",
    "EvaluationError",
    "ExistenceError",
    "InstantiationError",
    "Limit",
    "MessageError",
    "ObjectType",
    "Operation",
    "Permission",
    "RepresentationError",
    "Type",
    "domain_error_for_argument",
    "domain_error_for_flag_values",
    "domain_error_for_goal",
    "domain_error_for_term",
    "error_detector",
    "error_type",
    "evaluation_error",
    "existence_error",
    "existence_error_for_procedure",
    "existence_error_for_resource",
    "existence_error_for_source_sink",
    "existence_error_for_stream",
    "expected_domain",
    "expected_type",
    "instantiation_error_for_argument",
    "instantiation_error_for_goal",
    "limit",
    "message_error",
    "object_type",
    "operation",
    "permission_error",
    "permission_type",
    "representation_error",
    "syntax_error",
    "syntax_error_while_parsing_clauses",
    "syntax_error_while_parsing_term",
    "system_error",
    "type_error",
    "type_error_for_argument",
    "type_error_for_argument_list",
    "type_error_for_goal",
    "type_error_for_term",
]
