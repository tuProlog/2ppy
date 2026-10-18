import it.unibo.tuprolog.solve.exception.error as _errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = []


SystemError = _errors.SystemError
"""The system error: an internal problem occurred, thrown as `error(system_error, _)`.

The JVM class (also a Python `RuntimeError` and a `tuprolog.errors.PrologSystemError`). Members:
those of `tuprolog.solve.exception.LogicError` (e.g. `type`, `error_struct`, `message`, and
`cause`, the wrapped exception, if any). Not star-exported, as it would shadow Python's built-in
`SystemError`: import it explicitly.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.SystemError.*")
