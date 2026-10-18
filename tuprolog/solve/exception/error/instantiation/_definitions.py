import it.unibo.tuprolog.solve.exception.error as _errors  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["InstantiationError"]


InstantiationError = _errors.InstantiationError
"""The instantiation error, thrown as `error(instantiation_error, _)`: a term is unbound.

The JVM class (also a Python `ValueError` and a `tuprolog.errors.PrologInstantiationError`).
Members (snake_case aliases as well): `culprit`, the unbound variable; besides those of
`tuprolog.solve.exception.LogicError` (e.g. `type`, `error_struct`, `message`).
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.InstantiationError.*")
