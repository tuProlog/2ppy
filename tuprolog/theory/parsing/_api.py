"""Factories of theory parsers and readers, and parsing through the default ones."""

from collections.abc import Iterable

from tuprolog.core import Clause
from tuprolog.core.operators import OperatorSet
from tuprolog.core.parsing import parser_factory
from tuprolog.jvmioutils import InputStream
from tuprolog.theory import Theory

from ._definitions import (
    DEFAULT_CLAUSES_PARSER,
    DEFAULT_CLAUSES_READER,
    ClausesParser,
    ClausesReader,
)

__all__ = [
    "clauses_parser",
    "clauses_reader",
    "parse_clauses",
    "parse_theory",
    "read_clauses",
    "read_theory",
]


def clauses_parser(
    with_default_operators: bool = True, operators: OperatorSet | None = None
) -> ClausesParser:
    """Creates a parser of clauses and theories from strings.

    Args:
        with_default_operators: Whether the parser knows the standard Prolog operators (True by
            default).
        operators: Further operators the parser knows, if not None: added to the standard ones
            if `with_default_operators`, or the only ones known otherwise.

    Returns:
        The parser.

    Examples:
        >>> from tuprolog.core.operators import XFX, operator, operator_set
        >>> parser = clauses_parser(operators=operator_set(operator("likes", XFX, 700)))
        >>> parser.parse_theory("alice likes pizza.")
        IndexedTheory{ likes(alice, pizza) :- true }

    See Also:
        `clauses_reader`, for files and streams.
    """
    return parser_factory(ClausesParser, with_default_operators, operators)


def clauses_reader(
    with_default_operators: bool = True, operators: OperatorSet | None = None
) -> ClausesReader:
    """Creates a reader of clauses and theories from files or streams.

    Args:
        with_default_operators: Whether the reader knows the standard Prolog operators (True by
            default).
        operators: Further operators the reader knows, if not None: added to the standard ones
            if `with_default_operators`, or the only ones known otherwise.

    Returns:
        The reader.

    Examples:
        >>> import io
        >>> clauses_reader().read_theory(io.StringIO("a. b."))
        IndexedTheory{ a :- true. b :- true }

    See Also:
        `clauses_parser`, for strings.
    """
    return parser_factory(ClausesReader, with_default_operators, operators)


def parse_theory(string: str, operators: OperatorSet | None = None) -> Theory:
    """Parses Prolog source code into a theory.

    Args:
        string: The source code: clauses, each one ended by a full stop.
        operators: The operators to use instead of the standard ones, if not None (see
            `tuprolog.core.operators`).

    Returns:
        The immutable, indexed theory of the parsed clauses, in order.

    Raises:
        ParsingError: If `string` is not valid Prolog (see `tuprolog.errors`).

    Examples:
        >>> parse_theory("mortal(X) :- human(X). human(socrates).")
        IndexedTheory{ mortal(X_...) :- human(X_...). human(socrates) :- true }
        >>> from tuprolog.errors import ParsingError
        >>> try:
        ...     parse_theory("a :- .")
        ... except ParsingError as error:
        ...     print(error.message)
        Operator ':-' (xfx, priority 1200) is missing its right operand

    See Also:
        `read_theory`, for files and streams.
    """
    return DEFAULT_CLAUSES_PARSER.parse_theory(string, operators)


def parse_clauses(
    string: str, operators: OperatorSet | None = None, lazy: bool = True
) -> Iterable[Clause]:
    """Parses Prolog source code into clauses.

    Args:
        string: The source code: clauses, each one ended by a full stop.
        operators: The operators to use instead of the standard ones, if not None (see
            `tuprolog.core.operators`).
        lazy: Whether clauses are parsed on demand, while iterating over the result (True by
            default), or all at once, into a list.

    Returns:
        The parsed clauses, in order: a lazy iterable, or a list.

    Raises:
        ParsingError: If `string` is not valid Prolog (when the invalid clause is reached, if
            `lazy`).

    Examples:
        >>> parse_clauses("a. b :- a.", lazy=False)
        [a :- true, b :- a]
    """
    if lazy:
        return DEFAULT_CLAUSES_PARSER.parse_clauses_lazily(string, operators)
    else:
        return DEFAULT_CLAUSES_PARSER.parse_clauses(string, operators)


def read_theory(input: InputStream | str, operators: OperatorSet | None = None) -> Theory:
    """Reads a theory from a file or stream.

    Args:
        input: A path (a string or a path-like object), a Python stream (e.g. `open("kb.pl")`,
            `io.StringIO`), or a JVM input stream.
        operators: The operators to use instead of the standard ones, if not None (see
            `tuprolog.core.operators`).

    Returns:
        The immutable, indexed theory of the clauses read, in order.

    Raises:
        ParsingError: If the input is not valid Prolog.

    Examples:
        >>> import io
        >>> read_theory(io.StringIO("parent(abe, homer)."))
        IndexedTheory{ parent(abe, homer) :- true }

    See Also:
        `parse_theory`, for strings.
    """
    return DEFAULT_CLAUSES_READER.read_theory(input, operators)


def read_clauses(
    input: InputStream | str, operators: OperatorSet | None = None, lazy: bool = True
) -> Iterable[Clause]:
    """Reads clauses from a file or stream.

    Args:
        input: A path (a string or a path-like object), a Python stream, or a JVM input stream.
        operators: The operators to use instead of the standard ones, if not None (see
            `tuprolog.core.operators`).
        lazy: Whether clauses are read on demand, while iterating over the result (True by
            default), or all at once, into a list.

    Returns:
        The clauses read, in order: a lazy iterable, or a list.

    Raises:
        ParsingError: If the input is not valid Prolog.

    Examples:
        >>> import io
        >>> read_clauses(io.BytesIO(b"a. b."), lazy=False)
        [a :- true, b :- true]
    """
    if lazy:
        return DEFAULT_CLAUSES_READER.read_clauses_lazily(input, operators)
    else:
        return DEFAULT_CLAUSES_READER.read_clauses(input, operators)
