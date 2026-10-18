from tuprolog.solve import ExecutionContext

from ._definitions import SyntaxError

__all__ = [
    "error_detector",
    "syntax_error",
    "syntax_error_while_parsing_clauses",
    "syntax_error_while_parsing_term",
]


def syntax_error(context: ExecutionContext, message: str) -> SyntaxError:
    """Creates a syntax error with a message, without positional information.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        message: the error message.

    Returns:
        The error, thrown as `error(syntax_error, Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> syntax_error(context, "missing dot").message
        'Syntax error: missing dot'
    """
    return SyntaxError.of(context, message)


def syntax_error_while_parsing_term(
    context: ExecutionContext, input: str, row: int, column: int, message: str
) -> SyntaxError:
    """Creates the syntax error for some text failing to parse as a term.

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        input: the text being parsed.
        row: the (1-based) line where parsing failed.
        column: the (1-based) column where parsing failed.
        message: the detail message.

    Returns:
        The error, thrown as `error(syntax_error, Message)`.

    Examples:
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.exception.error import *
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> context = prolog_solver().current_context
        >>> syntax_error_while_parsing_term(context, "f(", 1, 3, "unexpected end").message
        'Syntax error at 1:3 while parsing `f(`: unexpected end'
    """
    return SyntaxError.whileParsingTerm(context, input, row, column, message)


def syntax_error_while_parsing_clauses(
    context: ExecutionContext, input: str, index: int, row: int, column: int, message: str
) -> SyntaxError:
    """Creates the syntax error for a clause of some text failing to parse.

    The message shows the offending lines, with a caret (`^`) under the offending column (see
    `error_detector`).

    Args:
        context: the execution context in which the error occurs (e.g. a request's `context`).
        input: the text being parsed, e.g. a theory.
        index: the index of the clause failing to parse.
        row: the (1-based) line where parsing failed.
        column: the (1-based) column where parsing failed.
        message: the detail message.

    Returns:
        The error, thrown as `error(syntax_error, Message)`.
    """
    return SyntaxError.whileParsingClauses(context, input, index, row, column, message)


def error_detector(text: str, line: int, column: int, message: str | None = None) -> str:
    """Renders a line of a text with a caret (`^`) under a column, for error messages.

    The previous line, if any, is shown as well, for context.

    Args:
        text: the text.
        line: the (1-based) line to show.
        column: the (1-based) column to point at.
        message: a message to append after the caret, if any.

    Returns:
        The rendered lines, each prefixed by its number.

    Examples:
        >>> from tuprolog.solve.exception.error.syntax import error_detector
        >>> print(error_detector("foo(bar baz)", 1, 9, "unexpected"))
        1: foo(bar baz)
                   ^ unexpected
    """
    return SyntaxError.errorDetector(text, line, column, message)
