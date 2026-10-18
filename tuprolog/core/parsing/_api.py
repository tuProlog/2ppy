from collections.abc import Iterable
from typing import Any

from tuprolog.core import Atom, Clause, Constant, Integer, Numeric, Real, Struct, Term, Var
from tuprolog.core.operators import DEFAULT_OPERATORS, OperatorSet
from tuprolog.jvmioutils import InputStream

from ._definitions import DEFAULT_TERM_PARSER, DEFAULT_TERM_READER, TermParser, TermReader

__all__ = [
    "parse_atom",
    "parse_clause",
    "parse_constant",
    "parse_integer",
    "parse_numeric",
    "parse_real",
    "parse_struct",
    "parse_term",
    "parse_var",
    "parser_factory",
    "read_term",
    "read_terms",
    "term_parser",
    "term_reader",
]


def parser_factory(
    source: Any, with_default_operators: bool = True, operators: OperatorSet | None = None
) -> Any:
    """Builds a parser or a reader with a given operator set (used by `term_parser` and
    `term_reader`).

    Args:
        source: the factory, i.e. `TermParser` or `TermReader` (anything with
            `withDefaultOperators`, `withNoOperator` and `withOperators` methods).
        with_default_operators: whether to include the default operators (`DEFAULT_OPERATORS`).
        operators: other operators to include. If `None`, none.

    Returns:
        The parser (or reader).
    """
    if operators is None:
        if with_default_operators:
            return source.withDefaultOperators()
        else:
            return source.withNoOperator()
    else:
        if with_default_operators:
            return source.withOperators(DEFAULT_OPERATORS.plus(operators))  # type: ignore[attr-defined]
        else:
            return source.withOperators(operators)


def term_parser(
    with_default_operators: bool = True, operators: OperatorSet | None = None
) -> TermParser:
    """Creates a term parser with a given default operator set.

    Args:
        with_default_operators: whether to include the default operators (`DEFAULT_OPERATORS`).
        operators: other operators to include (e.g. declared by a program). If `None`, none.

    Returns:
        The parser.

    Examples:
        >>> from tuprolog.core.operators import XFX, operator, operator_set
        >>> parser = term_parser(operators=operator_set(operator("++", XFX, 700)))
        >>> parser.parse_term("X ++ 1 + 2")
        '++'(X_..., '+'(1, 2))
    """
    return parser_factory(TermParser, with_default_operators, operators)


def term_reader(
    with_default_operators: bool = True, operators: OperatorSet | None = None
) -> TermReader:
    """Creates a term reader with a given default operator set.

    Args:
        with_default_operators: whether to include the default operators (`DEFAULT_OPERATORS`).
        operators: other operators to include (e.g. declared by a program). If `None`, none.

    Returns:
        The reader (a `TermReader`).

    Examples:
        >>> import io
        >>> reader = term_reader()
        >>> reader.read_term(io.StringIO("f(X). g(Y)."))
        f(X_...)
    """
    return parser_factory(TermReader, with_default_operators, operators)


def parse_term(string: str, operators: OperatorSet | None = None) -> Term:
    """Parses a term from a string, with the default parser (`DEFAULT_TERM_PARSER`).

    Args:
        string: the text, in Prolog syntax, without the final `.`.
        operators: the operators to parse with, replacing the parser's default ones (so pass e.g.
            `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default ones.

    Returns:
        The term.

    Raises:
        ParseException: if `string` is not valid Prolog syntax.

    Examples:
        >>> parse_term("f(X, [1, 2 | T], 'Hello')")
        f(X_..., [1, 2 | T_...], 'Hello')
        >>> t = parse_term("f(X, X)")
        >>> t[0] == t[1]
        True
        >>> from tuprolog.core.operators import DEFAULT_OPERATORS, XFX, operator
        >>> parse_term("a ++ b", DEFAULT_OPERATORS + operator("++", XFX, 700))
        '++'(a, b)
    """
    return DEFAULT_TERM_PARSER.parse_term(string, operators)


def parse_struct(string: str, operators: OperatorSet | None = None) -> Struct:
    """Parses a structure from a string, with the default parser (`DEFAULT_TERM_PARSER`).

    Args:
        string: the text, in Prolog syntax, without the final `.`.
        operators: the operators to parse with, replacing the parser's default ones (so pass e.g.
            `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default ones.

    Returns:
        The structure.

    Raises:
        ParseException: if `string` is not valid Prolog syntax.
        InvalidTermTypeException: if `string` is valid, but represents another kind of term.

    Examples:
        >>> parse_struct("parent(homer, bart)").arity
        2
    """
    return DEFAULT_TERM_PARSER.parse_struct(string, operators)


def parse_constant(string: str, operators: OperatorSet | None = None) -> Constant:
    """Parses a constant (an atom or a number) from a string, with the default parser
    (`DEFAULT_TERM_PARSER`).

    Args:
        string: the text, in Prolog syntax, without the final `.`.
        operators: the operators to parse with, replacing the parser's default ones (so pass e.g.
            `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default ones.

    Returns:
        The constant.

    Raises:
        ParseException: if `string` is not valid Prolog syntax.
        InvalidTermTypeException: if `string` is valid, but represents another kind of term.

    Examples:
        >>> parse_constant("bart"), parse_constant("42")
        (bart, 42)
    """
    return DEFAULT_TERM_PARSER.parse_constant(string, operators)


def parse_var(string: str, operators: OperatorSet | None = None) -> Var:
    """Parses a variable from a string, with the default parser (`DEFAULT_TERM_PARSER`).

    Args:
        string: the text, in Prolog syntax, without the final `.`.
        operators: the operators to parse with, replacing the parser's default ones (so pass e.g.
            `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default ones.

    Returns:
        The variable.

    Raises:
        ParseException: if `string` is not valid Prolog syntax.
        InvalidTermTypeException: if `string` is valid, but represents another kind of term.

    Examples:
        >>> parse_var("X").name
        'X'
    """
    return DEFAULT_TERM_PARSER.parse_var(string, operators)


def parse_atom(string: str, operators: OperatorSet | None = None) -> Atom:
    """Parses an atom from a string, with the default parser (`DEFAULT_TERM_PARSER`).

    Args:
        string: the text, in Prolog syntax, without the final `.`.
        operators: the operators to parse with, replacing the parser's default ones (so pass e.g.
            `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default ones.

    Returns:
        The atom.

    Raises:
        ParseException: if `string` is not valid Prolog syntax.
        InvalidTermTypeException: if `string` is valid, but represents another kind of term.

    Examples:
        >>> parse_atom("'Hello World'").value
        'Hello World'
    """
    return DEFAULT_TERM_PARSER.parse_atom(string, operators)


def parse_numeric(string: str, operators: OperatorSet | None = None) -> Numeric:
    """Parses a number from a string, with the default parser (`DEFAULT_TERM_PARSER`).

    Args:
        string: the text, in Prolog syntax, without the final `.`.
        operators: the operators to parse with, replacing the parser's default ones (so pass e.g.
            `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default ones.

    Returns:
        The number (an integer or a real).

    Raises:
        ParseException: if `string` is not valid Prolog syntax.
        InvalidTermTypeException: if `string` is valid, but represents another kind of term.

    Examples:
        >>> parse_numeric("42"), parse_numeric("2.5"), parse_numeric("0x1F")
        (42, 2.5, 31)
    """
    return DEFAULT_TERM_PARSER.parse_numeric(string, operators)


def parse_integer(string: str, operators: OperatorSet | None = None) -> Integer:
    """Parses an integer from a string, with the default parser (`DEFAULT_TERM_PARSER`).

    Args:
        string: the text, in Prolog syntax, without the final `.`.
        operators: the operators to parse with, replacing the parser's default ones (so pass e.g.
            `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default ones.

    Returns:
        The integer.

    Raises:
        ParseException: if `string` is not valid Prolog syntax.
        InvalidTermTypeException: if `string` is valid, but represents another kind of term.

    Examples:
        >>> parse_integer("123456789012345678901234567890").value
        123456789012345678901234567890
    """
    return DEFAULT_TERM_PARSER.parse_integer(string, operators)


def parse_real(string: str, operators: OperatorSet | None = None) -> Real:
    """Parses a real number from a string, with the default parser (`DEFAULT_TERM_PARSER`).

    Args:
        string: the text, in Prolog syntax, without the final `.`.
        operators: the operators to parse with, replacing the parser's default ones (so pass e.g.
            `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default ones.

    Returns:
        The real.

    Raises:
        ParseException: if `string` is not valid Prolog syntax.
        InvalidTermTypeException: if `string` is valid, but represents another kind of term.

    Examples:
        >>> parse_real("3.14").value
        Decimal('3.14')
    """
    return DEFAULT_TERM_PARSER.parse_real(string, operators)


def parse_clause(string: str, operators: OperatorSet | None = None) -> Clause:
    """Parses a clause from a string, with the default parser (`DEFAULT_TERM_PARSER`).

    The text must be a rule or a fact with an explicit `:-` (e.g. `"p :- true"`), or a directive
    (`":- goal"`): a bare head, e.g. `"p"`, is not a clause here (wrap it with
    `tuprolog.core.fact`, or read whole programs with `tuprolog.theory.parsing`).

    Args:
        string: the text, in Prolog syntax, without the final `.`.
        operators: the operators to parse with, replacing the parser's default ones (so pass e.g.
            `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default ones.

    Returns:
        The clause.

    Raises:
        ParseException: if `string` is not valid Prolog syntax.
        InvalidTermTypeException: if `string` is valid, but represents another kind of term.

    Examples:
        >>> parse_clause("grandparent(X, Z) :- parent(X, Y), parent(Y, Z)")
        grandparent(X_..., Z_...) :- (parent(X_..., Y_...), parent(Y_..., Z_...))
        >>> parse_clause("parent(homer, bart) :- true"), parse_clause(":- dynamic(counter/1)")
        (parent(homer, bart) :- true, :- dynamic(counter/1))
    """
    return DEFAULT_TERM_PARSER.parse_clause(string, operators)


def read_term(input: InputStream | str, operators: OperatorSet | None = None) -> Term:
    """Reads the first term from a stream, with the default reader (`DEFAULT_TERM_READER`).

    Args:
        input: a Python stream (binary or text), a JVM `InputStream`, or a file path: a string is a
            path, not Prolog text (use `parse_term` for that). It is closed once read.
        operators: the operators to parse with, replacing the parser's default ones (so pass e.g.
            `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default ones.

    Returns:
        The first term (each term ends with `.`), or `None` if there is none.

    Raises:
        ParseException: if the text is not valid Prolog syntax.

    Examples:
        >>> import io
        >>> read_term(io.StringIO("parent(homer, bart). parent(abe, homer)."))
        parent(homer, bart)
    """
    return DEFAULT_TERM_READER.read_term(input, operators)


def read_terms(input: InputStream | str, operators: OperatorSet | None = None) -> Iterable[Term]:
    """Reads all the terms from a stream, lazily, with the default reader (`DEFAULT_TERM_READER`).

    Args:
        input: a Python stream (binary or text), a JVM `InputStream`, or a file path: a string is a
            path, not Prolog text. It is closed once read.
        operators: the operators to parse with, replacing the parser's default ones (so pass e.g.
            `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default ones.

    Returns:
        The terms (each ending with `.` in the text), as a lazy iterable, to consume once: syntax
        errors raise `ParseException` while iterating.

    Examples:
        >>> import io
        >>> list(read_terms(io.StringIO("parent(homer, bart). ancestor(X, Y) :- parent(X, Y).")))
        [parent(homer, bart), ancestor(X_..., Y_...) :- parent(X_..., Y_...)]
    """
    return DEFAULT_TERM_READER.read_terms(input, operators)
