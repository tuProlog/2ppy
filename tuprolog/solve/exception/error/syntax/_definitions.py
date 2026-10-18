import it.unibo.tuprolog.solve.exception.error as _errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = []


SyntaxError = _errors.SyntaxError
"""The syntax error: some text is not valid Prolog, thrown as `error(syntax_error, _)`.

The JVM class (also a Python `ValueError` and a `tuprolog.errors.PrologSyntaxError`). Members:
those of `tuprolog.solve.exception.LogicError` (e.g. `type`, `error_struct`, `message`). Not
star-exported, as it would shadow Python's built-in `SyntaxError`: import it explicitly.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.SyntaxError.*")
