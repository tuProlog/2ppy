import it.unibo.tuprolog.solve.exception.error as _errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["MessageError"]


MessageError = _errors.MessageError
"""The error carrying an arbitrary thrown term, used when no other `LogicError` fits.

The JVM class (also a `tuprolog.errors.PrologMessageError`). Members (snake_case aliases as
well): `content`, the thrown term; besides those of `tuprolog.solve.exception.LogicError`.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.MessageError.*")
