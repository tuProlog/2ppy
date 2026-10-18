import it.unibo.tuprolog.solve.exception.error as errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

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
]


DomainError = errors.DomainError
"""The domain error, thrown as `error(domain_error(Domain, Culprit), _)`.

It means that `Culprit` is not in `Domain`.

The JVM class (also a Python `ValueError` and a `tuprolog.errors.PrologDomainError`). Members
(snake_case aliases as well): `expected_domain`, the `Domain`; `culprit`, the offending term;
besides those of `tuprolog.solve.exception.LogicError` (e.g. `type`, `error_struct`, `message`).
"""


Domain = DomainError.Expected
"""The enumeration of the domains a domain error may refer to (2P-Kt's `DomainError.Expected`).

Each value (also available as a `DOMAIN_*` constant) is the `Domain` of a
`domain_error(Domain, Culprit)` term: `to_term()` gives it as an atom (e.g. `io_mode`), and
`domain` as a string. `Domain.of(name)` and `Domain.fromTerm(term)` look a value up (see
`expected_domain`).

Examples:
    >>> Domain.IO_MODE.to_term()
    io_mode
"""


DOMAIN_ATOM_PROPERTY = Domain.ATOM_PROPERTY
"""`atom_property`: the expected domain is a property of atoms."""


DOMAIN_BUFFERING_MODE = Domain.BUFFERING_MODE
"""`buffering_mode`: the expected domain is a buffering mode of streams (e.g. `line`, `block`)."""


DOMAIN_CHARACTER_CODE_LIST = Domain.CHARACTER_CODE_LIST
"""`character_code_list`: the expected domain is a list of character codes."""


DOMAIN_CLOSE_OPTION = Domain.CLOSE_OPTION
"""`close_option`: the expected domain is an option of `close/2` (e.g. `force(true)`)."""


DOMAIN_DATE_TIME = Domain.DATE_TIME
"""`date_time`: the expected domain is a date-time."""


DOMAIN_EOF_ACTION = Domain.EOF_ACTION
"""`eof_action`: the expected domain is an end-of-stream action (`error`, `eof_code`, `reset`)."""


DOMAIN_FLAG_VALUE = Domain.FLAG_VALUE
"""`flag_value`: the expected domain is an admissible value of a Prolog flag."""


DOMAIN_FORMAT_CONTROL_SEQUENCE = Domain.FORMAT_CONTROL_SEQUENCE
"""`format_control_sequence`: the expected domain is a control sequence of `format/2,3`."""


DOMAIN_IO_MODE = Domain.IO_MODE
"""`io_mode`: the expected domain is a mode of opening streams (`read`, `write`, `append`)."""


DOMAIN_WELL_FORMED_LIST = Domain.WELL_FORMED_LIST
"""`well_formed_list`: the expected domain is a well-formed list, i.e. one ending with `[]`."""


DOMAIN_NON_EMPTY_LIST = Domain.NON_EMPTY_LIST
"""`non_empty_list`: the expected domain is a non-empty list."""


DOMAIN_NOT_LESS_THAN_ZERO = Domain.NOT_LESS_THAN_ZERO
"""`not_less_than_zero`: the expected domain is a non-negative number."""


DOMAIN_OPERATOR_PRIORITY = Domain.OPERATOR_PRIORITY
"""`operator_priority`: the expected domain is an operator priority (an integer, 0 to 1200)."""


DOMAIN_OPERATOR_SPECIFIER = Domain.OPERATOR_SPECIFIER
"""`operator_specifier`: the expected domain is an operator specifier (e.g. `xfx`, `fy`, `yfx`)."""


DOMAIN_ORDER = Domain.ORDER
"""`order`: the expected domain is a comparison order (`<`, `=`, `>`)."""


DOMAIN_OS_FILE_PERMISSION = Domain.OS_FILE_PERMISSION
"""`os_file_permission`: the expected domain is a permission of files in the operating system."""


DOMAIN_OS_FILE_PROPERTY = Domain.OS_FILE_PROPERTY
"""`os_file_property`: the expected domain is a property of files in the operating system."""


DOMAIN_OS_PATH = Domain.OS_PATH
"""`os_path`: the expected domain is a path of the operating system."""


DOMAIN_PREDICATE_PROPERTY = Domain.PREDICATE_PROPERTY
"""`predicate_property`: the expected domain is a property of predicates (e.g. `dynamic`)."""


DOMAIN_FLAG = Domain.FLAG
"""`flag`: the expected domain is the name of a Prolog flag."""


DOMAIN_READ_OPTION = Domain.READ_OPTION
"""`read_option`: the expected domain is an option of `read_term/2,3` (e.g. `variables(Vs)`)."""


DOMAIN_SELECTABLE_ITEM = Domain.SELECTABLE_ITEM
"""`selectable_item`: the expected domain is an item that can be selected."""


DOMAIN_SOCKET_ADDRESS = Domain.SOCKET_ADDRESS
"""`socket_address`: the expected domain is a socket address."""


DOMAIN_SOCKET_DOMAIN = Domain.SOCKET_DOMAIN
"""`socket_domain`: the expected domain is a socket domain."""


DOMAIN_SOURCE_SINK = Domain.SOURCE_SINK
"""`source_sink`: the expected domain is a source or sink of a stream (e.g. a file name or URL)."""


DOMAIN_STREAM = Domain.STREAM
"""`stream`: the expected domain is a stream."""


DOMAIN_STREAM_OPTION = Domain.STREAM_OPTION
"""`stream_option`: the expected domain is an option of `open/4` (e.g. `alias(A)`)."""


DOMAIN_STREAM_OR_ALIAS = Domain.STREAM_OR_ALIAS
"""`stream_or_alias`: the expected domain is a stream, or the alias of one."""


DOMAIN_STREAM_POSITION = Domain.STREAM_POSITION
"""`stream_position`: the expected domain is a position in a stream."""


DOMAIN_STREAM_PROPERTY = Domain.STREAM_PROPERTY
"""`stream_property`: the expected domain is a property of streams (e.g. `alias(A)`, `input`)."""


DOMAIN_STREAM_SEEK_METHOD = Domain.STREAM_SEEK_METHOD
"""`stream_seek_method`: the expected domain is a method of seeking in a stream."""


DOMAIN_STREAM_TYPE = Domain.STREAM_TYPE
"""`stream_type`: the expected domain is a type of streams (`text`, `binary`)."""


DOMAIN_TERM_STREAM_OR_ALIAS = Domain.TERM_STREAM_OR_ALIAS
"""`term_stream_or_alias`: the expected domain is a term stream, or the alias of one."""


DOMAIN_VAR_BINDING_OPTION = Domain.VAR_BINDING_OPTION
"""`var_binding_option`: the expected domain is an option binding variables."""


DOMAIN_WRITE_OPTION = Domain.WRITE_OPTION
"""`write_option`: the expected domain is an option of `write_term/2,3` (e.g. `quoted(true)`)."""


DOMAIN_CLAUSE = Domain.CLAUSE
"""`clause`: the expected domain is a well-formed clause.

That is, a callable term, or a `Head :- Body` one with a callable head and body.
"""


DOMAIN_RULE = Domain.RULE
"""`rule`: the expected domain is a rule, i.e. a `Head :- Body` clause."""


DOMAIN_FACT = Domain.FACT
"""`fact`: the expected domain is a fact, i.e. a clause with no body."""


DOMAIN_DIRECTIVE = Domain.DIRECTIVE
"""`directive`: the expected domain is a directive, i.e. a `:- Goal` clause."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.DomainError.*")
